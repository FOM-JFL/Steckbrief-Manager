"""
Skript zum Importieren der bestehenden Steckbriefe aus DOCX-Dateien in JSON-Format.
"""

import os
import json
import re
from docx import Document
from datetime import datetime

def extract_steckbrief(docx_path):
    """Extrahiert Steckbrief-Daten aus einer DOCX-Datei."""
    doc = Document(docx_path)
    steckbrief = {
        'id': 'sb_' + str(int(datetime.now().timestamp() * 1000)) + '_' + os.path.basename(docx_path)[:8],
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat(),
        'quelldatei': os.path.basename(docx_path)
    }
    
    # Tabellen durchgehen
    for table_idx, table in enumerate(doc.tables):
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            
            if len(cells) >= 2:
                key = cells[0].lower()
                value = cells[1] if len(cells) > 1 else ''
                
                # Stammdaten (Tabelle 1)
                if 'titel' in key:
                    steckbrief['titel'] = value
                elif 'auftraggeber' in key:
                    steckbrief['auftraggeber'] = value
                elif 'prozessmanager' in key:
                    steckbrief['prozessmanager'] = value
                elif 'anforderungsmanager' in key:
                    steckbrief['anforderungsmanager'] = value
                elif 'prozessverantwortlich' in key:
                    steckbrief['prozessverantwortlicher'] = value
                elif 'projektteam' in key or 'prozessteam' in key:
                    steckbrief['projektteam'] = value
                elif 'prozesscluster' in key:
                    steckbrief['prozesscluster'] = value
                elif 'umsetzungsaufwand' in key:
                    # Aufwand extrahieren (kann in einer späteren Spalte sein)
                    aufwand_text = ' '.join(cells[1:]).lower() if len(cells) > 1 else ''
                    if 'groß' in aufwand_text or 'gross' in aufwand_text:
                        if 'mittel' in aufwand_text:
                            steckbrief['umsetzungsaufwand'] = 'mittel-gross'
                        else:
                            steckbrief['umsetzungsaufwand'] = 'gross'
                    elif 'mittel' in aufwand_text:
                        steckbrief['umsetzungsaufwand'] = 'mittel'
                    elif 'klein' in aufwand_text:
                        steckbrief['umsetzungsaufwand'] = 'klein'
                
                # W-Fragen (Tabelle 2)
                elif 'warum' in key:
                    steckbrief['warum'] = value
                elif key.startswith('wer'):
                    steckbrief['wer'] = value
                elif 'welche' in key:
                    steckbrief['welche'] = value
                elif key.startswith('was'):
                    steckbrief['was'] = value
                elif key.startswith('wie'):
                    steckbrief['wie'] = value
                elif key.startswith('wo'):
                    steckbrief['wo'] = value
                elif 'wann' in key:
                    steckbrief['wann'] = value
                
                # Bewertungskriterien (Tabellen 3 und 4)
                elif 'unternehmensstrategisch' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_strategie'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_strategie_text'] = cells[2] if len(cells) > 2 else ''
                elif 'rechtlich' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_recht'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_recht_text'] = cells[2] if len(cells) > 2 else ''
                elif 'technisch' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_technik'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_technik_text'] = cells[2] if len(cells) > 2 else ''
                elif 'kunden' in key and 'anforderung' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_kunden'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_kunden_text'] = cells[2] if len(cells) > 2 else ''
                elif 'lehrende' in key and 'anforderung' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_lehrende'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_lehrende_text'] = cells[2] if len(cells) > 2 else ''
                elif 'lieferanten' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_lieferanten'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_lieferanten_text'] = cells[2] if len(cells) > 2 else ''
                elif 'mitarbeitende' in key and 'anforderung' in key:
                    if len(cells) >= 3:
                        steckbrief['bewertung_mitarbeitende'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['bewertung_mitarbeitende_text'] = cells[2] if len(cells) > 2 else ''
                
                # Nutzen-Bewertungen
                elif 'durchlaufzeit' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_durchlaufzeiten'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_durchlaufzeiten_text'] = cells[2] if len(cells) > 2 else ''
                elif 'fehlerwiederholung' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_fehler'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_fehler_text'] = cells[2] if len(cells) > 2 else ''
                elif 'prozesskosten' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_kosten'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_kosten_text'] = cells[2] if len(cells) > 2 else ''
                elif 'nicht wertschöpfend' in key or 'reduktion' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_reduktion'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_reduktion_text'] = cells[2] if len(cells) > 2 else ''
                elif 'studierendenzahl' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_studierende'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_studierende_text'] = cells[2] if len(cells) > 2 else ''
                elif 'qualität' in key:
                    if len(cells) >= 3:
                        steckbrief['nutzen_qualitaet'] = cells[1] if cells[1].isdigit() else '0'
                        steckbrief['nutzen_qualitaet_text'] = cells[2] if len(cells) > 2 else ''
    
    # Falls kein Titel gefunden wurde, Dateiname verwenden
    if 'titel' not in steckbrief or not steckbrief['titel']:
        steckbrief['titel'] = os.path.splitext(os.path.basename(docx_path))[0]
    
    if 'auftraggeber' not in steckbrief:
        steckbrief['auftraggeber'] = ''
    
    return steckbrief


def main():
    """Hauptfunktion zum Importieren aller Steckbriefe."""
    steckbriefe_dir = r'p:\Steckbrief-Manager\Volle Steckbriefe_2026_03_02'
    output_file = r'p:\Steckbrief-Manager\steckbriefe.json'
    
    steckbriefe = []
    
    # Alle DOCX-Dateien im Verzeichnis durchgehen
    for filename in os.listdir(steckbriefe_dir):
        if filename.endswith('.docx'):
            docx_path = os.path.join(steckbriefe_dir, filename)
            print(f'Verarbeite: {filename}')
            try:
                steckbrief = extract_steckbrief(docx_path)
                steckbriefe.append(steckbrief)
                print(f'  -> Titel: {steckbrief.get("titel", "Unbekannt")}')
            except Exception as e:
                print(f'  -> Fehler: {e}')
    
    # JSON speichern
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(steckbriefe, f, ensure_ascii=False, indent=2)
    
    print(f'\n{len(steckbriefe)} Steckbriefe exportiert nach: {output_file}')
    print('Sie können diese Datei in der Web-Oberfläche über "Import" laden.')


if __name__ == '__main__':
    main()
