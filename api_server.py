"""
Backend-API für den Steckbrief Manager (Prozesse & Projekte)
Verbindet das Frontend mit der MariaDB-Datenbank bcw_allgemein.t_hochschulsteckbriefe
Authentifizierung über Active Directory (LDAP), Rollenverwaltung in der DB
"""
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from functools import wraps
import mysql.connector
import jwt
import datetime
import os
from dotenv import load_dotenv
from ldap3 import Server, Connection, SIMPLE, ALL_ATTRIBUTES

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mariadb.bcw-intern.local'),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASS'],
    'database': os.environ.get('DB_NAME', 'bcw_allgemein'),
    'ssl_disabled': False
}

LDAP_SERVER = os.environ.get('LDAP_SERVER', 'ldap://bcw-intern.local')
LDAP_DOMAIN = os.environ.get('LDAP_DOMAIN', 'bcw-intern.local')
LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN', 'DC=bcw-intern,DC=local')
JWT_SECRET = os.environ.get('JWT_SECRET', 'change-me-in-production')
JWT_EXPIRY_HOURS = int(os.environ.get('JWT_EXPIRY_HOURS', '8'))
INITIAL_ADMIN = os.environ.get('INITIAL_ADMIN', '')

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# --- AD/LDAP Authentifizierung ---
def authenticate_ad(username, password):
    """Authentifiziert gegen Active Directory, gibt User-Info zurück oder None"""
    user_upn = f"{username}@{LDAP_DOMAIN}"
    server = Server(LDAP_SERVER, get_info='NO_INFO')
    try:
        conn = Connection(server, user=user_upn, password=password, authentication=SIMPLE, auto_bind=True)
        # Benutzerinfos abrufen
        conn.search(LDAP_BASE_DN, f'(sAMAccountName={username})',
                     attributes=['displayName', 'mail'])
        if conn.entries:
            entry = conn.entries[0]
            return {
                'username': username,
                'display_name': str(entry.displayName) if hasattr(entry, 'displayName') else username,
                'email': str(entry.mail) if hasattr(entry, 'mail') else ''
            }
        return {'username': username, 'display_name': username, 'email': ''}
    except Exception:
        return None
    finally:
        try:
            conn.unbind()
        except Exception:
            pass


# --- JWT-Hilfsfunktionen ---
def create_token(user_info, role):
    payload = {
        'username': user_info['username'],
        'display_name': user_info['display_name'],
        'email': user_info.get('email', ''),
        'role': role,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# --- Auth-Middleware ---
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Nicht authentifiziert'}), 401
        token_data = decode_token(auth_header[7:])
        if not token_data:
            return jsonify({'error': 'Token ungültig oder abgelaufen'}), 401
        g.user = token_data
        return f(*args, **kwargs)
    return decorated


def require_role(*roles):
    """Dekorator: Nur bestimmte Rollen dürfen zugreifen"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.user.get('role') not in roles:
                return jsonify({'error': 'Keine Berechtigung'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


# --- Auth-Endpoints ---
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'error': 'Benutzername und Passwort erforderlich'}), 400

    user_info = authenticate_ad(username, password)
    if not user_info:
        return jsonify({'error': 'Anmeldung fehlgeschlagen. Bitte prüfe Benutzername und Passwort.'}), 401

    # Benutzer in DB anlegen oder aktualisieren
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM t_steckbrief_users WHERE username = %s', (username,))
    db_user = cursor.fetchone()

    if not db_user:
        # Erster Login: Rolle bestimmen
        role = 'admin' if username == INITIAL_ADMIN.lower() else 'viewer'
        cursor.execute(
            'INSERT INTO t_steckbrief_users (username, display_name, email, role, last_login) VALUES (%s, %s, %s, %s, NOW())',
            (username, user_info['display_name'], user_info.get('email', ''), role)
        )
    else:
        role = db_user['role']
        cursor.execute(
            'UPDATE t_steckbrief_users SET display_name = %s, email = %s, last_login = NOW() WHERE username = %s',
            (user_info['display_name'], user_info.get('email', ''), username)
        )
    conn.commit()
    conn.close()

    token = create_token(user_info, role)
    return jsonify({
        'token': token,
        'username': username,
        'display_name': user_info['display_name'],
        'role': role
    })


@app.route('/api/auth/me', methods=['GET'])
@require_auth
def auth_me():
    return jsonify(g.user)


# --- Benutzerverwaltung (nur Admin) ---
@app.route('/api/users', methods=['GET'])
@require_auth
@require_role('admin')
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, username, display_name, email, role, created_at, last_login FROM t_steckbrief_users ORDER BY username')
    users = cursor.fetchall()
    for u in users:
        for key, val in u.items():
            if hasattr(val, 'isoformat'):
                u[key] = val.isoformat() if val else None
    conn.close()
    return jsonify(users)


@app.route('/api/users', methods=['POST'])
@require_auth
@require_role('admin')
def create_user_manual():
    """Legt einen Benutzer manuell an (Admin-Funktion)."""
    data = request.json or {}
    username = data.get('username', '').strip().lower()
    display_name = data.get('display_name', '').strip()
    role = data.get('role', 'viewer')

    if not username or not display_name:
        return jsonify({'error': 'Benutzername und Anzeigename sind erforderlich'}), 400
    if role not in ('viewer', 'editor', 'admin'):
        return jsonify({'error': 'Ungültige Rolle'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id FROM t_steckbrief_users WHERE username = %s', (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': f'Benutzer "{username}" existiert bereits'}), 409

    cursor.execute(
        'INSERT INTO t_steckbrief_users (username, display_name, email, role) VALUES (%s, %s, %s, %s)',
        (username, display_name, '', role)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': new_id}), 201


@app.route('/api/users/<int:uid>/role', methods=['PUT'])
@require_auth
@require_role('admin')
def update_user_role(uid):
    data = request.json or {}
    new_role = data.get('role', '')
    if new_role not in ('viewer', 'editor', 'admin'):
        return jsonify({'error': 'Ungültige Rolle'}), 400

    # Eigene Rolle darf nicht geändert werden
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT username FROM t_steckbrief_users WHERE id = %s', (uid,))
    target = cursor.fetchone()
    if not target:
        conn.close()
        return jsonify({'error': 'Benutzer nicht gefunden'}), 404
    if target['username'] == g.user['username']:
        conn.close()
        return jsonify({'error': 'Eigene Rolle kann nicht geändert werden'}), 400

    cursor.execute('UPDATE t_steckbrief_users SET role = %s WHERE id = %s', (new_role, uid))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/users/<int:uid>', methods=['DELETE'])
@require_auth
@require_role('admin')
def delete_user(uid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT username FROM t_steckbrief_users WHERE id = %s', (uid,))
    target = cursor.fetchone()
    if not target:
        conn.close()
        return jsonify({'error': 'Benutzer nicht gefunden'}), 404
    if target['username'] == g.user['username']:
        conn.close()
        return jsonify({'error': 'Eigener Account kann nicht gelöscht werden'}), 400
    cursor.execute('DELETE FROM t_steckbrief_users WHERE id = %s', (uid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/users/ensure-editor', methods=['POST'])
@require_auth
@require_role('admin')
def ensure_editor():
    """Legt einen Benutzer als Editor an, falls er noch nicht existiert."""
    data = request.json or {}
    fid = data.get('fid')
    display_name = data.get('display_name', '').strip()
    if not fid or not display_name:
        return jsonify({'error': 'fid und display_name erforderlich'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Person in datapool nachschlagen um Username abzuleiten
    cursor.execute(
        'SELECT Vorname, Nachname FROM datapool.t_personen WHERE PersonenID = %s',
        (fid,)
    )
    person = cursor.fetchone()
    if not person:
        conn.close()
        return jsonify({'error': 'Person nicht gefunden'}), 404

    username = f"{person['Vorname'].strip().lower()}.{person['Nachname'].strip().lower()}"

    # Prüfen ob User bereits existiert
    cursor.execute('SELECT id, role FROM t_steckbrief_users WHERE username = %s', (username,))
    existing = cursor.fetchone()

    if existing:
        # User existiert schon – falls nur Viewer, auf Editor hochstufen
        if existing['role'] == 'viewer':
            cursor.execute('UPDATE t_steckbrief_users SET role = %s WHERE id = %s', ('editor', existing['id']))
            conn.commit()
        conn.close()
        return jsonify({'success': True, 'action': 'updated' if existing['role'] == 'viewer' else 'exists'})

    # Neuen User als Editor anlegen
    cursor.execute(
        'INSERT INTO t_steckbrief_users (username, display_name, email, role) VALUES (%s, %s, %s, %s)',
        (username, display_name, '', 'editor')
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'action': 'created'})


# --- Personen-Suche ---
@app.route('/api/personen/suche', methods=['GET'])
@require_auth
def personen_suche():
    """Sucht Personen nach Name (für Autocomplete der FID-Felder)"""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT DISTINCT p.PersonenID, p.Vorname, p.Nachname, p.Titel_de, p.Geschlecht,
                  CASE
                    WHEN p.Nachname = %s OR p.Vorname = %s THEN 0
                    WHEN p.Nachname LIKE %s OR p.Vorname LIKE %s THEN 1
                    ELSE 2
                  END AS relevanz
           FROM datapool.t_personen p
           INNER JOIN tele_v.t_lohnmandanten lm ON lm.PersonenFID = p.PersonenID
               AND lm.Start <= CURDATE()
               AND (lm.End IS NULL OR lm.End >= CURDATE())
               AND lm.Deaktiviert = 0
           WHERE (p.Nachname LIKE %s OR p.Vorname LIKE %s) AND p.Deaktiviert='N'
           ORDER BY relevanz, p.Nachname, p.Vorname LIMIT 20""",
        (q, q, f'{q}%', f'{q}%', f'%{q}%', f'%{q}%')
    )
    results = cursor.fetchall()
    # Hilfsfeld entfernen
    for r in results:
        r.pop('relevanz', None)
    conn.close()
    return jsonify(results)


# --- Alle Steckbriefe laden ---
@app.route('/api/steckbriefe', methods=['GET'])
@require_auth
def get_steckbriefe():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    # Für Nicht-Admins: archivierte ausblenden
    include_archived = request.args.get('include_archived', '0')
    is_admin = g.user.get('role') == 'admin'
    where_clause = ''
    if not is_admin:
        where_clause = 'WHERE (s.archiviert IS NULL OR s.archiviert = 0)'
    elif include_archived == 'only':
        where_clause = 'WHERE s.archiviert = 1'
    cursor.execute(f"""
        SELECT s.*,
            pa.Vorname AS auftraggeber_vorname, pa.Nachname AS auftraggeber_nachname, pa.Titel_de AS auftraggeber_titel,
            pp.Vorname AS prozessmanager_vorname, pp.Nachname AS prozessmanager_nachname, pp.Titel_de AS prozessmanager_titel,
            pan.Vorname AS anforderungsmanager_vorname, pan.Nachname AS anforderungsmanager_nachname, pan.Titel_de AS anforderungsmanager_titel,
            pv.Vorname AS prozessverantwortlicher_vorname, pv.Nachname AS prozessverantwortlicher_nachname, pv.Titel_de AS prozessverantwortlicher_titel
        FROM t_hochschulsteckbriefe s
        LEFT JOIN datapool.t_personen pa ON s.auftraggeberFID = pa.PersonenID
        LEFT JOIN datapool.t_personen pp ON s.prozessmanagerFID = pp.PersonenID
        LEFT JOIN datapool.t_personen pan ON s.anforderungsmanagerFID = pan.PersonenID
        LEFT JOIN datapool.t_personen pv ON s.prozessverantwortlicherFID = pv.PersonenID
        {where_clause}
        ORDER BY s.id DESC
    """)
    rows = cursor.fetchall()
    # Datumswerte in Strings konvertieren
    for row in rows:
        for key, val in row.items():
            if hasattr(val, 'isoformat'):
                row[key] = val.isoformat() if val else None
    conn.close()
    return jsonify(rows)


# --- Einzelnen Steckbrief laden ---
@app.route('/api/steckbriefe/<int:sid>', methods=['GET'])
@require_auth
def get_steckbrief(sid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*,
            pa.Vorname AS auftraggeber_vorname, pa.Nachname AS auftraggeber_nachname, pa.Titel_de AS auftraggeber_titel,
            pp.Vorname AS prozessmanager_vorname, pp.Nachname AS prozessmanager_nachname, pp.Titel_de AS prozessmanager_titel,
            pan.Vorname AS anforderungsmanager_vorname, pan.Nachname AS anforderungsmanager_nachname, pan.Titel_de AS anforderungsmanager_titel,
            pv.Vorname AS prozessverantwortlicher_vorname, pv.Nachname AS prozessverantwortlicher_nachname, pv.Titel_de AS prozessverantwortlicher_titel
        FROM t_hochschulsteckbriefe s
        LEFT JOIN datapool.t_personen pa ON s.auftraggeberFID = pa.PersonenID
        LEFT JOIN datapool.t_personen pp ON s.prozessmanagerFID = pp.PersonenID
        LEFT JOIN datapool.t_personen pan ON s.anforderungsmanagerFID = pan.PersonenID
        LEFT JOIN datapool.t_personen pv ON s.prozessverantwortlicherFID = pv.PersonenID
        WHERE s.id = %s
    """, (sid,))
    row = cursor.fetchone()
    if row:
        for key, val in row.items():
            if hasattr(val, 'isoformat'):
                row[key] = val.isoformat() if val else None
    conn.close()
    if not row:
        return jsonify({'error': 'Nicht gefunden'}), 404
    return jsonify(row)


# --- Steckbrief speichern (neu oder update) ---
@app.route('/api/steckbriefe', methods=['POST'])
@require_auth
@require_role('editor', 'admin')
def save_steckbrief():
    data = request.json
    # DEBUG: Log received person FIDs
    print(f"[SAVE DEBUG] Received FIDs: auftraggeber={data.get('auftraggeberFID')}, prozessmanager={data.get('prozessmanagerFID')}, anforderungsmanager={data.get('anforderungsmanagerFID')}, prozessverantwortlicher={data.get('prozessverantwortlicherFID')}, id={data.get('id')}")
    conn = get_db()
    cursor = conn.cursor()

    fields = [
        'titel', 'auftraggeberFID', 'auftraggeber_multi', 'prozessmanagerFID', 'anforderungsmanagerFID',
        'prozessverantwortlicherFID', 'projektteam', 'it_unterstuetzung', 'prozesscluster', 'prioritaet', 'umsetzungsaufwand',
        'betroffener_lifecycle', 'ziel_vision', 'warum', 'wer', 'welche', 'was', 'wie', 'wo', 'wann',
        'einordnung_gesamtprozess',
        'bewertung_strategie', 'bewertung_strategie_text',
        'bewertung_recht', 'bewertung_recht_text',
        'bewertung_technik', 'bewertung_technik_text',
        'bewertung_kunden', 'bewertung_kunden_text',
        'bewertung_lehrende', 'bewertung_lehrende_text',
        'bewertung_lieferanten', 'bewertung_lieferanten_text',
        'bewertung_mitarbeitende', 'bewertung_mitarbeitende_text',
        'nutzen_durchlaufzeiten', 'nutzen_durchlaufzeiten_text',
        'nutzen_fehler', 'nutzen_fehler_text',
        'nutzen_kosten', 'nutzen_kosten_text',
        'nutzen_reduktion', 'nutzen_reduktion_text',
        'nutzen_studierende', 'nutzen_studierende_text',
        'nutzen_qualitaet', 'nutzen_qualitaet_text',
        'nutzen_vzae',
        'aenderungshistorie',
        'bearbeiter',
        'identifikationsnummer',
        'uebermittlung_datum', 'grobkonzept_datum', 'freigabe_datum',
        'beginn_datum', 'fertigstellung_datum', 'abnahme_datum',
        'kommunikation_datum', 'auswertung_datum',
        'status_optimierung',
        'start', 'gesamtstatus', 'fortschritt', 'status_steckbrief', 'teil_hochschulentwicklungsplan',
        'geplanter_abschluss',
        'phasen_data',
        'zeitplan_data'
    ]

    # Leere Strings in None umwandeln für korrekte DB-Typen
    sid = data.get('id')

    if sid:
        # Update: Nur die tatsächlich gesendeten Felder aktualisieren
        update_fields = [f for f in fields if f in data]
        if not update_fields:
            conn.close()
            return jsonify({'id': sid, 'success': True})
        values = []
        for f in update_fields:
            val = data.get(f)
            if val == '' or val is None:
                values.append(None)
            else:
                values.append(val)
        set_clause = ', '.join([f"{f} = %s" for f in update_fields])
        sql = f"UPDATE t_hochschulsteckbriefe SET {set_clause} WHERE id = %s"
        cursor.execute(sql, values + [sid])
    else:
        # Insert: Alle Felder
        values = []
        for f in fields:
            val = data.get(f)
            if val == '' or val is None:
                values.append(None)
            else:
                values.append(val)
        placeholders = ', '.join(['%s'] * len(fields))
        cols = ', '.join(fields)
        sql = f"INSERT INTO t_hochschulsteckbriefe ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        sid = cursor.lastrowid

    conn.commit()
    conn.close()
    return jsonify({'id': sid, 'success': True})


# --- Steckbrief archivieren / wiederherstellen ---
@app.route('/api/steckbriefe/<int:sid>/archiv', methods=['POST'])
@require_auth
@require_role('admin')
def toggle_archiv(sid):
    data = request.json
    archiviert = 1 if data.get('archiviert') else 0
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE t_hochschulsteckbriefe SET archiviert = %s WHERE id = %s", (archiviert, sid))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'archiviert': archiviert})


# --- Steckbrief löschen ---
@app.route('/api/steckbriefe/<int:sid>', methods=['DELETE'])
@require_auth
@require_role('editor', 'admin')
def delete_steckbrief(sid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM t_hochschulsteckbriefe WHERE id = %s", (sid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
