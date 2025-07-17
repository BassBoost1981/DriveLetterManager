# Drive Letter Manager

A portable Windows application for easy management of drive letters. Perfect for situations where drive letters don't match after a Windows reinstallation.

## 🚀 Features

- **Portable**: Runs directly from an .exe file without installation
- **Simple**: Intuitive graphical user interface
- **Safe**: Uses native Windows tools (diskpart)
- **Compatible**: Works from Windows 7 onwards
- **Clear**: Shows all drives with their labels
- **User-friendly**: Dropdown menus for easy selection
- **Bilingual**: German and English interface

## 📋 System Requirements

- Windows 7 or higher
- Administrator rights (for drive letter changes)
- No additional dependencies required

## 🔧 Installation and Usage

### Option 1: Use the ready-made .exe
1. Download `DriveLetterManager.exe` from the [Releases](https://github.com/BassBoost1981/DriveLetterManager/releases) page
2. Start the file **as Administrator** (Right-click → "Run as administrator")
3. The program displays all available drives in a clear table
4. **Click in the "New Letter" column** for the desired drive
5. **Select the new letter from the dropdown menu**
6. **Repeat this** for additional drives (batch changes possible)
7. Click **"Apply Changes"**

### Option 2: Compile from source code

#### Prerequisites
- Python 3.7 or higher
- pip (Python Package Installer)

#### Steps
1. Clone or download the repository
2. Open a command prompt in the project folder
3. Run the build script:
   ```batch
   build_simple.bat
   ```
4. Find the finished .exe in the `dist` folder

#### Manual compilation
```batch
# Install PyInstaller
pip install pyinstaller

# Create .exe
pyinstaller --onefile --windowed --name "DriveLetterManager" drive_letter_manager.py
```

## 🖥️ User Interface

The program offers an intuitive, table-based user interface:

### 1. Drive Overview (Main Table)
- **Column 1**: Current letter (e.g., C:, D:, E:)
- **Column 2**: Drive label (e.g., System, Data, Backup)
- **Column 3**: New letter (dropdown menu for selection)

### 2. Operation
- **Click in the "New Letter" column** to open a dropdown menu
- **Select the desired new letter** from the list
- **Multiple changes possible**: You can change multiple drives simultaneously
- **Button automatically activated** as soon as changes are selected

### 3. Control Area
- **"Apply Changes"**: Executes all marked changes
- **"Refresh"**: Reloads the drive list
- **"Exit"**: Closes the program

### 4. Instructions
The program shows clear operating instructions directly in the interface.

## ⚠️ Important Notes

### Administrator Rights
- The program **must be started as Administrator**
- Without admin rights, no drive letters can be changed
- The program warns you if admin rights are missing

### Security
- The program only uses native Windows tools (diskpart, wmic)
- No manipulation of registry or critical system files
- All changes are made through official Windows APIs

### Limitations
- A: and B: are normally reserved for floppy drives
- System drives (usually C:) should be changed with caution
- Drives currently in use may not be changeable

## 🐛 Troubleshooting

### "Administrator rights required"
**Solution**: Start the program as Administrator
- Right-click on the .exe → "Run as administrator"

### "Error determining drives"
**Solution**:
- Ensure Windows Management Instrumentation (WMI) is working
- Restart the program
- Check if all drives are properly connected

### "Error changing drive letter"
**Possible causes**:
- Drive is currently in use (close all programs accessing it)
- New letter is already assigned
- System drive cannot be changed

## 📁 Project Structure

```
DriveLetterManager/
├── drive_letter_manager.py    # Main program
├── requirements.txt           # Python dependencies
├── build.bat                 # Build script (with icon)
├── build_simple.bat          # Simple build script
├── README.md                 # This documentation
└── dist/                     # Compiled .exe (after build)
    └── DriveLetterManager.exe
```

## 🔄 Development

### Code Structure
- **DriveLetterManager**: Main class with GUI and logic
- **get_drives()**: Determines drives via wmic
- **change_drive_letter()**: Changes letters via diskpart
- **setup_gui()**: Creates the Tkinter user interface

### Extensions
The program can be easily extended:
- ✅ Multilingual support (German/English)
- Drive icons
- Extended drive information
- ✅ Batch changes

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Create a pull request

## 📞 Support

For problems or questions:
- Create an issue in the repository
- Describe the problem in detail
- Provide your Windows version
