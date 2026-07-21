from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

from database import Database
from models import Communication


class CommunicationsWidget(QWidget):
    """İletişim geçmişi sekmesi"""
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_communications()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout()
        
        # Kontrol paneli
        control_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Yeni İletişim")
        add_btn.clicked.connect(self.add_communication)
        
        edit_btn = QPushButton("✏️ Düzenle")
        edit_btn.clicked.connect(self.edit_communication)
        
        delete_btn = QPushButton("🗑️ Sil")
        delete_btn.clicked.connect(self.delete_communication)
        
        control_layout.addWidget(add_btn)
        control_layout.addWidget(edit_btn)
        control_layout.addWidget(delete_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
        # İletişim tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Müşteri", "Tür", "Konu", "Tarih", "Not"])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_communications(self):
        """İletişim geçmişini tablodan yükle"""
        all_comms = []
        customers = self.db.get_all_customers()
        
        for customer in customers:
            comms = self.db.get_customer_communications(customer.id)
            all_comms.extend(comms)
        
        self.table.setRowCount(len(all_comms))
        
        for row, comm in enumerate(all_comms):
            customer = self.db.get_customer(comm.customer_id)
            self.table.setItem(row, 0, QTableWidgetItem(str(comm.id)))
            self.table.setItem(row, 1, QTableWidgetItem(customer.name if customer else ""))
            self.table.setItem(row, 2, QTableWidgetItem(comm.type))
            self.table.setItem(row, 3, QTableWidgetItem(comm.subject))
            self.table.setItem(row, 4, QTableWidgetItem(comm.created_at.strftime("%d.%m.%Y %H:%M")))
            self.table.setItem(row, 5, QTableWidgetItem(comm.notes or ""))
    
    def add_communication(self):
        """Yeni iletişim kaydı ekle"""
        dialog = CommunicationDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            comm = dialog.get_communication()
            try:
                self.db.add_communication(comm)
                self.load_communications()
                QMessageBox.information(self, "Başarı", "İletişim kaydı eklendi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"İletişim eklenirken hata oluştu: {str(e)}")
    
    def edit_communication(self):
        """İletişim kaydı düzenle"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Düzenlemek için bir kayıt seçin.")
            return
        
        comm_id = int(self.table.item(current_row, 0).text())
        customers = self.db.get_all_customers()
        comm = None
        for customer in customers:
            comms = self.db.get_customer_communications(customer.id)
            for c in comms:
                if c.id == comm_id:
                    comm = c
                    break
        
        if comm:
            dialog = CommunicationDialog(self.db, comm)
            if dialog.exec_() == QDialog.Accepted:
                self.db.delete_communication(comm_id)
                new_comm = dialog.get_communication()
                self.db.add_communication(new_comm)
                self.load_communications()
                QMessageBox.information(self, "Başarı", "İletişim kaydı güncellendi.")
    
    def delete_communication(self):
        """İletişim kaydı sil"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir kayıt seçin.")
            return
        
        comm_id = int(self.table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, "Onay",
            "Bu iletişim kaydını silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_communication(comm_id)
                self.load_communications()
                QMessageBox.information(self, "Başarı", "İletişim kaydı silindi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"İletişim silinirken hata oluştu: {str(e)}")


class CommunicationDialog(QDialog):
    """İletişim ekleme/düzenleme diyaloğu"""
    
    def __init__(self, db: Database, comm=None):
        super().__init__()
        self.db = db
        self.comm = comm or Communication()
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
        
        if self.comm.customer_id:
            index = self.customer_combo.findData(self.comm.customer_id)
            self.customer_combo.setCurrentIndex(index)
        
        layout.addWidget(customer_label)
        layout.addWidget(self.customer_combo)
        
        # İletişim türü
        type_label = QLabel("İletişim Türü:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Email", "Telefon", "Toplantı", "Diğer"])
        if self.comm.type:
            self.type_combo.setCurrentText(self.comm.type)
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)
        
        # Konu
        subject_label = QLabel("Konu:")
        self.subject_input = QLineEdit()
        self.subject_input.setText(self.comm.subject)
        layout.addWidget(subject_label)
        layout.addWidget(self.subject_input)
        
        # İçerik
        content_label = QLabel("İçerik:")
        self.content_input = QTextEdit()
        self.content_input.setText(self.comm.content)
        layout.addWidget(content_label)
        layout.addWidget(self.content_input)
        
        # Notlar
        notes_label = QLabel("Notlar:")
        self.notes_input = QTextEdit()
        self.notes_input.setText(self.comm.notes)
        self.notes_input.setMaximumHeight(80)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_input)
        
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
        self.setWindowTitle("İletişim Ekle/Düzenle")
        self.setGeometry(200, 200, 600, 500)
    
    def get_communication(self) -> Communication:
        """Diyalogdan iletişim bilgisini al"""
        self.comm.customer_id = self.customer_combo.currentData()
        self.comm.type = self.type_combo.currentText()
        self.comm.subject = self.subject_input.text()
        self.comm.content = self.content_input.toPlainText()
        self.comm.notes = self.notes_input.toPlainText()
        return self.comm
