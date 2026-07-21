import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    """Ana program"""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
