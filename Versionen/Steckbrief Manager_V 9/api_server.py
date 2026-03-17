"""
Backend-API für den Steckbrief-Manager
Verbindet das Frontend mit der MariaDB-Datenbank bcw_allgemein.t_hochschulsteckbriefe
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'mariadb.bcw-intern.local',
    'user': os.environ.get('DB_USER', 'ralf.schmitz'),
    'password': os.environ.get('DB_PASS', 'd-kvsl1715'),
    'database': 'bcw_allgemein',
    'ssl_disabled': False
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# --- Personen-Suche ---
@app.route('/api/personen/suche', methods=['GET'])
def personen_suche():
    """Sucht Personen nach Name (für Autocomplete der FID-Felder)"""
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT DISTINCT p.PersonenID, p.Vorname, p.Nachname, p.Titel_de
           FROM datapool.t_personen p
           INNER JOIN tele_v.t_lohnmandanten lm ON lm.PersonenFID = p.PersonenID
               AND lm.Start <= CURDATE()
               AND (lm.End IS NULL OR lm.End >= CURDATE())
               AND lm.Deaktiviert = 0
           WHERE (p.Nachname LIKE %s OR p.Vorname LIKE %s) AND p.Deaktiviert='N'
           ORDER BY p.Nachname, p.Vorname LIMIT 20""",
        (f'%{q}%', f'%{q}%')
    )
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)


# --- Alle Steckbriefe laden ---
@app.route('/api/steckbriefe', methods=['GET'])
def get_steckbriefe():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*,
            pa.Vorname AS auftraggeber_vorname, pa.Nachname AS auftraggeber_nachname,
            pp.Vorname AS prozessmanager_vorname, pp.Nachname AS prozessmanager_nachname,
            pan.Vorname AS anforderungsmanager_vorname, pan.Nachname AS anforderungsmanager_nachname,
            pv.Vorname AS prozessverantwortlicher_vorname, pv.Nachname AS prozessverantwortlicher_nachname
        FROM t_hochschulsteckbriefe s
        LEFT JOIN datapool.t_personen pa ON s.auftraggeberFID = pa.PersonenID
        LEFT JOIN datapool.t_personen pp ON s.prozessmanagerFID = pp.PersonenID
        LEFT JOIN datapool.t_personen pan ON s.anforderungsmanagerFID = pan.PersonenID
        LEFT JOIN datapool.t_personen pv ON s.prozessverantwortlicherFID = pv.PersonenID
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
def get_steckbrief(sid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*,
            pa.Vorname AS auftraggeber_vorname, pa.Nachname AS auftraggeber_nachname,
            pp.Vorname AS prozessmanager_vorname, pp.Nachname AS prozessmanager_nachname,
            pan.Vorname AS anforderungsmanager_vorname, pan.Nachname AS anforderungsmanager_nachname,
            pv.Vorname AS prozessverantwortlicher_vorname, pv.Nachname AS prozessverantwortlicher_nachname
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
def save_steckbrief():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    fields = [
        'titel', 'auftraggeberFID', 'prozessmanagerFID', 'anforderungsmanagerFID',
        'prozessverantwortlicherFID', 'projektteam', 'prozesscluster', 'umsetzungsaufwand',
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
        'aenderungshistorie',
        'bearbeiter',
        'identifikationsnummer',
        'uebermittlung_datum', 'grobkonzept_datum', 'freigabe_datum',
        'beginn_datum', 'fertigstellung_datum', 'abnahme_datum',
        'kommunikation_datum', 'auswertung_datum',
        'start', 'gesamtstatus', 'status_steckbrief', 'teil_hochschulentwicklungsplan'
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


# --- Steckbrief löschen ---
@app.route('/api/steckbriefe/<int:sid>', methods=['DELETE'])
def delete_steckbrief(sid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM t_hochschulsteckbriefe WHERE id = %s", (sid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
