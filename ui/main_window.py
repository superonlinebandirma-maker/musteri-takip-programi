from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QLabel, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.customers import CustomersWidget
from ui.sales import SalesWidget
from ui.communications import CommunicationsWidget
from ui.tasks import TasksWidget
from ui.reports import ReportsWidget


class MainWindow(QMainWindow):
    """Ana pencere"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri Takip Programı (CRM)")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_stylesheet())
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("Müşteri Takip ve İlişki Yönetim Sistemi")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("padding: 10px; background-color: #2c3e50; color: white;")
        layout.addWidget(title_label)
        
        self.tabs = QTabWidget()
        
        self.customers_widget = CustomersWidget()
        self.sales_widget = SalesWidget(self.customers_widget.db)
        self.communications_widget = CommunicationsWidget(self.customers_widget.db)
        self.tasks_widget = TasksWidget(self.customers_widget.db)
        self.reports_widget = ReportsWidget(self.customers_widget.db)
        
        self.tabs.addTab(self.customers_widget, "👥 Müşteriler")
        self.tabs.addTab(self.sales_widget, "💰 Satışlar")
        self.tabs.addTab(self.communications_widget, "📞 İletişim")
        self.tabs.addTab(self.tasks_widget, "✅ Görevler")
        self.tabs.addTab(self.reports_widget, "📊 Raporlar")
        
        layout.addWidget(self.tabs)
        
        self.statusBar().showMessage("Hoşgeldiniz!")
        
        self.show()
    
    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #ecf0f1;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
            }
            QTabBar::tab {
                background-color: #95a5a6;
                color: white;
                padding: 8px 20px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1e5f8f;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: none;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #bdc3c7;
                padding: 5px;
                border-radius: 4px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
        """
