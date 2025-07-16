#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drive Letter Manager - Portable Windows Tool
============================================

Ein portables Windows-Programm zur einfachen Verwaltung von Laufwerksbuchstaben.
Verwendet native Windows-Tools (diskpart) über subprocess für maximale Kompatibilität.

Autor: Drive Letter Manager
Version: 1.0
Lizenz: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import ctypes
import os
import string
import json
from typing import Dict, List


class DriveLetterManager:
    """Hauptklasse für den Drive Letter Manager."""

    def __init__(self):
        """Initialisiert den Drive Letter Manager."""
        self.root = tk.Tk()
        self.drives_data = {}
        self.drive_widgets = []
        self.current_language = "de"  # Standard: Deutsch
        self.setup_translations()  # Initialisiere Widget-Liste
        self.drives_canvas = None  # Initialisiere Canvas-Referenz
        self.drives_frame = None  # Initialisiere Frame-Referenz
        self.setup_gui()

        # Prüfe Admin-Rechte beim Start
        if not self.is_admin():
            messagebox.showwarning(
                self.t("admin_required_title"),
                self.t("admin_required_message")
            )

    def setup_translations(self):
        """Initialisiert die Übersetzungen für Deutsch und Englisch."""
        self.translations = {
            "de": {
                "title": "Laufwerksbuchstaben ändern",
                "current_drives": "Aktuelle Laufwerke:",
                "drive": "Laufwerk",
                "description": "Bezeichnung",
                "new_letter": "Neuer Buchstabe",
                "instructions": "Anweisungen",
                "instruction_text": (
                    "• Verwenden Sie die Dropdown-Menüs in der Spalte 'Neuer Buchstabe'\n"
                    "• Wählen Sie für jedes Laufwerk den gewünschten neuen Buchstaben\n"
                    "• Klicken Sie auf 'Änderungen durchführen' um alle Änderungen zu übernehmen\n"
                    "• Administratorrechte sind für Änderungen erforderlich"
                ),
                "apply_changes": "Änderungen durchführen",
                "refresh": "Aktualisieren",
                "exit": "Beenden",
                "language": "Sprache",
                "admin_required_title": "Administratorrechte erforderlich",
                "admin_required_message": (
                    "Dieses Programm benötigt Administratorrechte für Änderungen an Laufwerksbuchstaben.\n\n"
                    "Starten Sie das Programm als Administrator neu."
                ),
                "no_changes": "Keine Änderungen",
                "no_changes_message": "Es wurden keine Änderungen an den Laufwerksbuchstaben vorgenommen.",
                "confirm_changes": "Änderungen bestätigen",
                "changes_summary": "Folgende Änderungen werden durchgeführt:",
                "success": "Erfolgreich",
                "changes_applied": "Alle Änderungen wurden erfolgreich angewendet!",
                "error": "Fehler",
                "error_occurred": "Ein Fehler ist aufgetreten:",
                "drives_updated": "Laufwerke aktualisiert"
            },
            "en": {
                "title": "Change Drive Letters",
                "current_drives": "Current Drives:",
                "drive": "Drive",
                "description": "Description",
                "new_letter": "New Letter",
                "instructions": "Instructions",
                "instruction_text": (
                    "• Use the dropdown menus in the 'New Letter' column\n"
                    "• Select the desired new letter for each drive\n"
                    "• Click 'Apply Changes' to apply all changes\n"
                    "• Administrator rights are required for changes"
                ),
                "apply_changes": "Apply Changes",
                "refresh": "Refresh",
                "exit": "Exit",
                "language": "Language",
                "admin_required_title": "Administrator Rights Required",
                "admin_required_message": (
                    "This program requires administrator rights to change drive letters.\n\n"
                    "Please restart the program as administrator."
                ),
                "no_changes": "No Changes",
                "no_changes_message": "No changes were made to drive letters.",
                "confirm_changes": "Confirm Changes",
                "changes_summary": "The following changes will be applied:",
                "success": "Success",
                "changes_applied": "All changes have been applied successfully!",
                "error": "Error",
                "error_occurred": "An error occurred:",
                "drives_updated": "Drives updated"
            }
        }

    def t(self, key: str) -> str:
        """Übersetzt einen Text-Schlüssel in die aktuelle Sprache."""
        return self.translations.get(self.current_language, {}).get(key, key)

    def switch_language(self):
        """Wechselt zwischen Deutsch und Englisch."""
        self.current_language = "en" if self.current_language == "de" else "de"
        self.update_ui_language()

    def update_ui_language(self):
        """Aktualisiert alle UI-Texte in der neuen Sprache."""
        self.root.title(self.t("title"))
        # UI wird komplett neu aufgebaut
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_gui()
        self.refresh_drives()

    def is_admin(self) -> bool:
        """
        Prüft, ob das Programm mit Administratorrechten läuft.
        
        Returns:
            bool: True wenn Admin-Rechte vorhanden, False sonst
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def get_drives(self) -> Dict[str, str]:
        """
        Ermittelt alle verfügbaren Laufwerke und deren Bezeichnungen.

        Returns:
            Dict[str, str]: Dictionary mit Laufwerksbuchstaben als Key und Bezeichnung als Value
        """
        drives = {}

        try:
            # Versuche zuerst PowerShell (moderne Methode)
            result = subprocess.run([
                'powershell', '-Command',
                'Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, VolumeName | ConvertTo-Csv -NoTypeInformation'
            ], capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Erste Zeile ist Header
                    if line.strip() and ',' in line:
                        # CSV-Format: "DeviceID","VolumeName"
                        parts = line.replace('"', '').split(',')
                        if len(parts) >= 2:
                            device_id = parts[0].strip()  # z.B. "C:"
                            volume_name = parts[1].strip() if parts[1].strip() else "Lokaler Datenträger"

                            if device_id and ':' in device_id:
                                drives[device_id] = volume_name
            else:
                # Fallback zu wmic (falls PowerShell fehlschlägt)
                result = subprocess.run([
                    'wmic', 'logicaldisk', 'get', 'size,freespace,caption,volumename'
                ], capture_output=True, text=True, shell=True, timeout=10)

                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:  # Erste Zeile ist Header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3:
                                caption = parts[0]  # z.B. "C:"
                                if len(parts) > 3:
                                    volume_name = ' '.join(parts[3:])
                                else:
                                    volume_name = "Lokaler Datenträger"

                                if caption and ':' in caption:
                                    drives[caption] = volume_name
                else:
                    # Letzter Fallback: Einfache Laufwerkserkennung
                    for letter in string.ascii_uppercase:
                        drive_path = f"{letter}:\\"
                        if os.path.exists(drive_path):
                            drives[f"{letter}:"] = "Lokaler Datenträger"

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Ermitteln der Laufwerke: {str(e)}")

        return drives
    
    def get_available_letters(self) -> List[str]:
        """
        Ermittelt alle verfügbaren Laufwerksbuchstaben (A-Z).
        
        Returns:
            List[str]: Liste der verfügbaren Buchstaben
        """
        used_letters = set(drive[0].upper() for drive in self.drives_data.keys())
        all_letters = set(chr(i) for i in range(ord('A'), ord('Z') + 1))
        # Entferne A: und B: (normalerweise für Disketten reserviert)
        all_letters.discard('A')
        all_letters.discard('B')
        available = sorted(list(all_letters - used_letters))
        return [f"{letter}:" for letter in available]
    
    def change_drive_letter(self, old_letter: str, new_letter: str) -> bool:
        """
        Ändert einen Laufwerksbuchstaben mittels diskpart.

        Args:
            old_letter (str): Aktueller Laufwerksbuchstabe (z.B. "D:")
            new_letter (str): Neuer Laufwerksbuchstabe (z.B. "E:")

        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if not self.is_admin():
            messagebox.showerror(
                "Administratorrechte erforderlich",
                "Dieses Programm benötigt Administratorrechte, um Laufwerksbuchstaben zu ändern.\n\n"
                "Bitte starten Sie das Programm als Administrator."
            )
            return False

        # Validierung der Eingaben
        if not old_letter or not new_letter:
            messagebox.showerror("Ungültige Eingabe", "Laufwerksbuchstaben dürfen nicht leer sein.")
            return False

        if old_letter == new_letter:
            messagebox.showwarning("Gleiche Buchstaben", "Alter und neuer Laufwerksbuchstabe sind identisch.")
            return False

        # Prüfe ob neuer Buchstabe bereits verwendet wird
        if new_letter in self.drives_data:
            messagebox.showerror(
                "Buchstabe bereits vergeben",
                f"Der Laufwerksbuchstabe {new_letter} wird bereits verwendet."
            )
            return False

        try:
            # Erstelle diskpart-Skript mit verbesserter Fehlerbehandlung
            diskpart_script = f"""select volume {old_letter[0]}
assign letter={new_letter[0]}
exit"""

            # Führe diskpart aus
            process = subprocess.Popen(
                ['diskpart'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW  # Verstecke Konsole
            )

            stdout, stderr = process.communicate(input=diskpart_script, timeout=30)

            # Analysiere die Ausgabe für bessere Fehlermeldungen
            if process.returncode == 0:
                # Prüfe ob die Änderung wirklich erfolgreich war
                if "successfully" in stdout.lower() or "erfolgreich" in stdout.lower():
                    messagebox.showinfo(
                        "Erfolg",
                        f"Laufwerksbuchstabe erfolgreich von {old_letter} zu {new_letter} geändert!\n\n"
                        f"Die Änderung wird nach einer kurzen Aktualisierung sichtbar."
                    )
                    return True
                else:
                    # Diskpart lief ohne Fehler, aber möglicherweise ohne Erfolg
                    messagebox.showwarning(
                        "Unklarer Status",
                        f"Diskpart wurde ausgeführt, aber der Status ist unklar.\n\n"
                        f"Bitte prüfen Sie manuell, ob die Änderung erfolgreich war.\n\n"
                        f"Ausgabe: {stdout}"
                    )
                    return True
            else:
                # Analysiere spezifische Fehlermeldungen
                error_msg = stderr.strip() if stderr.strip() else stdout.strip()

                if "access denied" in error_msg.lower() or "zugriff verweigert" in error_msg.lower():
                    messagebox.showerror(
                        "Zugriff verweigert",
                        "Zugriff verweigert. Mögliche Ursachen:\n"
                        "• Das Laufwerk wird gerade verwendet\n"
                        "• Unzureichende Berechtigungen\n"
                        "• Systemlaufwerk kann nicht geändert werden\n\n"
                        "Schließen Sie alle Programme, die auf das Laufwerk zugreifen."
                    )
                elif "not found" in error_msg.lower() or "nicht gefunden" in error_msg.lower():
                    messagebox.showerror(
                        "Laufwerk nicht gefunden",
                        f"Das Laufwerk {old_letter} wurde nicht gefunden.\n\n"
                        "Aktualisieren Sie die Laufwerksliste und versuchen Sie es erneut."
                    )
                elif "already assigned" in error_msg.lower() or "bereits zugewiesen" in error_msg.lower():
                    messagebox.showerror(
                        "Buchstabe bereits vergeben",
                        f"Der Laufwerksbuchstabe {new_letter} ist bereits vergeben.\n\n"
                        "Wählen Sie einen anderen Buchstaben."
                    )
                else:
                    messagebox.showerror(
                        "Diskpart-Fehler",
                        f"Fehler beim Ändern des Laufwerksbuchstabens:\n\n{error_msg}"
                    )
                return False

        except subprocess.TimeoutExpired:
            messagebox.showerror(
                "Timeout",
                "Die Operation hat zu lange gedauert und wurde abgebrochen.\n\n"
                "Versuchen Sie es erneut oder starten Sie das System neu."
            )
            return False
        except FileNotFoundError:
            messagebox.showerror(
                "Diskpart nicht gefunden",
                "Das Windows-Tool 'diskpart' wurde nicht gefunden.\n\n"
                "Stellen Sie sicher, dass Sie Windows verwenden."
            )
            return False
        except Exception as e:
            messagebox.showerror(
                "Unerwarteter Fehler",
                f"Ein unerwarteter Fehler ist aufgetreten:\n\n{str(e)}\n\n"
                "Versuchen Sie es erneut oder starten Sie das Programm neu."
            )
            return False
    
    def setup_gui(self):
        """Erstellt die grafische Benutzeroberfläche."""
        self.root.title(self.t("title"))
        # Fenstergrößen werden nach dem Laden der Laufwerke angepasst
        self.root.resizable(True, True)
        
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfiguriere Grid-Gewichtung
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Sprachauswahl
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(lang_frame, text=self.t("language") + ":").grid(row=0, column=0, sticky=tk.W)
        lang_button = ttk.Button(lang_frame, text="English" if self.current_language == "de" else "Deutsch",
                                command=self.switch_language, width=10)
        lang_button.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)

        # Titel
        title_label = ttk.Label(main_frame, text=self.t("current_drives"), font=("Arial", 12, "bold"))
        title_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 10))
        
        # Laufwerks-Tabelle
        self.create_drives_table(main_frame)
        
        # Anweisungen
        self.create_instructions(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)

        # Lade Laufwerke und passe Fenstergröße an
        self.refresh_drives()

    def adjust_window_size(self):
        """Passt die Fenstergröße an die Anzahl der Laufwerke an."""
        if not hasattr(self, 'drives_data') or not self.drives_data:
            # Fallback wenn noch keine Laufwerke geladen
            self.root.geometry("750x500")
            return

        num_drives = len(self.drives_data)
        print(f"Adjusting window size for {num_drives} drives")

        # Basis-Höhe für UI-Elemente (Sprache, Titel, Anweisungen, Buttons)
        base_height = 380

        # Höhe pro Laufwerk (ca. 35px pro Zeile)
        drive_height = 35

        # Berechne Gesamthöhe
        total_height = base_height + (num_drives * drive_height)

        # Mindest- und Maximalhöhe
        min_height = 550
        max_height = 800

        # Begrenze die Höhe
        window_height = max(min_height, min(max_height, total_height))

        # Feste Breite
        window_width = 750

        print(f"Setting window size to {window_width}x{window_height}")
        self.root.geometry(f"{window_width}x{window_height}")

        # Canvas-Höhe anpassen
        if hasattr(self, 'canvas') and self.canvas:
            if total_height > max_height:
                # Scrolling erforderlich
                canvas_height = max_height - base_height
            else:
                # Alle Laufwerke passen ins Fenster
                canvas_height = num_drives * drive_height + 50

            print(f"Setting canvas height to {canvas_height}")
            self.canvas.configure(height=canvas_height)

        # GUI aktualisieren
        self.root.update_idletasks()

    def create_drives_table(self, parent):
        """Erstellt die Tabelle für die Laufwerksanzeige mit Dropdown-Spalte."""
        # Frame für Tabelle
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Hauptframe für Tabelle und Dropdowns
        content_frame = ttk.Frame(table_frame)
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=0, minsize=80)   # Laufwerk Spalte - breiter
        content_frame.columnconfigure(1, weight=0, minsize=350)  # Bezeichnung Spalte - breiter
        content_frame.columnconfigure(2, weight=0, minsize=200)  # Neuer Buchstabe Spalte
        content_frame.rowconfigure(0, weight=0)
        content_frame.rowconfigure(1, weight=1)

        # Header mit angepassten Breiten und Padding
        ttk.Label(content_frame, text=self.t("drive"), font=("Arial", 9, "bold"), width=10).grid(row=0, column=0, sticky=tk.W, padx=(5,10), pady=5)
        ttk.Label(content_frame, text=self.t("description"), font=("Arial", 9, "bold"), width=40).grid(row=0, column=1, sticky=tk.W, padx=(5,10), pady=5)
        ttk.Label(content_frame, text=self.t("new_letter"), font=("Arial", 9, "bold"), width=20).grid(row=0, column=2, sticky=tk.W, padx=(5,10), pady=5)

        # Scrollbarer Frame für Laufwerke
        self.canvas = tk.Canvas(content_frame, height=200)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.drives_frame = ttk.Frame(self.canvas)

        # Konfiguriere Spalten im drives_frame
        self.drives_frame.columnconfigure(0, weight=0, minsize=80)   # Laufwerk - breiter
        self.drives_frame.columnconfigure(1, weight=0, minsize=350)  # Bezeichnung - breiter
        self.drives_frame.columnconfigure(2, weight=0, minsize=200)  # Neuer Buchstabe

        self.drives_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.drives_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        self.drive_widgets = []
    
    def create_instructions(self, parent):
        """Erstellt den Bereich mit Anweisungen."""
        # Frame für Anweisungen
        info_frame = ttk.LabelFrame(parent, text=self.t("instructions"), padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        # Anweisungstext
        instruction_label = ttk.Label(info_frame, text=self.t("instruction_text"), justify=tk.LEFT)
        instruction_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def create_buttons(self, parent):
        """Erstellt die Buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))

        # Ändern Button
        self.change_button = ttk.Button(button_frame, text=self.t("apply_changes"),
                                       command=self.on_change_click)
        self.change_button.pack(side=tk.LEFT, padx=(0, 10))

        # Aktualisieren Button
        refresh_button = ttk.Button(button_frame, text=self.t("refresh"), command=self.refresh_drives)
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))

        # Beenden Button
        exit_button = ttk.Button(button_frame, text=self.t("exit"), command=self.root.quit)
        exit_button.pack(side=tk.RIGHT)
    


    def refresh_drives(self):
        """Aktualisiert die Laufwerksliste und erstellt neue Dropdown-Menüs."""
        # Laufwerke neu laden
        self.drives_data = self.get_drives()

        # Prüfe ob GUI-Komponenten existieren
        if not hasattr(self, 'drives_frame') or self.drives_frame is None:
            print("GUI noch nicht initialisiert, überspringe refresh_drives")
            return

        # Lösche alte Widgets sicher
        if hasattr(self, 'drive_widgets') and self.drive_widgets:
            for widget_row in self.drive_widgets:
                for widget in widget_row:
                    try:
                        if hasattr(widget, 'destroy'):
                            widget.destroy()
                    except tk.TclError:
                        # Widget bereits zerstört
                        pass
            self.drive_widgets.clear()

        # Erstelle neue Zeilen für jedes Laufwerk
        available_letters = self.get_available_letters()

        for i, (drive, label) in enumerate(sorted(self.drives_data.items())):
            try:
                # Laufwerk Label - breiter
                drive_label = ttk.Label(self.drives_frame, text=drive, width=8)
                drive_label.grid(row=i, column=0, padx=(5,10), pady=2, sticky=tk.W)

                # Bezeichnung Label - breiter für bessere Lesbarkeit
                display_label = label if len(label) <= 40 else label[:37] + "..."
                desc_label = ttk.Label(self.drives_frame, text=display_label, width=40)
                desc_label.grid(row=i, column=1, padx=(5,10), pady=2, sticky=tk.W)

                # Dropdown für neuen Buchstaben - mit kürzeren Werten
                new_drive_var = tk.StringVar()
                dropdown_values = available_letters + [drive]  # Aktueller Buchstabe auch verfügbar
                dropdown_values = sorted(list(set(dropdown_values)))  # Duplikate entfernen und sortieren

                # Kürze die Dropdown-Werte auf nur den Buchstaben
                short_dropdown_values = [letter.split(':')[0] + ':' for letter in dropdown_values]

                new_drive_combo = ttk.Combobox(self.drives_frame, textvariable=new_drive_var,
                                             values=short_dropdown_values, state="readonly", width=8)
                new_drive_combo.set(drive.split(':')[0] + ':')  # Nur Buchstabe mit Doppelpunkt
                new_drive_combo.grid(row=i, column=2, padx=(5,10), pady=2, sticky=tk.W+tk.E)

                # Speichere Widget-Referenzen
                widget_row = [drive_label, desc_label, new_drive_combo, new_drive_var, drive]
                self.drive_widgets.append(widget_row)

            except Exception as e:
                print(f"Fehler beim Erstellen von Laufwerk {drive}: {e}")
                continue

        # Canvas-Scroll-Region aktualisieren
        try:
            if self.drives_frame and self.drives_canvas:
                self.drives_frame.update_idletasks()
                self.drives_canvas.configure(scrollregion=self.drives_canvas.bbox("all"))
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Scroll-Region: {e}")

        drives_count = len(self.drives_data)
        update_msg = f"Drives updated: {drives_count} drives found" if self.current_language == "en" else f"Laufwerke aktualisiert: {drives_count} Laufwerke gefunden"
        print(update_msg)

        # Passe Fenstergröße an die Anzahl der Laufwerke an
        self.root.after(100, self.adjust_window_size)  # Verzögert ausführen nach GUI-Update
    
    def on_change_click(self):
        """Behandelt den Klick auf den Ändern-Button."""
        # Sammle alle geplanten Änderungen aus den Dropdown-Menüs
        changes = []

        for widget_row in self.drive_widgets:
            _, desc_label, _, var, original_drive = widget_row
            current_selection = var.get()

            # Vergleiche nur die Buchstaben (ohne Beschreibung)
            original_letter = original_drive.split(':')[0] + ':'
            selected_letter = current_selection

            if selected_letter != original_letter:
                drive_desc = desc_label.cget("text")
                changes.append((original_letter, selected_letter, drive_desc))

        if not changes:
            messagebox.showinfo(self.t("no_changes"), self.t("no_changes_message"))
            return

        # Zeige Zusammenfassung der Änderungen
        change_summary = self.t("changes_summary") + "\n\n"
        for current, new, label in changes:
            change_summary += f"• {current} → {new} ({label})\n"

        change_summary += f"\n{len(changes)} " + ("change" if len(changes) == 1 else "changes") + ". Continue?" if self.current_language == "en" else f"\nInsgesamt {len(changes)} Änderung(en). Fortfahren?"

        # Bestätigung
        if messagebox.askyesno(self.t("confirm_changes"), change_summary):
            successful_changes = 0

            for current, new, label in changes:
                if self.change_drive_letter(current, new):
                    successful_changes += 1
                else:
                    # Bei Fehler fragen ob fortfahren
                    if not messagebox.askyesno("Fehler aufgetreten",
                                             f"Fehler bei Änderung {current} → {new}.\n\n"
                                             f"Möchten Sie mit den verbleibenden Änderungen fortfahren?"):
                        break

            # Ergebnis anzeigen
            if successful_changes > 0:
                success_msg = f"{successful_changes} of {len(changes)} changes applied successfully." if self.current_language == "en" else f"{successful_changes} von {len(changes)} Änderungen erfolgreich durchgeführt."
                messagebox.showinfo(self.t("success"), success_msg)

            # Liste aktualisieren
            self.refresh_drives()
    
    def run(self):
        """Startet die Anwendung."""
        # Prüfe Admin-Rechte beim Start
        if not self.is_admin():
            messagebox.showwarning(
                "Administratorrechte empfohlen",
                "Für das Ändern von Laufwerksbuchstaben sind Administratorrechte erforderlich.\n\n"
                "Starten Sie das Programm als Administrator, um alle Funktionen nutzen zu können."
            )
        
        self.root.mainloop()


def main():
    """Hauptfunktion."""
    try:
        app = DriveLetterManager()
        app.run()
    except Exception as e:
        messagebox.showerror("Kritischer Fehler", f"Ein kritischer Fehler ist aufgetreten:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
