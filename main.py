import os
import logging
import sys

from pathlib import Path

from PySide6.QtGui     import *
from PySide6.QtCore    import *
from PySide6.QtWidgets import *

from ui.design import Ui_MainWindow




# key names will be folder names! Ключи с названием папок
extensions = {

    'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 
              'h264', 'flv', 'rm', 'swf', 'vob'],

    'data': ['sql', 'sqlite', 'sqlite3', 'csv', 'dat', 'db', 'log', 'mdb', 'sav', 
             'tar', 'xml'],

    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl',
              'cda'],

    'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 
              'tiff'],

    'archive': ['zip', 'rar', '7z', 'z', 'gz', 'rpm', 'arj', 'pkg', 'deb'],

    'text': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],

    '3d': ['stl', 'obj', 'fbx', 'dae', '3ds', 'iges', 'step'],

    'presentation': ['pptx', 'ppt', 'pps', 'key', 'odp'],

    'spreadsheet': ['xlsx', 'xls', 'xlsm', 'ods'],

    'font': ['otf', 'ttf', 'fon', 'fnt'],

    'gif': ['gif'],

    'exe': ['exe', 'msi'],

    'bat': ['bat'],

    'apk': ['apk'],
    
    'torrent': ['torrent']
}

#Класс 
class Folder():  
    # also creates folders from dictionary keys
    @staticmethod
    def create_folders_from_list(folder_path, folder_names):
        for folder in folder_names:
            if not os.path.exists(f'{folder_path}\\{folder}'):
                os.mkdir(f'{folder_path}\\{folder}')

    def get_subfolder_paths(self, folder_path) -> list:
        subfolder_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]
        
        return subfolder_paths

    def get_subfolder_names(self, folder_path) -> list:
        subfolder_paths = self.get_subfolder_paths(folder_path)
        subfolder_names = [f.split('\\')[-1] for f in subfolder_paths]
        
        return subfolder_names

    def get_file_paths(self, folder_path) -> list:
        file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
        
        return file_paths

    def get_file_names(self, folder_path) -> list:
        file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
        file_names = [f.split('\\')[-1] for f in file_paths]
        
        return file_names

    def sort_files(self, folder_path):
        global extensions
        file_paths = self.get_file_paths(folder_path)
        ext_list = list(extensions.items())
        
        for file_path in file_paths:
            extensions = file_path.split('.')[-1]
            file_name = file_path.split('\\')[-1]
            
            for dict_key_int in range(len(ext_list)):
                if extensions in ext_list[dict_key_int][1]:
                    print(f'Moving {file_name} in {ext_list[dict_key_int][0]} folder\n')
                    os.rename(file_path, f'{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}')
                    logging.info(f'Moving {file_name} in {ext_list[dict_key_int][0]} folder\n')

    def remove_empty_folders(self, folder_path):
        subfolder_paths = self.get_subfolder_paths(folder_path)
        
        for p in subfolder_paths:
            if not os.listdir(p):
                print('Deleting empty folder:', p.split('\\')[-1], '\n')
                os.rmdir(p)

#Класс окна
class Form(QMainWindow):
    def __init__(self):
        super(Form, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.entry = self.ui.btn_folder
        self.path_folder = self.ui.path_folder

        #digits
        self.entry.clicked.connect(self.get_directory)
        self.ui.btn_start.clicked.connect(self.get_start)
        
        
    def get_directory(self):                                                     # <-----
        dirlist = QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
        self.path_folder.setText(dirlist)
        global main_path
        main_path = dirlist
        return main_path

    def get_start(self):
        #text = self.path_folder.toRawText()
        main()
        self.ui.done.setText('Done')

def main() -> None:
    folder = Folder()
    folder.create_folders_from_list(main_path, extensions)
    folder.sort_files(main_path)
    folder.remove_empty_folders(main_path)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Form()
    window.show()

    sys.exit(app.exec())
    


    
