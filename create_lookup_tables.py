"""
Erstellt die Hilfstabellen für den Steckbrief-Manager
im Schema HochschulorgaApps auf mariadb.bcw-intern.local
"""
import mysql.connector

DB_CONFIG = {
    'host': 'mariadb.bcw-intern.local',
    'user': 'HochschulorgaApps',
    'password': '%z8J9xjZha)9,)Jn',
    'database': 'HochschulorgaApps',
    'ssl_disabled': False
}

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # -------------------------------------------------------
    # 1. Rollen
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_rollen (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rolle VARCHAR(50) NOT NULL UNIQUE,
            bezeichnung VARCHAR(100) NOT NULL,
            farbe_bg VARCHAR(10),
            farbe_text VARCHAR(10),
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_rollen")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_rollen (rolle, bezeichnung, farbe_bg, farbe_text, sortierung) VALUES (%s,%s,%s,%s,%s)",
            [
                ('admin',       'Administrator', '#fce4ec', '#c62828', 1),
                ('editor',      'Editor',        '#e8f5e9', '#2e7d32', 2),
                ('viewer',      'Nur Lesen',     '#e3f2fd', '#1565c0', 3),
                ('deactivated', 'Deaktiviert',   '#f5f5f5', '#9e9e9e', 4),
            ]
        )
    print("✓ SteckbriefManager_rollen")

    # -------------------------------------------------------
    # 2. Prozesscluster
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_prozesscluster (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bezeichnung VARCHAR(200) NOT NULL UNIQUE,
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_prozesscluster")
    if cursor.fetchone()[0] == 0:
        cluster = [
            '/',
            'Leitbild & Charta entwickeln',
            '(Hochschul-)Entwicklung planen',
            'Organisation & QM lenken',
            'Organisation & QM weiterentwickeln',
            'Studiengänge (weiter-)entwickeln',
            'Studieneinstieg durchführen',
            'Semesterplanung durchführen',
            'Lehren & Lernen inkl. Feedback gestalten',
            'Studienbegleitende Prüfungen organisieren',
            'Studierende & Lehrende beraten',
            'Studienabschluss umsetzen',
            'Lehre & Studium evaluieren',
            'Forschungsfragen identifizieren',
            'Forschungsmittel akquirieren',
            'Forschungsprojekte organisieren',
            'Forschungsprojekte durchführen',
            'Forschungsergebnisse transferieren',
            'Forschungsprojekte abschließen',
            'Forschung evaluieren',
            'Lehrgänge (weiter-)entwickeln',
            'Lehrgangseinstieg durchführen',
            'Lehrgangsplanung durchführen',
            'Lehrgangsbegleitende Prüfungen organisieren',
            'Lehrgangsteilnehmende & Lehrende beraten',
            'Lehrgangsabschluss umsetzen',
            'Fort-/Weiterbildung evaluieren',
            'Lehrangebot vermarkten & Informationen bereitstellen',
            'Studierende & Teilnehmende gewinnen',
            '(Lehr-)Personal bereitstellen',
            'Räumliche & sächliche Infrastruktur bereitstellen',
            'IT-Strukturen bereitstellen',
            'Finanzen bewirtschaften',
        ]
        cursor.executemany(
            "INSERT INTO SteckbriefManager_prozesscluster (bezeichnung, sortierung) VALUES (%s,%s)",
            [(b, i) for i, b in enumerate(cluster)]
        )
    print("✓ SteckbriefManager_prozesscluster")

    # -------------------------------------------------------
    # 3. Gesamtstatus
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_gesamtstatus (
            id INT AUTO_INCREMENT PRIMARY KEY,
            status VARCHAR(100) NOT NULL UNIQUE,
            css_klasse VARCHAR(50),
            farbe_bg VARCHAR(10),
            farbe_text VARCHAR(10),
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_gesamtstatus")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_gesamtstatus (status, css_klasse, farbe_bg, farbe_text, sortierung) VALUES (%s,%s,%s,%s,%s)",
            [
                ('/',                  'status-grey',   '#f5f5f5', '#757575', 0),
                ('Idee / Konzeption',  'status-blue',   '#e3f2fd', '#1565c0', 1),
                ('Geplant',            'status-blue',   '#e3f2fd', '#1565c0', 2),
                ('In Umsetzung',       'status-orange', '#fff3e0', '#e65100', 3),
                ('Pilotierung',        'status-orange', '#fff3e0', '#e65100', 4),
                ('Im Betrieb',         'status-green',  '#e8f5e9', '#2e7d32', 5),
                ('Pausiert',           'status-grey',   '#f5f5f5', '#757575', 6),
                ('Abgebrochen',        'status-red',    '#ffebee', '#c62828', 7),
            ]
        )
    print("✓ SteckbriefManager_gesamtstatus")

    # -------------------------------------------------------
    # 4. Status Steckbrief
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_status_steckbrief (
            id INT AUTO_INCREMENT PRIMARY KEY,
            status VARCHAR(100) NOT NULL UNIQUE,
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_status_steckbrief")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_status_steckbrief (status, sortierung) VALUES (%s,%s)",
            [
                ('/',                       0),
                ('Noch nicht gefüllt',      1),
                ('Rahmendaten hinterlegt',  2),
                ('Gefüllt',                 3),
            ]
        )
    print("✓ SteckbriefManager_status_steckbrief")

    # -------------------------------------------------------
    # 5. Life-Cycle
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_lifecycle (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bezeichnung VARCHAR(100) NOT NULL UNIQUE,
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_lifecycle")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_lifecycle (bezeichnung, sortierung) VALUES (%s,%s)",
            [
                ('/',                       0),
                ('Student-Life-Cycle',      1),
                ('Product-Life-Cycle',      2),
                ('Lehrenden-Life-Cycle',    3),
            ]
        )
    print("✓ SteckbriefManager_lifecycle")

    # -------------------------------------------------------
    # 6. Umsetzungsaufwand
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_umsetzungsaufwand (
            id INT AUTO_INCREMENT PRIMARY KEY,
            aufwand VARCHAR(50) NOT NULL UNIQUE,
            bezeichnung VARCHAR(100) NOT NULL,
            farbe_bg VARCHAR(10),
            farbe_text VARCHAR(10),
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_umsetzungsaufwand")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_umsetzungsaufwand (aufwand, bezeichnung, farbe_bg, farbe_text, sortierung) VALUES (%s,%s,%s,%s,%s)",
            [
                ('klein',  'Klein',  '#e8f5e9', '#2e7d32', 1),
                ('mittel', 'Mittel', '#fff8e1', '#f57c00', 2),
                ('gross',  'Groß',   '#ffebee', '#c62828', 3),
            ]
        )
    print("✓ SteckbriefManager_umsetzungsaufwand")

    # -------------------------------------------------------
    # 7. Bewertungskriterien (Zwänge + Nutzen)
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_bewertungskriterien (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kategorie ENUM('zwang','nutzen') NOT NULL,
            db_feld VARCHAR(100) NOT NULL UNIQUE,
            bezeichnung VARCHAR(200) NOT NULL,
            skala_0 VARCHAR(50) DEFAULT 'irrelevant',
            skala_1 VARCHAR(50),
            skala_2 VARCHAR(50),
            skala_3 VARCHAR(50),
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_bewertungskriterien")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """INSERT INTO SteckbriefManager_bewertungskriterien
               (kategorie, db_feld, bezeichnung, skala_0, skala_1, skala_2, skala_3, sortierung)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            [
                ('zwang',  'bewertung_strategie',      'Unternehmensstrategische Anforderungen', 'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 1),
                ('zwang',  'bewertung_recht',           'Rechtliche Vorschriften',               'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 2),
                ('zwang',  'bewertung_technik',         'Technische Zwänge',                     'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 3),
                ('zwang',  'bewertung_kunden',          'Anforderungen Kunden',                  'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 4),
                ('zwang',  'bewertung_lehrende',        'Anforderungen Lehrende',                'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 5),
                ('zwang',  'bewertung_lieferanten',     'Anforderungen Lieferanten',             'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 6),
                ('zwang',  'bewertung_mitarbeitende',   'Anforderungen Mitarbeitende',           'irrelevant', 'förderlich',       'wichtig',         'zwingend notwendig', 7),
                ('nutzen', 'nutzen_durchlaufzeiten',    'Senkung der Durchlaufzeiten',           'irrelevant', 'geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',       1),
                ('nutzen', 'nutzen_fehler',             'Vermeidung von Fehlerwiederholungsraten','irrelevant','geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',       2),
                ('nutzen', 'nutzen_kosten',             'Senkung der Prozesskosten',             'irrelevant', 'geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',       3),
                ('nutzen', 'nutzen_reduktion',          'Reduktion nicht wertschöpfender Prozesse','irrelevant','geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',      4),
                ('nutzen', 'nutzen_studierende',        'Steigerung der Studierendenzahlen',     'irrelevant', 'geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',       5),
                ('nutzen', 'nutzen_qualitaet',          'Qualitätszuwachs',                      'irrelevant', 'geringerer Nutzen','mittlerer Nutzen','hoher Nutzen',       6),
            ]
        )
    print("✓ SteckbriefManager_bewertungskriterien")

    # -------------------------------------------------------
    # 8. Prioritäten
    # -------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SteckbriefManager_prioritaeten (
            id INT AUTO_INCREMENT PRIMARY KEY,
            wert INT NOT NULL UNIQUE,
            bezeichnung VARCHAR(100),
            sortierung INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cursor.execute("SELECT COUNT(*) FROM SteckbriefManager_prioritaeten")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO SteckbriefManager_prioritaeten (wert, bezeichnung, sortierung) VALUES (%s,%s,%s)",
            [
                (1, None, 1),
                (2, None, 2),
                (3, None, 3),
                (4, None, 4),
                (5, None, 5),
                (6, None, 6),
            ]
        )
    print("✓ SteckbriefManager_prioritaeten")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n✅ Alle 8 Hilfstabellen erfolgreich angelegt und befüllt.")


if __name__ == '__main__':
    main()
