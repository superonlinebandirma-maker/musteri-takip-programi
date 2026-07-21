from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

from database import Database
from models import Sale


class SalesWidget(QWidget):
    """Satış yönetimi sekmesi"""
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_sales()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout()
        
        # Kontrol paneli
        control_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Yeni Satış")
        add_btn.clicked.connect(self.add_sale)
        
        edit_btn = QPushButton("✏️ Düzenle")
        edit_btn.clicked.connect(self.edit_sale)
        
        delete_btn = QPushButton("🗑️ Sil")
        delete_btn.clicked.connect(self.delete_sale)
        
        control_layout.addWidget(add_btn)
        control_layout.addWidget(edit_btn)
        control_layout.addWidget(delete_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
        # Satış tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Müşteri", "Ürün", "Miktar", "Durum", "Tarih", "Açıklama"])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_sales(self):
        """Satışları tablodan yükle"""
        all_sales = []
        customers = self.db.get_all_customers()
        
        for customer in customers:
            sales = self.db.get_customer_sales(customer.id)
            all_sales.extend(sales)
        
        self.table.setRowCount(len(all_sales))
        
        for row, sale in enumerate(all_sales):
            customer = self.db.get_customer(sale.customer_id)
            self.table.setItem(row, 0, QTableWidgetItem(str(sale.id)))
            self.table.setItem(row, 1, QTableWidgetItem(customer.name if customer else ""))
            self.table.setItem(row, 2, QTableWidgetItem(sale.product))
            self.table.setItem(row, 3, QTableWidgetItem(f"{sale.amount:.2f} TL"))
            self.table.setItem(row, 4, QTableWidgetItem(sale.status))
            self.table.setItem(row, 5, QTableWidgetItem(sale.created_at.strftime("%d.%m.%Y")))
            self.table.setItem(row, 6, QTableWidgetItem(sale.description or ""))
    
    def add_sale(self):
        """Yeni satış ekle"""
        dialog = SaleDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            sale = dialog.get_sale()
            try:
                self.db.add_sale(sale)
                self.load_sales()
                QMessageBox.information(self, "Başarı", "Satış kaydı eklendi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Satış eklenirken hata oluştu: {str(e)}")
    
    def edit_sale(self):
        """Satış düzenle"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Düzenlemek için bir satış seçin.")
            return
        
        sale_id = int(self.table.item(current_row, 0).text())
        customers = self.db.get_all_customers()
        sale = None
        for customer in customers:
            sales = self.db.get_customer_sales(customer.id)
            for s in sales:
                if s.id == sale_id:
                    sale = s
                    break
        
        if sale:
            dialog = SaleDialog(self.db, sale)
            if dialog.exec_() == QDialog.Accepted:
                updated_sale = dialog.get_sale()
                try:
                    self.db.update_sale(updated_sale)
                    self.load_sales()
                    QMessageBox.information(self, "Başarı", "Satış kaydı güncellendi.")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Satış güncellenirken hata oluştu: {str(e)}")
    
    def delete_sale(self):
        """Satış sil"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir satış seçin.")
            return
        
        sale_id = int(self.table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, "Onay",
            "Bu satış kaydını silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_sale(sale_id)
                self.load_sales()
                QMessageBox.information(self, "Başarı", "Satış kaydı silindi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Satış silinirken hata oluştu: {str(e)}")


class SaleDialog(QDialog):
    """Satış ekleme/düzenleme diyaloğu"""
    
    def __init__(self, db: Database, sale=None):
        super().__init__()
        self.db = db
        self.sale = sale or Sale()
        self.init_ui()
    
    def init_ui(self):
        """Diyaloğu oluştur"""
        layout = QVBoxLayout()
        
        # Müşteri
        customer_label = QLabel("Müşteri:")
        self.customer_combo = QComboBox()
        customers = self.db.get_all_customers()
        for customer in customers:
            self.customer_combo.addItem(customer.name, customer.id)
        
        if self.sale.customer_id:
            index = self.customer_combo.findData(self.sale.customer_id)
            self.customer_combo.setCurrentIndex(index)
        
        layout.addWidget(customer_label)
        layout.addWidget(self.customer_combo)
        
        # Ürün
        product_label = QLabel("Ürün:")
        self.product_input = QLineEdit()
        self.product_input.setText(self.sale.product)
        layout.addWidget(product_label)
        layout.addWidget(self.product_input)
        
        # Miktar
        amount_label = QLabel("Miktar (TL):")
        self.amount_input = QLineEdit()
        self.amount_input.setText(str(self.sale.amount))
        layout.addWidget(amount_label)
        layout.addWidget(self.amount_input)
        
        # Durum
        status_label = QLabel("Durum:")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Bekleme", "Devam Ediyor", "Tamamlandı", "İptal"])
        if self.sale.status:
            self.status_combo.setCurrentText(self.sale.status)
        layout.addWidget(status_label)
        layout.addWidget(self.status_combo)
        
        # Açıklama
        description_label = QLabel("Açıklama:")
        self.description_input = QTextEdit()
        self.description_input.setText(self.sale.description)
        self.description_input.setMaximumHeight(100)
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)
        
        # Butonlar
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Kaydet")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("Satış Ekle/Düzenle")
        self.setGeometry(200, 200, 500, 400)
    
    def get_sale(self) -> Sale:
        """Diyalogdan satış bilgisini al"""
        self.sale.customer_id = self.customer_combo.currentData()
        self.sale.product = self.product_input.text()
        self.sale.amount = float(self.amount_input.text() or 0)
        self.sale.status = self.status_combo.currentText()
        self.sale.description = self.description_input.toPlainText()
        return self.sale
