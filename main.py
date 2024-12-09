import os, time, random
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

global running

class onFileDownloadEvent(FileSystemEventHandler):

    def __init__(self):
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.init_folders = ["Ejecutables", "Documentos", "Imagenes", "Comprimidos"]
        self.file_types = {
            "Ejecutables": ["exe", "msi", "apk", "bat", "bin", "cmd", "com", "gadget", "jar", "wsf"],
            "Documentos": ["doc", "docx", "odt", "pdf", "xls", "xlsx", "ods", "ppt", "pptx", "txt", "rtf", "txt"],
            "Imagenes": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "tiff"],
            "Comprimidos": ["zip", "rar", "tar", "tar.gz", "7z", "dmg", "iso"]
        }
        self.file_type = None
        self.file_name = None
        self.ordered_directory = None

    def create_tree_structure(self):
        OS_DOWNLOAD_DIR_LIST = os.listdir(self.download_path)
        for folder in self.init_folders:
            if folder not in OS_DOWNLOAD_DIR_LIST:
                os.mkdir(os.path.join(self.download_path, folder))

    def is_file_blocked(self, file_path):
        try:
            with open(file_path, "r") as file:
                pass
            return False
        except IOError:
            return True

    def on_created(self, event):
        self.create_tree_structure()
        self.file_type = event.src_path.split(".")[-1]
        self.file_name = event.src_path.split("\\")[-1]
        self.ordered_directory = None

        for folder, file_types in self.file_types.items():
            if self.file_type in file_types:
                self.ordered_directory = os.path.join(self.download_path, folder)

        if not self.ordered_directory:
            return
        
        print(f"File {self.file_name} of type {self.file_type} has been downloaded")
        
        # Checking if file is in use by another process
        while self.is_file_blocked(event.src_path):
            time.sleep(0.1)

        try:
            os.rename(event.src_path, self.ordered_directory + "\\" + self.file_name)
        except FileExistsError as e:
            new_file_name = f"Copy_{random.randint(0, 999999)}_{self.file_name}"
            os.rename(event.src_path, self.ordered_directory + "\\" + new_file_name)

def main():
    running = True
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    event_handler = onFileDownloadEvent()
    observer = Observer()
    observer.schedule(event_handler, download_path, recursive=True)
    observer.start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        running = False

    observer.join()
        
if __name__ == "__main__":
    main()