import sqlite3
from datetime import datetime
from typing import List, Optional
import os

from models import Customer, Sale, Communication, Task


class Database:
    """SQLite veritabanı yönetimi"""
    
    def __init__(self, db_path: str = "crm.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Veritabanı bağlantısı oluştur"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Müşteriler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                country TEXT,
                company TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Satışlar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                amount REAL,
                product TEXT,
                status TEXT DEFAULT 'Bekleme',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # İletişim geçmişi tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS communications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                type TEXT,
                subject TEXT,
                content TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Görevler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                due_date TIMESTAMP,
                priority TEXT DEFAULT 'Normal',
                status TEXT DEFAULT 'Beklemede',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # MÜŞTERİ İŞLEMLERİ
    def add_customer(self, customer: Customer) -> int:
        """Yeni müşteri ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, email, phone, address, city, country, company, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer.name, customer.email, customer.phone, customer.address,
              customer.city, customer.country, customer.company, customer.notes))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return customer_id
    
    def get_all_customers(self) -> List[Customer]:
        """Tüm müşterileri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_customer(row) for row in rows]
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Belirli müşteriyi getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_customer(row) if row else None
    
    def update_customer(self, customer: Customer):
        """Müşteriyi güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers
            SET name=?, email=?, phone=?, address=?, city=?, country=?, company=?, notes=?, updated_at=?
            WHERE id=?
        ''', (customer.name, customer.email, customer.phone, customer.address,
              customer.city, customer.country, customer.company, customer.notes,
              datetime.now(), customer.id))
        conn.commit()
        conn.close()
    
    def delete_customer(self, customer_id: int):
        """Müşteriyi sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
    
    def search_customers(self, query: str) -> List[Customer]:
        """Müşteri ara"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{query}%"
        cursor.execute('''
            SELECT * FROM customers
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR company LIKE ?
            ORDER BY name
        ''', (search_pattern, search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_customer(row) for row in rows]
    
    # SATIŞS İŞLEMLERİ
    def add_sale(self, sale: Sale) -> int:
        """Yeni satış ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sales (customer_id, amount, product, status, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (sale.customer_id, sale.amount, sale.product, sale.status, sale.description))
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        return sale_id
    
    def get_customer_sales(self, customer_id: int) -> List[Sale]:
        """Müşterinin satışlarını getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sales WHERE customer_id = ? ORDER BY created_at DESC', (customer_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_sale(row) for row in rows]
    
    def update_sale(self, sale: Sale):
        """Satışı güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE sales
            SET customer_id=?, amount=?, product=?, status=?, description=?, updated_at=?
            WHERE id=?
        ''', (sale.customer_id, sale.amount, sale.product, sale.status, sale.description, datetime.now(), sale.id))
        conn.commit()
        conn.close()
    
    def delete_sale(self, sale_id: int):
        """Satışı sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sales WHERE id = ?', (sale_id,))
        conn.commit()
        conn.close()
    
    # İLETİŞİM İŞLEMLERİ
    def add_communication(self, comm: Communication) -> int:
        """Yeni iletişim kaydı ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO communications (customer_id, type, subject, content, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (comm.customer_id, comm.type, comm.subject, comm.content, comm.notes))
        conn.commit()
        comm_id = cursor.lastrowid
        conn.close()
        return comm_id
    
    def get_customer_communications(self, customer_id: int) -> List[Communication]:
        """Müşterinin iletişim geçmişini getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM communications WHERE customer_id = ? ORDER BY created_at DESC', (customer_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_communication(row) for row in rows]
    
    def delete_communication(self, comm_id: int):
        """İletişim kaydını sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM communications WHERE id = ?', (comm_id,))
        conn.commit()
        conn.close()
    
    # GÖREV İŞLEMLERİ
    def add_task(self, task: Task) -> int:
        """Yeni görev ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (customer_id, title, description, due_date, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task.customer_id, task.title, task.description, task.due_date, task.priority, task.status))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id
    
    def get_customer_tasks(self, customer_id: int) -> List[Task]:
        """Müşterinin görevlerini getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE customer_id = ? ORDER BY due_date', (customer_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_task(row) for row in rows]
    
    def get_all_tasks(self) -> List[Task]:
        """Tüm görevleri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY due_date')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_task(row) for row in rows]
    
    def update_task(self, task: Task):
        """Görevi güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET customer_id=?, title=?, description=?, due_date=?, priority=?, status=?, updated_at=?
            WHERE id=?
        ''', (task.customer_id, task.title, task.description, task.due_date, task.priority, task.status, datetime.now(), task.id))
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id: int):
        """Görevi sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    
    # RAPORLAMA
    def get_sales_summary(self):
        """Satış özeti getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count, SUM(amount) as total
            FROM sales
            GROUP BY status
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_total_sales(self):
        """Toplam satış miktarı"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) as total FROM sales')
        row = cursor.fetchone()
        conn.close()
        return row['total'] or 0
    
    def get_total_customers(self):
        """Toplam müşteri sayısı"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM customers')
        row = cursor.fetchone()
        conn.close()
        return row['count']
    
    # YÖNETİM FONKSİYONLARI
    def _row_to_customer(self, row) -> Customer:
        """Veritabanı satırını Customer nesnesine dönüştür"""
        if not row:
            return None
        return Customer(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
            address=row['address'],
            city=row['city'],
            country=row['country'],
            company=row['company'],
            notes=row['notes'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
    
    def _row_to_sale(self, row) -> Sale:
        """Veritabanı satırını Sale nesnesine dönüştür"""
        if not row:
            return None
        return Sale(
            id=row['id'],
            customer_id=row['customer_id'],
            amount=row['amount'],
            product=row['product'],
            status=row['status'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
    
    def _row_to_communication(self, row) -> Communication:
        """Veritabanı satırını Communication nesnesine dönüştür"""
        if not row:
            return None
        return Communication(
            id=row['id'],
            customer_id=row['customer_id'],
            type=row['type'],
            subject=row['subject'],
            content=row['content'],
            notes=row['notes'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
    
    def _row_to_task(self, row) -> Task:
        """Veritabanı satırını Task nesnesine dönüştür"""
        if not row:
            return None
        return Task(
            id=row['id'],
            customer_id=row['customer_id'],
            title=row['title'],
            description=row['description'],
            due_date=datetime.fromisoformat(row['due_date']) if row['due_date'] else None,
            priority=row['priority'],
            status=row['status'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
