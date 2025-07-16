# Drive Letter Manager

Ein portables Windows-Programm zur einfachen Verwaltung von Laufwerksbuchstaben. Perfekt für Situationen, in denen nach einer Windows-Neuinstallation die Laufwerksbuchstaben nicht mehr stimmen.

## 🚀 Features

- **Portable**: Läuft direkt aus einer .exe-Datei ohne Installation
- **Einfach**: Intuitive grafische Benutzeroberfläche
- **Sicher**: Verwendet native Windows-Tools (diskpart)
- **Kompatibel**: Funktioniert ab Windows 7
- **Übersichtlich**: Zeigt alle Laufwerke mit Bezeichnungen an
- **Benutzerfreundlich**: Dropdown-Menüs für einfache Auswahl

## 📋 Systemanforderungen

- Windows 7 oder höher
- Administratorrechte (für Laufwerksbuchstaben-Änderungen)
- Keine zusätzlichen Abhängigkeiten erforderlich

## 🔧 Installation und Verwendung

### Option 1: Fertige .exe verwenden
1. Laden Sie `DriveLetterManager.exe` herunter
2. Starten Sie die Datei **als Administrator** (Rechtsklick → "Als Administrator ausführen")
3. Das Programm zeigt alle verfügbaren Laufwerke in einer übersichtlichen Tabelle an
4. **Klicken Sie in die Spalte "Neuer Buchstabe"** für das gewünschte Laufwerk
5. **Wählen Sie aus dem Dropdown-Menü** den neuen Buchstaben aus
6. **Wiederholen Sie dies** für weitere Laufwerke (Batch-Änderungen möglich)
7. Klicken Sie auf **"Ausgewählte Änderungen durchführen"**

### Option 2: Aus Quellcode kompilieren

#### Voraussetzungen
- Python 3.7 oder höher
- pip (Python Package Installer)

#### Schritte
1. Klonen oder laden Sie das Repository herunter
2. Öffnen Sie eine Eingabeaufforderung im Projektordner
3. Führen Sie das Build-Skript aus:
   ```batch
   build_simple.bat
   ```
4. Die fertige .exe finden Sie im `dist`-Ordner

#### Manuelle Kompilierung
```batch
# PyInstaller installieren
pip install pyinstaller

# .exe erstellen
pyinstaller --onefile --windowed --name "DriveLetterManager" drive_letter_manager.py
```

## 🖥️ Benutzeroberfläche

Das Programm bietet eine intuitive, tabellenbasierte Benutzeroberfläche:

### 1. Laufwerksübersicht (Haupttabelle)
- **Spalte 1**: Aktueller Buchstabe (z.B. C:, D:, E:)
- **Spalte 2**: Laufwerksbezeichnung (z.B. System, Daten, Backup)
- **Spalte 3**: Neuer Buchstabe (Dropdown-Menü zum Auswählen)

### 2. Bedienung
- **Klicken Sie in die Spalte "Neuer Buchstabe"** um ein Dropdown-Menü zu öffnen
- **Wählen Sie den gewünschten neuen Buchstaben** aus der Liste
- **Mehrere Änderungen möglich**: Sie können mehrere Laufwerke gleichzeitig ändern
- **Button wird automatisch aktiviert** sobald Änderungen ausgewählt wurden

### 3. Steuerungsbereich
- **"Ausgewählte Änderungen durchführen"**: Führt alle markierten Änderungen durch
- **"Aktualisieren"**: Lädt die Laufwerksliste neu
- **"Beenden"**: Schließt das Programm

### 4. Anweisungen
Das Programm zeigt klare Anweisungen zur Bedienung direkt in der Oberfläche.

## ⚠️ Wichtige Hinweise

### Administratorrechte
- Das Programm **muss als Administrator** gestartet werden
- Ohne Admin-Rechte können keine Laufwerksbuchstaben geändert werden
- Das Programm warnt Sie, falls Admin-Rechte fehlen

### Sicherheit
- Das Programm verwendet nur native Windows-Tools (diskpart, wmic)
- Keine Manipulation von Registry oder kritischen Systemdateien
- Alle Änderungen werden über offizielle Windows-APIs durchgeführt

### Einschränkungen
- A: und B: sind normalerweise für Diskettenlaufwerke reserviert
- Systemlaufwerke (meist C:) sollten mit Vorsicht geändert werden
- Laufwerke, die gerade verwendet werden, können möglicherweise nicht geändert werden

## 🐛 Fehlerbehebung

### "Administratorrechte erforderlich"
**Lösung**: Starten Sie das Programm als Administrator
- Rechtsklick auf die .exe → "Als Administrator ausführen"

### "Fehler beim Ermitteln der Laufwerke"
**Lösung**: 
- Stellen Sie sicher, dass Windows Management Instrumentation (WMI) funktioniert
- Starten Sie das Programm neu
- Prüfen Sie, ob alle Laufwerke ordnungsgemäß angeschlossen sind

### "Fehler beim Ändern des Laufwerksbuchstabens"
**Mögliche Ursachen**:
- Laufwerk wird gerade verwendet (schließen Sie alle Programme, die darauf zugreifen)
- Neuer Buchstabe ist bereits vergeben
- Systemlaufwerk kann nicht geändert werden

## 📁 Projektstruktur

```
DriveLetterManager/
├── drive_letter_manager.py    # Hauptprogramm
├── requirements.txt           # Python-Abhängigkeiten
├── build.bat                 # Build-Skript (mit Icon)
├── build_simple.bat          # Einfaches Build-Skript
├── README.md                 # Diese Dokumentation
└── dist/                     # Kompilierte .exe (nach Build)
    └── DriveLetterManager.exe
```

## 🔄 Entwicklung

### Code-Struktur
- **DriveLetterManager**: Hauptklasse mit GUI und Logik
- **get_drives()**: Ermittelt Laufwerke über wmic
- **change_drive_letter()**: Ändert Buchstaben über diskpart
- **setup_gui()**: Erstellt die Tkinter-Benutzeroberfläche

### Erweiterungen
Das Programm kann einfach erweitert werden:
- Mehrsprachigkeit (Deutsch/Englisch)
- Laufwerks-Icons
- Erweiterte Laufwerksinformationen
- Batch-Änderungen

## 📄 Lizenz

MIT License - Siehe LICENSE-Datei für Details

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

## 📞 Support

Bei Problemen oder Fragen:
- Erstellen Sie ein Issue im Repository
- Beschreiben Sie das Problem detailliert
- Geben Sie Ihre Windows-Version an
