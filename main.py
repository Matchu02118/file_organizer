from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import sys
from pathlib import Path
import os, shutil
import datetime
import resources

fmtc = {
    "Executables": (".exe", ".msi", ".sh", ".bat", ".apk"),
    "Documents": (".docx", ".doc", ".pdf", ".txt", ".odt"),
    "Records": (".xlsx", ".xls", ".csv"),
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"),
    "Audio": (".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"),
    "Videos": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"),
    "Archives": (".zip", ".rar", ".tar", ".gz", ".7z"),
    "Code": (".py", ".java", ".cpp", ".c", ".js", ".ts", ".html", ".css", ".rb", ".php", ".go", ".rs"),
}

button_category_map = {
"fmtc": "Executables",
"fmtc_2": "Documents",
"fmtc_3": "Records",
"fmtc_4": "Images",
"fmtc_5": "Audio",
"fmtc_6": "Videos",
"fmtc_7": "Archives",
"fmtc_8": "Code",
}

def message(parent, title, text):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Information)

    msg.setStyleSheet("""
        QMessageBox {
            background-color:white;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #777777;
        }
    """)

    msg.exec()

def filterMessage(parent, title, text):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Information)

    msg.setStyleSheet("""
        QMessageBox {
            background-color:white;
            color: white;
            font-size: 10x;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #777777;
        }
    """)

    msg.exec()

def warning(parent, title, text):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Warning)

    msg.setStyleSheet("""
        QMessageBox {
            background-color:white;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton {
            background-color: #555555;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #777777;
        }
    """)

    msg.exec()

def get_category(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in fmtc.items():
        if ext in extensions:
            return category
    return "Others" 

def resource_path(relative_path: str) -> str:
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon(resource_path("projectIcon.ico")))
    window.show()
    sys.exit(app.exec())
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("ui/window.ui"), self)
        
        self.option1.clicked.connect(self.option_one)
        self.option2.clicked.connect(self.option_two)
    
    def option_one(self):
        dialog = OptionOne()
        dialog.exec()

    def option_two(self):
        dialog = OptionTwo()
        dialog.exec()

class OptionOne(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("ui/option1.ui"), self)
        self.setWindowTitle("General File Organizer")
        self.setWindowIcon(QIcon(resource_path("projectIcon.ico")))
        self.filtered_formats = []
        
        self.dirSlct.clicked.connect(self.select_wd)

        for btnName in button_category_map.keys():
            getattr(self, btnName).clicked.connect(self.filter_fileFormats)
        
        self.btn1.clicked.connect(self.organize)
        
    def select_wd(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Target Folder",
            ""
        )
        
        if folder:
            self.dir.setText(folder)
    
    def filter_fileFormats(self):
        btn = self.sender()
        btn_name = btn.objectName()
        c = button_category_map[btn_name]
    
        if btn.isChecked():
            self.filtered_formats.extend(fmtc[c])
            message(self, f"Filter {c}", f"The organizer app will now ignore {c} type files.\n"
            f"Files that end with {fmtc[c]} are now going to be excluded.")
            
        else:
            message(self,
            f"Include {c}",
            f"The organizer app will now include {c} type files.\n"
            f"Files that end with {fmtc[c]} are now going to be included "
            f"during the file organization process.")
    
        if self.fmtc_8.isChecked():
            self.fmtc_8.setText("")
        else:
            self.fmtc_8.setText("Code")
        
    def organize(self):
        targetDir = self.dir.text().strip()
        if not targetDir:
            message(self, "Missing Directory", "Please select a target directory before proceeding.")
            return
        
        path = Path(targetDir)
        
        if not path.exists():
            warning(self, "Invalid Directory", f"The path '{targetDir}' does not exist.")
            return

        if not path.is_dir():
            warning(self, "Invalid Input", f"'{targetDir}' is not a directory.")
            return
        
        outname = self.outputName.text().strip()
        if not outname:
            outname = f"MyOrganizedFiles-{datetime.datetime.today().strftime("%m-%d-%Y")}"
        
        base_destination = path / outname
        base_destination.mkdir(exist_ok=True)
        
        for file in os.listdir(path):
            file_path = path / file
            if not file_path.is_file():
                continue

            _, ext = os.path.splitext(file)
            if ext.lower() in self.filtered_formats:
                continue

            category = get_category(file)
            category_folder = base_destination / category
            category_folder.mkdir(exist_ok=True)

            dest_file = category_folder / file

            if dest_file.exists():
                base, ext = os.path.splitext(file)
                counter = 1
                while (category_folder / f"{base}_{counter}{ext}").exists():
                    counter += 1
                dest_file = category_folder / f"{base}_{counter}{ext}"

            shutil.move(str(file_path), dest_file)
            
        message(self, "Success!", f"Files are organized in the {outname} folder.")
        
class OptionTwo(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("ui/option2.ui"), self)
        self.setWindowIcon(QIcon(resource_path("projectIcon.ico")))
        self.setWindowTitle("Name-Based File Organizer")
        
        self.dirSlct.clicked.connect(self.select_wd)
        self.btn1.clicked.connect(self.organize)
        
        self.fname.textChanged.connect(self.previewOutput)
        self.lname.textChanged.connect(self.previewOutput)
        
    def select_wd(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Target Folder", "")
        
        if folder:
            self.dir.setText(folder)
    
    def organize(self):
        dir_text = self.dir.text().strip()
        if not dir_text:
            QtWidgets.QMessageBox.warning(self, "No Folder Selected", "Please select a target folder first.")
            return
        dir_path = Path(dir_text)
        
        if not dir_path.exists():
            warning(self, "Invalid Directory", f"Target path {dir_path} does not exist.")
            return
        
        if not dir_path.is_dir():
            warning(self, "Not a directory", f"Target path {dir_path} is not a directory.")
            return

        first_name = self.fname.text().strip()
        last_name = self.lname.text().strip()

        if not (first_name or last_name):
            QMessageBox.warning(self, "Missing Names", "Please enter at least first or last name.")
            return

        first_name_parts = first_name.lower().split()
        last_name_lower = last_name.lower()

        folder_name = f"{last_name}, {first_name}"
        base_dest_dir = dir_path / folder_name
        base_dest_dir.mkdir(exist_ok=True)

        moved_files = 0

        for file in os.listdir(dir_path):
            file_path = dir_path / file
            if not file_path.is_file():
                continue

            file_lower = file.lower()
            first_name_match = all(part in file_lower for part in first_name_parts) if first_name_parts else True
            last_name_match = last_name_lower in file_lower if last_name_lower else True

            if first_name_match and last_name_match:
                category = get_category(file)
                if category:
                    category_folder = base_dest_dir / category
                    category_folder.mkdir(exist_ok=True)

                    dest_file = category_folder / file
                    if dest_file.exists():
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while (category_folder / f"{base}_{counter}{ext}").exists():
                            counter += 1
                        dest_file = category_folder / f"{base}_{counter}{ext}"

                    shutil.move(str(file_path), dest_file)
                    moved_files += 1
        
        message(self,
            "Organizing Complete",
            f"{moved_files} files organized in:\n{base_dest_dir}"
            )
    
    def previewOutput(self):
        first_name = self.fname.text().strip()
        last_name = self.lname.text().strip()

        folder_name = f"{last_name}, {first_name}"
        folder_name = folder_name.strip(", .")
        self.dirName.setText(folder_name)
        
main()