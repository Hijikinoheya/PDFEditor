import sys
from PyQt5.QtWidgets import QApplication
from loading_screen import LoadingScreen
from main_window import PDFEditorApp

def main():
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    main_window = PDFEditorApp()
    loading_screen.finish(main_window)
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()