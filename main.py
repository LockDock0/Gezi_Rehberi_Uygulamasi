import sys
import sqlite3
import requests
import csv
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter
from database import veritabani_olustur

# --- ANYTYPE TARZI AYDINLIK TEMA ---
TEMA_AYDINLIK = """
QWidget { background-color: #FAFAFA; color: #111111; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 14px; }
QLabel { color: #222222; }
QLabel h1, QLabel h2, QLabel h3 { font-weight: 600; color: #000000; letter-spacing: -0.5px; }
QPushButton { background-color: #FFFFFF; color: #111111; border: 1px solid #EAEAEA; border-radius: 8px; padding: 10px 18px; font-weight: 500; outline: none; }
QPushButton:hover { background-color: #F0F0F0; border: 1px solid #DDDDDD; }
QPushButton:pressed { background-color: #E5E5E5; }
QPushButton#VurguluBtn { background-color: #111111; color: #FFFFFF; border: none; }
QPushButton#VurguluBtn:hover { background-color: #333333; }
QPushButton#SilBtn { background-color: #FFF0F0; color: #D32F2F; border: 1px solid #FFCDD2; }
QPushButton#SilBtn:hover { background-color: #FFEBEE; border: 1px solid #EF9A9A; }
QLineEdit, QSpinBox, QTextBrowser, QTextEdit, QComboBox { background-color: #FFFFFF; border: 1px solid #EAEAEA; border-radius: 8px; padding: 10px; color: #111111; selection-background-color: #D3E2FD; selection-color: #111111; }
QLineEdit:focus, QSpinBox:focus, QTextBrowser:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #A0A0A0; }
QListWidget { background-color: transparent; border: none; outline: 0; }
QListWidget::item { padding: 14px; margin-bottom: 4px; border-radius: 8px; background-color: #FFFFFF; border: 1px solid #EAEAEA; }
QListWidget::item:selected { background-color: #F0F4FF; color: #111111; border: 1px solid #D3E2FD; font-weight: 500; }
QTabWidget::pane { border: none; background: transparent; top: 10px; }
QTabBar::tab { background: transparent; border: none; padding: 10px 15px; min-width: 140px; margin-right: 5px; color: #666666; font-weight: 500; font-size: 14px; border-bottom: 2px solid transparent; }
QTabBar::tab:selected { color: #111111; border-bottom: 2px solid #111111; font-weight: 600; }
QTabBar::tab:hover:!selected { color: #333333; }
QTableWidget { background-color: #FFFFFF; border: 1px solid #EAEAEA; border-radius: 8px; gridline-color: #EAEAEA; outline: none; }
QHeaderView::section { background-color: #F0F0F0; padding: 8px; border: 1px solid #EAEAEA; font-weight: bold; }
QGroupBox { font-weight: 600; border: 1px solid #EAEAEA; border-radius: 8px; margin-top: 15px; padding-top: 15px; }
#UstBar { background-color: #FFFFFF; border-bottom: 1px solid #EAEAEA; }
#OzelBaslik { background-color: #FFFFFF; }
#BaslikBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #111111; outline: none; }
#BaslikBtn:hover { background-color: #EAEAEA; }
#KapatBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #111111; outline: none; }
#KapatBtn:hover { background-color: #E81123; color: white; }
QDialog { background-color: #FAFAFA; }
"""

# --- ANYTYPE TARZI KARANLIK TEMA (DARK MODE) ---
TEMA_KARANLIK = """
QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 14px; }
QLabel { color: #E0E0E0; }
QLabel h1, QLabel h2, QLabel h3 { font-weight: 600; color: #FFFFFF; letter-spacing: -0.5px; }
QPushButton { background-color: #1E1E1E; color: #E0E0E0; border: 1px solid #2A2A2A; border-radius: 8px; padding: 10px 18px; font-weight: 500; outline: none; }
QPushButton:hover { background-color: #2C2C2C; border: 1px solid #3A3A3A; }
QPushButton:pressed { background-color: #3A3A3A; }
QPushButton#VurguluBtn { background-color: #E0E0E0; color: #121212; border: none; }
QPushButton#VurguluBtn:hover { background-color: #FFFFFF; }
QPushButton#SilBtn { background-color: #2A1A1A; color: #EF5350; border: 1px solid #4A2A2A; }
QPushButton#SilBtn:hover { background-color: #3A1A1A; border: 1px solid #E53935; }
QLineEdit, QSpinBox, QTextBrowser, QTextEdit, QComboBox { background-color: #1E1E1E; border: 1px solid #2A2A2A; border-radius: 8px; padding: 10px; color: #E0E0E0; selection-background-color: #4A4A4A; selection-color: #FFFFFF; }
QLineEdit:focus, QSpinBox:focus, QTextBrowser:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #555555; }
QListWidget { background-color: transparent; border: none; outline: 0; }
QListWidget::item { padding: 14px; margin-bottom: 4px; border-radius: 8px; background-color: #1A1A1A; border: 1px solid #222222; }
QListWidget::item:selected { background-color: #2A2A35; color: #FFFFFF; border: 1px solid #4A4A5A; font-weight: 500; }
QTabWidget::pane { border: none; background: transparent; top: 10px; }
QTabBar::tab { background: transparent; border: none; padding: 10px 15px; min-width: 140px; margin-right: 5px; color: #888888; font-weight: 500; font-size: 14px; border-bottom: 2px solid transparent; }
QTabBar::tab:selected { color: #FFFFFF; border-bottom: 2px solid #FFFFFF; font-weight: 600; }
QTabBar::tab:hover:!selected { color: #AAAAAA; }
QTableWidget { background-color: #1A1A1A; border: 1px solid #222222; border-radius: 8px; gridline-color: #2A2A2A; outline: none; }
QHeaderView::section { background-color: #222222; padding: 8px; border: 1px solid #2A2A2A; font-weight: bold; color: white; }
QGroupBox { font-weight: 600; border: 1px solid #222222; border-radius: 8px; margin-top: 15px; padding-top: 15px; }
#UstBar { background-color: #1A1A1A; border-bottom: 1px solid #222222; }
#OzelBaslik { background-color: #1A1A1A; }
#BaslikBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #E0E0E0; outline: none; }
#BaslikBtn:hover { background-color: #2A2A2A; }
#KapatBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #E0E0E0; outline: none; }
#KapatBtn:hover { background-color: #E81123; color: white; outline: none; }
QDialog { background-color: #121212; }
"""

class OzelBaslikCubugu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("OzelBaslik")
        self.setFixedHeight(35)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 0, 0)
        layout.setSpacing(0)
        
        self.lbl_baslik = QLabel("Gezi Rehberi")
        self.lbl_baslik.setStyleSheet("font-weight: 500; font-size: 13px; color: gray;")
        layout.addWidget(self.lbl_baslik)
        layout.addStretch()
        
        self.btn_kucult = QPushButton("—")
        self.btn_buyut = QPushButton("◻")
        self.btn_kapat = QPushButton("✕")
        
        self.btn_kucult.setObjectName("BaslikBtn")
        self.btn_buyut.setObjectName("BaslikBtn")
        self.btn_kapat.setObjectName("KapatBtn")
        
        self.btn_kucult.setFixedSize(45, 35)
        self.btn_buyut.setFixedSize(45, 35)
        self.btn_kapat.setFixedSize(45, 35)
        
        self.btn_kucult.clicked.connect(self.parent.showMinimized)
        self.btn_buyut.clicked.connect(self.pencereyi_buyut_kucult)
        self.btn_kapat.clicked.connect(self.parent.close)
        
        layout.addWidget(self.btn_kucult)
        layout.addWidget(self.btn_buyut)
        layout.addWidget(self.btn_kapat)

        self._is_tracking = False
        self._start_pos = None

    def pencereyi_buyut_kucult(self):
        if self.parent.isMaximized(): self.parent.showNormal()
        else: self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_tracking = True
            self._start_pos = event.globalPos() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._is_tracking: self.parent.move(event.globalPos() - self._start_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton: self._is_tracking = False

class GirisEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        layout.addWidget(QLabel("<h1 style='text-align: center; font-size: 28px;'>Gezi Rehberi</h1>"))
        layout.addSpacing(20)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.input_kullanici = QLineEdit()
        self.input_kullanici.setPlaceholderText("Kullanıcı adı...")
        self.input_sifre = QLineEdit()
        self.input_sifre.setPlaceholderText("Şifre...")
        self.input_sifre.setEchoMode(QLineEdit.Password)
        
        self.input_kullanici.returnPressed.connect(self.giris_yap)
        self.input_sifre.returnPressed.connect(self.giris_yap)
        
        form_layout.addRow("Kullanıcı Adı:", self.input_kullanici)
        form_layout.addRow("Şifre:", self.input_sifre)
        layout.addWidget(form_widget)

        layout.addSpacing(20)
        btn_layout = QHBoxLayout()
        btn_giris = QPushButton("Giriş Yap")
        btn_giris.setObjectName("VurguluBtn") 
        btn_giris.clicked.connect(self.giris_yap)
        btn_kayit = QPushButton("Kayıt Ol")
        btn_kayit.clicked.connect(lambda: self.parent.ekran_degistir(1)) 
        
        btn_layout.addWidget(btn_kayit)
        btn_layout.addWidget(btn_giris)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def giris_yap(self):
        k_adi, sifre = self.input_kullanici.text(), self.input_sifre.text()
        if not k_adi or not sifre: return
        
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (k_adi, sifre))
        kullanici = cursor.fetchone()
        conn.close()

        if kullanici:
            self.parent.aktif_kullanici_id = kullanici[0]
            self.parent.aktif_kullanici_adi = k_adi
            self.parent.lbl_kullanici_isim.setText(f"Merhaba, {k_adi}")
            self.parent.sayfa_profil.kompleteri_ve_notlari_yukle()
            self.parent.ekran_degistir(2) 
            self.input_kullanici.clear()
            self.input_sifre.clear()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")

class KayitEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        
        layout.addWidget(QLabel("<h2 style='text-align: center;'>Yeni Hesap Oluştur</h2>"))
        layout.addSpacing(20)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.input_yeni_kullanici = QLineEdit()
        self.input_yeni_sifre = QLineEdit()
        self.input_yeni_sifre.setEchoMode(QLineEdit.Password)
        self.input_sifre_tekrar = QLineEdit()
        self.input_sifre_tekrar.setEchoMode(QLineEdit.Password)
        
        self.input_yeni_kullanici.returnPressed.connect(self.kayit_islemi)
        self.input_yeni_sifre.returnPressed.connect(self.kayit_islemi)
        self.input_sifre_tekrar.returnPressed.connect(self.kayit_islemi)
        
        form_layout.addRow("Kullanıcı Adı:", self.input_yeni_kullanici)
        form_layout.addRow("Şifre:", self.input_yeni_sifre)
        form_layout.addRow("Şifre Tekrar:", self.input_sifre_tekrar)
        layout.addWidget(form_widget)

        layout.addSpacing(20)
        btn_layout = QHBoxLayout()
        btn_kaydi_tamamla = QPushButton("Tamamla")
        btn_kaydi_tamamla.setObjectName("VurguluBtn")
        btn_kaydi_tamamla.clicked.connect(self.kayit_islemi)
        btn_iptal = QPushButton("Geri Dön")
        btn_iptal.clicked.connect(lambda: self.parent.ekran_degistir(0)) 
        
        btn_layout.addWidget(btn_iptal)
        btn_layout.addWidget(btn_kaydi_tamamla)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def kayit_islemi(self):
        k_adi = self.input_yeni_kullanici.text()
        sifre = self.input_yeni_sifre.text()
        if k_adi == "" or sifre == "" or sifre != self.input_sifre_tekrar.text(): return
        try:
            conn = sqlite3.connect('akilli_rehber.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (k_adi, sifre))
            conn.commit()
            conn.close()
            self.input_yeni_kullanici.clear()
            self.input_yeni_sifre.clear()
            self.input_sifre_tekrar.clear()
            self.parent.ekran_degistir(0)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı alınmış.")

class AnaEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        icerik_widget = QWidget()
        merkez_layout = QVBoxLayout(icerik_widget)
        merkez_layout.setAlignment(Qt.AlignCenter)
        
        merkez_layout.addWidget(QLabel("<h1 style='text-align: center; font-size: 32px;'>Gezilerini Planla</h1>"))
        merkez_layout.addWidget(QLabel("<h3 style='text-align: center; color: #888888; font-weight: 400;'>Keşfetmek istediğin rotayı seçerek başla.</h3>"))
        merkez_layout.addSpacing(30)

        grid_layout = QGridLayout()
        kategoriler = [("☀️ Yaz Tatili", 0, 0), ("❄️ Kış Tatili", 0, 1), 
                       ("🌲 Doğa & Kamp", 1, 0), ("🏛️ Kültür Turu", 1, 1)]
        
        for isim, satir, sutun in kategoriler:
            btn = QPushButton(isim)
            btn.setMinimumHeight(80) 
            btn.setCursor(Qt.PointingHandCursor) 
            db_isim = isim.split(" ", 1)[1] 
            btn.clicked.connect(lambda _, k=db_isim: self.parent.sezon_sec(k))
            grid_layout.addWidget(btn, satir, sutun)
        
        merkez_layout.addLayout(grid_layout)
        layout.addWidget(icerik_widget)
        self.setLayout(layout)

class ProfilEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 30)
        
        ust_baslik_layout = QHBoxLayout()
        ust_baslik_layout.addWidget(QLabel("<h2 style='font-size: 24px;'>Kişisel Alan</h2>"))
        ust_baslik_layout.addStretch()
        
        btn_excel = QPushButton("📥 CSV İndir")
        btn_excel.clicked.connect(self.excel_cikti_al)
        
        btn_pdf = QPushButton("📄 PDF Raporu Al")
        btn_pdf.clicked.connect(self.pdf_rapor_al)
        
        ust_baslik_layout.addWidget(btn_excel)
        ust_baslik_layout.addWidget(btn_pdf)
        layout.addLayout(ust_baslik_layout)
        
        self.sekmeler = QTabWidget()
        
        self.tab_gidilecek = QWidget()
        layout_g1 = QVBoxLayout(self.tab_gidilecek)
        layout_g1.setContentsMargins(0, 15, 0, 0)
        h1 = QHBoxLayout()
        self.input_gidilecek = QLineEdit()
        self.input_gidilecek.setPlaceholderText("📍 Şehir veya 🏛️ Mekan ara...")
        self.input_gidilecek.setMinimumHeight(45)
        self.input_gidilecek.returnPressed.connect(lambda: self.not_ekle_yeni("Gidilecek Yerler", self.input_gidilecek))
        btn_ekle1 = QPushButton("Ekle")
        btn_ekle1.setObjectName("VurguluBtn")
        btn_ekle1.setMinimumHeight(45)
        btn_ekle1.clicked.connect(lambda: self.not_ekle_yeni("Gidilecek Yerler", self.input_gidilecek))
        h1.addWidget(self.input_gidilecek)
        h1.addWidget(btn_ekle1)
        self.liste_gidilecek = QListWidget()
        self.liste_gidilecek.itemDoubleClicked.connect(lambda item: self.not_sil(item, "Gidilecek Yerler"))
        layout_g1.addLayout(h1)
        layout_g1.addWidget(self.liste_gidilecek)

        self.tab_gidilen = QWidget()
        layout_g2 = QVBoxLayout(self.tab_gidilen)
        layout_g2.setContentsMargins(0, 15, 0, 0)
        h2 = QHBoxLayout()
        self.input_gidilen = QLineEdit()
        self.input_gidilen.setPlaceholderText("📍 Şehir veya 🏛️ Mekan ara...")
        self.input_gidilen.setMinimumHeight(45)
        self.input_gidilen.returnPressed.connect(lambda: self.not_ekle_yeni("Gidilen Yerler", self.input_gidilen))
        btn_ekle2 = QPushButton("Ekle")
        btn_ekle2.setObjectName("VurguluBtn")
        btn_ekle2.setMinimumHeight(45)
        btn_ekle2.clicked.connect(lambda: self.not_ekle_yeni("Gidilen Yerler", self.input_gidilen))
        h2.addWidget(self.input_gidilen)
        h2.addWidget(btn_ekle2)
        self.liste_gidilen = QListWidget()
        self.liste_gidilen.itemDoubleClicked.connect(lambda item: self.not_sil(item, "Gidilen Yerler"))
        layout_g2.addLayout(h2)
        layout_g2.addWidget(self.liste_gidilen)

        self.tab_notlar = QWidget()
        layout_n = QVBoxLayout(self.tab_notlar)
        layout_n.setContentsMargins(0, 15, 0, 0)
        self.text_notepad = QTextEdit()
        self.text_notepad.setPlaceholderText("Seyahat planlarını, bütçe notlarını veya aklına gelenleri buraya yazabilirsin...")
        btn_not_kaydet = QPushButton("Notları Kaydet")
        btn_not_kaydet.setObjectName("VurguluBtn")
        btn_not_kaydet.setMinimumHeight(45)
        btn_not_kaydet.clicked.connect(self.notepad_kaydet)
        layout_n.addWidget(self.text_notepad)
        layout_n.addWidget(btn_not_kaydet)

        self.tablo_gecmis = QTableWidget()
        self.tablo_gecmis.setColumnCount(6)
        self.tablo_gecmis.setHorizontalHeaderLabels(["Şehir", "Mekan", "Kategori", "Bütçe", "Puan", "Yorum"])
        self.tablo_gecmis.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo_gecmis.horizontalHeader().setSectionResizeMode(5, QHeaderView.Interactive)
        self.tablo_gecmis.setColumnWidth(5, 300)
        self.tablo_gecmis.setWordWrap(True)
        self.tablo_gecmis.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tablo_gecmis.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo_gecmis.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.sekmeler.addTab(self.tab_gidilecek, "Gidilecek Yerler")
        self.sekmeler.addTab(self.tab_gidilen, "Gidilen Yerler")
        self.sekmeler.addTab(self.tab_notlar, "Genel Notlar")
        self.sekmeler.addTab(self.tablo_gecmis, "📊 Tüm İstatistikler") 
        
        layout.addWidget(self.sekmeler)
        self.setLayout(layout)

    def kompleteri_ve_notlari_yukle(self):
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        
        kelimeler = []
        cursor.execute("SELECT sehir_adi FROM Sehirler")
        kelimeler.extend(["📍 Şehir: " + row[0] for row in cursor.fetchall()])
        cursor.execute("SELECT mekan_adi FROM Mekanlar")
        kelimeler.extend(["🏛️ Mekan: " + row[0] for row in cursor.fetchall()])
        
        tamamlayici = QCompleter(kelimeler)
        tamamlayici.setCaseSensitivity(Qt.CaseInsensitive) 
        tamamlayici.setFilterMode(Qt.MatchContains) 
        
        self.input_gidilecek.setCompleter(tamamlayici)
        self.input_gidilen.setCompleter(tamamlayici)

        self.liste_gidilecek.clear()
        self.liste_gidilen.clear()
        self.text_notepad.clear()
        self.tablo_gecmis.setRowCount(0)

        cursor.execute("SELECT kategori, not_icerik, tarih FROM SeyahatNotlari WHERE kullanici_id = ?", (self.parent.aktif_kullanici_id,))
        for n in cursor.fetchall():
            kategori = n[0]
            if kategori == "Gidilecek Yerler":
                self.liste_gidilecek.addItem(f"{n[1]} \n⏱️ {n[2].split()[0]}")
            elif kategori == "Gidilen Yerler":
                self.liste_gidilen.addItem(f"{n[1]} \n⏱️ {n[2].split()[0]}")
            elif kategori == "Genel Notlar":
                self.text_notepad.setText(n[1])
            
        sorgu = '''SELECT s.sehir_adi, m.mekan_adi, m.sezon, m.butce, z.puan, z.yorum 
                   FROM Ziyaret_ve_Puanlama z
                   JOIN Mekanlar m ON z.mekan_id = m.id
                   JOIN Sehirler s ON m.sehir_id = s.id
                   WHERE z.kullanici_id = ? ORDER BY z.id DESC'''
        cursor.execute(sorgu, (self.parent.aktif_kullanici_id,))
        degerlendirmeler = cursor.fetchall()
        
        for row_idx, d in enumerate(degerlendirmeler):
            sehir_adi, mekan_adi, sezon, butce, puan, yorum = d
            
            self.tablo_gecmis.insertRow(row_idx)
            self.tablo_gecmis.setItem(row_idx, 0, QTableWidgetItem(str(sehir_adi)))
            self.tablo_gecmis.setItem(row_idx, 1, QTableWidgetItem(str(mekan_adi)))
            self.tablo_gecmis.setItem(row_idx, 2, QTableWidgetItem(str(sezon)))
            self.tablo_gecmis.setItem(row_idx, 3, QTableWidgetItem(str(butce)))
            self.tablo_gecmis.setItem(row_idx, 4, QTableWidgetItem("⭐ " * puan if puan > 0 else "-"))
            
            yorum_item = QTableWidgetItem(str(yorum) if yorum else "-")
            self.tablo_gecmis.setItem(row_idx, 5, yorum_item)
            
        conn.close()

    def not_ekle_yeni(self, kategori, input_widget):
        yeni_not = input_widget.text().strip()
        if yeni_not == "": return
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SeyahatNotlari (kullanici_id, kategori, not_icerik) VALUES (?, ?, ?)", 
                       (self.parent.aktif_kullanici_id, kategori, yeni_not))
        conn.commit()
        conn.close()
        input_widget.clear()
        self.kompleteri_ve_notlari_yukle() 

    def not_sil(self, item, kategori):
        cevap = QMessageBox.question(self, 'Sil', "Bu notu silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if cevap == QMessageBox.Yes:
            not_metni = item.text().split("\n")[0].strip()
            conn = sqlite3.connect('akilli_rehber.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM SeyahatNotlari WHERE kullanici_id=? AND kategori=? AND not_icerik=?", 
                           (self.parent.aktif_kullanici_id, kategori, not_metni))
            conn.commit()
            conn.close()
            self.kompleteri_ve_notlari_yukle()

    def notepad_kaydet(self):
        icerik = self.text_notepad.toPlainText()
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SeyahatNotlari WHERE kullanici_id=? AND kategori='Genel Notlar'", (self.parent.aktif_kullanici_id,))
        if icerik.strip():
            cursor.execute("INSERT INTO SeyahatNotlari (kullanici_id, kategori, not_icerik) VALUES (?, ?, ?)",
                           (self.parent.aktif_kullanici_id, 'Genel Notlar', icerik.strip()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Başarılı", "Genel notlarınız başarıyla kaydedildi!")

    def excel_cikti_al(self):
        dosya_adi = f"Seyahat_Panosu_{self.parent.aktif_kullanici_adi}.csv"
        try:
            with open(dosya_adi, mode='w', newline='', encoding='utf-8-sig') as f:
                yazici = csv.writer(f, delimiter=';')
                yazici.writerow(["Liste/Tür", "İçerik", "Tarih/Puan"])
                conn = sqlite3.connect('akilli_rehber.db')
                cursor = conn.cursor()
                cursor.execute("SELECT kategori, not_icerik, tarih FROM SeyahatNotlari WHERE kullanici_id = ?", (self.parent.aktif_kullanici_id,))
                for n in cursor.fetchall(): yazici.writerow([n[0], n[1], n[2].split()[0]])
                cursor.execute('''SELECT m.mekan_adi, z.yorum, z.puan FROM Ziyaret_ve_Puanlama z
                                  JOIN Mekanlar m ON z.mekan_id = m.id WHERE z.kullanici_id = ?''', (self.parent.aktif_kullanici_id,))
                for d in cursor.fetchall(): yazici.writerow(["Değerlendirme", f"{d[0]} - {d[1]}", f"{d[2]} Puan"])
                conn.close()
            yol = os.path.abspath(dosya_adi)
            QMessageBox.information(self, "Başarılı", f"Panonuz başarıyla Excel (CSV) olarak kaydedildi!\n\nYol:\n{yol}")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hata oluştu: {str(e)}")

    def pdf_rapor_al(self):
        dosya_yolu, _ = QFileDialog.getSaveFileName(self, "Seyahat Raporunu Kaydet", f"Seyahat_Raporum_{self.parent.aktif_kullanici_adi}.pdf", "PDF Dosyaları (*.pdf)")
        if not dosya_yolu: return
        
        try:
            conn = sqlite3.connect('akilli_rehber.db')
            cursor = conn.cursor()
            sorgu = '''SELECT s.sehir_adi, m.mekan_adi, m.sezon, z.puan, z.yorum 
                       FROM Ziyaret_ve_Puanlama z
                       JOIN Mekanlar m ON z.mekan_id = m.id
                       JOIN Sehirler s ON m.sehir_id = s.id
                       WHERE z.kullanici_id = ? ORDER BY z.id DESC'''
            cursor.execute(sorgu, (self.parent.aktif_kullanici_id,))
            ziyaretler = cursor.fetchall()
            conn.close()

            # --- DÜZELTİLMİŞ İSTATİSTİK HESAPLAMALARI ---
            essiz_mekanlar = set()
            kategori_sayilari = {}
            gecerli_puanlar = []

            for z in ziyaretler:
                mekan_adi = z[1]
                kat = z[2]
                puan = z[3]
                
                # Sadece 0'dan büyük puanları ortalamaya dahil et
                if puan > 0:
                    gecerli_puanlar.append(puan)
                
                # Mekan sayısını ve kategori dağılımını şişirmemek için eşsiz kontrolü
                if mekan_adi not in essiz_mekanlar:
                    essiz_mekanlar.add(mekan_adi)
                    kategori_sayilari[kat] = kategori_sayilari.get(kat, 0) + 1

            toplam_mekan = len(essiz_mekanlar)
            ortalama_puan = sum(gecerli_puanlar) / len(gecerli_puanlar) if len(gecerli_puanlar) > 0 else 0

            grafik_html = '<table width="100%" cellpadding="4" cellspacing="0" style="margin-top:10px; border:none;">'
            renkler = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"]
            renk_idx = 0
            
            for kat, sayi in kategori_sayilari.items():
                yuzde = int((sayi / toplam_mekan) * 100) if toplam_mekan > 0 else 0
                renk = renkler[renk_idx % len(renkler)]
                
                grafik_html += f"""
                <tr style="background-color:transparent;">
                    <td width="30%" style="font-size:13px; font-weight:bold; border:none; padding:5px 0;">{kat} (%{yuzde})</td>
                    <td width="70%" style="border:none; padding:5px 0;">
                        <table width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #bdc3c7; background-color:#edf2f4;">
                            <tr>
                                <td width="{yuzde}%" bgcolor="{renk}" height="14" style="border:none;"></td>
                                <td width="{100-yuzde}%" bgcolor="#edf2f4" style="border:none;"></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                """
                renk_idx += 1
            grafik_html += "</table>"

            html_icerik = f"""
            <html>
            <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #2c3e50; }}
                h1 {{ color: #2c3e50; text-align: center; font-size: 26px; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 15px; }}
                .ozet-tablo {{ width: 100%; margin-bottom: 20px; }}
                .ozet-kutusu {{ background-color: #f8f9fa; padding: 12px; border: 1px solid #e9ecef; text-align: center; }}
                .ozet-kutusu h3 {{ margin: 5px 0 0 0; color: #2980b9; font-size: 20px; }}
                .ozet-kutusu p {{ margin: 0; font-size: 12px; color: #7f8c8d; }}
                .ana-tablo {{ border-collapse: collapse; width: 100%; font-size: 13px; margin-top: 15px; }}
                .ana-tablo th {{ background-color: #34495e; color: white; padding: 10px; text-align: left; font-weight: bold; }}
                .ana-tablo td {{ border-bottom: 1px solid #e2e8f0; padding: 8px; color: #2d3748; }}
            </style>
            </head>
            <body>
                <h1>🌍 {self.parent.aktif_kullanici_adi.capitalize()} - Seyahat Raporu</h1>
                
                <table class="ozet-tablo" cellspacing="10" cellpadding="0">
                    <tr>
                        <td width="50%" style="border:none;">
                            <div class="ozet-kutusu">
                                <p>Eşsiz Ziyaret Edilen Mekan</p>
                                <h3>🗺️ {toplam_mekan} Rota</h3>
                            </div>
                        </td>
                        <td width="50%" style="border:none;">
                            <div class="ozet-kutusu">
                                <p>Ortalama Seyahat Puanı</p>
                                <h3>⭐ {ortalama_puan:.1f} / 5.0</h3>
                            </div>
                        </td>
                    </tr>
                </table>

                <h3 style="background-color:transparent; color:#2c3e50; font-size:16px; margin-top:15px; margin-bottom:5px; border-bottom:1px solid #ddd; padding-bottom:4px;">📊 Kategori Dağılım Grafiği</h3>
                {grafik_html}

                <h3 style="background-color:transparent; color:#2c3e50; font-size:16px; margin-top:25px; margin-bottom:5px; border-bottom:1px solid #ddd; padding-bottom:4px;">📌 Detaylı Seyahat Geçmişi</h3>
                <table class="ana-tablo">
                    <tr>
                        <th>Şehir</th>
                        <th>Mekan Adı</th>
                        <th>Kategori</th>
                        <th>Puan</th>
                        <th>Yorum</th>
                    </tr>
            """
            for s_adi, m_adi, sezon, puan, yorum in ziyaretler:
                puan_gorsel = '★' * puan if puan > 0 else 'Puan Yok'
                yorum_metni = yorum if yorum else '-'
                html_icerik += f"<tr><td>{s_adi}</td><td>{m_adi}</td><td>{sezon}</td><td>{puan_gorsel}</td><td>{yorum_metni}</td></tr>"

            html_icerik += """
                </table>
                <p style="text-align: center; font-size: 11px; color: #a0aec0; margin-top: 35px;">
                    <i>Akıllı Gezi Rehberi © Raporlama Modülü tarafından oluşturulmuştur.</i>
                </p>
            </body>
            </html>
            """
            
            yazici = QPrinter(QPrinter.ScreenResolution)
            yazici.setOutputFormat(QPrinter.PdfFormat)
            yazici.setOutputFileName(dosya_yolu)
            yazici.setPageSize(QPrinter.A4) 
            yazici.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter) 

            dokuman = QTextDocument()
            dokuman.setHtml(html_icerik)
            dokuman.print_(yazici)

            QMessageBox.information(self, "Başarılı", f"Grafikli Seyahat Raporunuz PDF olarak başarıyla kaydedildi!\n\nDosya: {dosya_yolu}")
        
        except Exception as e:
            QMessageBox.critical(self, "Kritik Hata", f"PDF oluşturulurken sistemsel bir hata oluştu:\n{str(e)}")

class SehirSecimEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 30)
        self.baslik = QLabel("<h2>Şehirler</h2>")
        layout.addWidget(self.baslik)
        
        self.sehir_listesi = QListWidget()
        self.sehir_listesi.itemDoubleClicked.connect(self.sehir_detayina_git)
        layout.addWidget(self.sehir_listesi)
        self.setLayout(layout)

    def sehirleri_yukle(self, sezon):
        self.baslik.setText(f"<h2>{sezon}</h2>")
        self.sehir_listesi.clear()
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        sorgu = '''
            SELECT s.id, s.sehir_adi, IFNULL(AVG(NULLIF(z.puan, 0)), 0) as ort_puan
            FROM Sehirler s JOIN Mekanlar m ON s.id = m.sehir_id
            LEFT JOIN Ziyaret_ve_Puanlama z ON m.id = z.mekan_id
            WHERE m.sezon = ? GROUP BY s.id ORDER BY ort_puan DESC
        '''
        cursor.execute(sorgu, (sezon,))
        for satir in cursor.fetchall():
            item = QListWidgetItem(f"📍 {satir[1]} (Puan: {round(satir[2], 1)})")
            item.setData(Qt.UserRole, (satir[0], satir[1])) 
            self.sehir_listesi.addItem(item)
        conn.close()

    def sehir_detayina_git(self, item):
        sehir_id, sehir_adi = item.data(Qt.UserRole)
        self.parent.sayfa_mekanlar.mekanlari_yukle(sehir_id, sehir_adi, self.parent.secili_sezon)
        self.parent.ekran_degistir(4)

class MekanlarEkran(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.secili_sehir_id = None
        self.secili_sehir_adi = ""
        self.secili_sezon = None
        self.secili_mekan_id = None 
        
        ana_layout = QHBoxLayout()
        ana_layout.setContentsMargins(30, 20, 30, 30)
        ana_layout.setSpacing(20) 

        sol_panel = QWidget()
        sol_layout = QVBoxLayout(sol_panel)
        sol_layout.setContentsMargins(0, 0, 0, 0)
        
        self.baslik = QLabel("<h2>Mekanlar</h2>")
        sol_layout.addWidget(self.baslik)

        self.mekan_listesi = QListWidget()
        self.mekan_listesi.setMinimumWidth(250)
        self.mekan_listesi.setMaximumWidth(350)
        self.mekan_listesi.itemClicked.connect(self.mekan_detaylarini_getir)
        sol_layout.addWidget(self.mekan_listesi)
        
        sag_panel = QWidget()
        sag_layout = QVBoxLayout(sag_panel)
        sag_layout.setContentsMargins(0, 0, 0, 0)
        
        self.lbl_detay_baslik = QLabel("<h2>Mekan Detayı</h2>")
        sag_layout.addWidget(self.lbl_detay_baslik)
        
        self.gorsel_etiket = QLabel("Sol taraftan bir mekan seçin...")
        self.gorsel_etiket.setAlignment(Qt.AlignCenter)
        self.gorsel_etiket.setMinimumHeight(180)
        self.gorsel_etiket.setStyleSheet("background-color: rgba(128, 128, 128, 0.1); border-radius: 8px; border: 1px dashed gray;")
        sag_layout.addWidget(self.gorsel_etiket)

        link_layout = QHBoxLayout()
        
        self.btn_bilgi = QPushButton("ℹ️ Hakkında Bilgi Al")
        self.btn_bilgi.setCursor(Qt.PointingHandCursor)
        self.btn_bilgi.clicked.connect(self.mekan_bilgisi_goster)
        
        self.btn_google = QPushButton("🌍 İnternette Ara")
        self.btn_google.setCursor(Qt.PointingHandCursor)
        self.btn_google.clicked.connect(self.internette_ara)
        
        self.btn_harita = QPushButton("🗺️ Haritada Gör")
        self.btn_harita.setCursor(Qt.PointingHandCursor)
        self.btn_harita.clicked.connect(self.haritada_gor)
        
        self.btn_bilgi.setEnabled(False)
        self.btn_google.setEnabled(False) 
        self.btn_harita.setEnabled(False)
        
        link_layout.addWidget(self.btn_bilgi)
        link_layout.addWidget(self.btn_google)
        link_layout.addWidget(self.btn_harita)
        link_layout.addStretch()
        sag_layout.addLayout(link_layout)

        sag_layout.addSpacing(10)
        
        listeler_layout = QHBoxLayout()
        
        puan_panel = QVBoxLayout()
        puan_panel.addWidget(QLabel("<b>Kullanıcı Puanları:</b>"))
        self.puan_listesi = QListWidget()
        self.puan_listesi.setMinimumWidth(160)
        self.puan_listesi.setMaximumWidth(180)
        puan_panel.addWidget(self.puan_listesi)
        
        yorum_panel = QVBoxLayout()
        yorum_panel.addWidget(QLabel("<b>Kullanıcı Yorumları:</b>"))
        self.yorum_listesi = QListWidget()
        yorum_panel.addWidget(self.yorum_listesi)
        
        listeler_layout.addLayout(puan_panel)
        listeler_layout.addLayout(yorum_panel)
        sag_layout.addLayout(listeler_layout)

        degerlendirme_box = QGroupBox("Değerlendirme ve Yorum Alanı")
        degerlendirme_layout = QVBoxLayout(degerlendirme_box)
        degerlendirme_layout.setContentsMargins(15, 15, 15, 15)
        degerlendirme_layout.setSpacing(12)

        puan_satir = QHBoxLayout()
        puan_satir.addWidget(QLabel("Senin Puanın:"))
        self.puan_spin = QSpinBox()
        self.puan_spin.setRange(0, 5) 
        self.puan_spin.setSpecialValueText("Puan Yok")
        self.puan_spin.setMinimumWidth(110) 
        self.puan_spin.setMinimumHeight(35)
        puan_satir.addWidget(self.puan_spin)
        
        self.btn_puan_kaydet = QPushButton("⭐ Puanı Kaydet")
        self.btn_puan_kaydet.setObjectName("VurguluBtn")
        self.btn_puan_kaydet.setMinimumHeight(35)
        self.btn_puan_kaydet.clicked.connect(self.puan_kaydet_islemi)
        puan_satir.addWidget(self.btn_puan_kaydet)
        
        self.btn_puan_sil = QPushButton("🗑️ Puanı Sil")
        self.btn_puan_sil.setObjectName("SilBtn")
        self.btn_puan_sil.setMinimumHeight(35)
        self.btn_puan_sil.clicked.connect(self.puan_sil_islemi)
        self.btn_puan_sil.setVisible(False) 
        puan_satir.addWidget(self.btn_puan_sil)
        puan_satir.addStretch()
        degerlendirme_layout.addLayout(puan_satir)

        ayirici = QFrame()
        ayirici.setFrameShape(QFrame.HLine)
        ayirici.setFrameShadow(QFrame.Sunken)
        degerlendirme_layout.addWidget(ayirici)

        yorum_satir = QHBoxLayout()
        self.input_yorum = QLineEdit()
        self.input_yorum.setPlaceholderText("Bu mekan hakkında yeni bir yorum yaz...")
        self.input_yorum.setMinimumHeight(40)
        self.input_yorum.returnPressed.connect(self.yorum_ekle_islemi)
        yorum_satir.addWidget(self.input_yorum)
        
        btn_yorum_gonder = QPushButton("💬 Yorum Gönder")
        btn_yorum_gonder.setMinimumHeight(40)
        btn_yorum_gonder.clicked.connect(self.yorum_ekle_islemi)
        yorum_satir.addWidget(btn_yorum_gonder)
        degerlendirme_layout.addLayout(yorum_satir)

        sag_layout.addWidget(degerlendirme_box)

        ana_layout.addWidget(sol_panel)
        ana_layout.addWidget(sag_panel, 1) 
        
        self.setLayout(ana_layout)

    def varsayilan_kategori_gorseli_ciz(self, sezon, mekan_adi):
        pixmap = QPixmap(340, 180)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, 0, 180)
        if sezon == "Yaz Tatili":
            gradient.setColorAt(0, QColor("#4fc3f7"))
            gradient.setColorAt(1, QColor("#0288d1"))
            emoji = "🏝️"
        elif sezon == "Kış Tatili":
            gradient.setColorAt(0, QColor("#b2ebf2"))
            gradient.setColorAt(1, QColor("#0097a7"))
            emoji = "❄️"
        elif sezon == "Doğa & Kamp":
            gradient.setColorAt(0, QColor("#aed581"))
            gradient.setColorAt(1, QColor("#33691e"))
            emoji = "⛺"
        else: 
            gradient.setColorAt(0, QColor("#ffb74d"))
            gradient.setColorAt(1, QColor("#e65100"))
            emoji = "🏛️"
            
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 340, 180, 12, 12)
        
        font_emoji = QFont("Segoe UI Emoji", 34)
        painter.setFont(font_emoji)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(QRect(0, 20, 340, 60), Qt.AlignCenter, emoji)
        
        font_text = QFont("Segoe UI", 12, QFont.Bold)
        painter.setFont(font_text)
        painter.drawText(QRect(15, 90, 310, 30), Qt.AlignCenter, mekan_adi)
        
        font_sub = QFont("Segoe UI", 9)
        painter.setFont(font_sub)
        painter.setPen(QColor(255, 255, 255, 190))
        painter.drawText(QRect(15, 125, 310, 20), Qt.AlignCenter, f"{sezon} Önerilen Rota")
        
        painter.end()
        return pixmap

    def mekanlari_yukle(self, sehir_id, sehir_adi, sezon):
        self.secili_sehir_id = sehir_id
        self.secili_sehir_adi = sehir_adi
        self.secili_sezon = sezon
        self.secili_mekan_id = None
        self.baslik.setText(f"<h2>{sehir_adi}</h2>")
        self.lbl_detay_baslik.setText("<h2>Mekan Detayı</h2>")
        
        self.btn_bilgi.setEnabled(False)
        self.btn_google.setEnabled(False)
        self.btn_harita.setEnabled(False)
        self.gorsel_etiket.clear()
        self.gorsel_etiket.setText("Sol taraftan bir mekan seçin...")
        self.gorsel_etiket.setStyleSheet("background-color: rgba(128, 128, 128, 0.1); border-radius: 8px; border: 1px dashed gray;")
        
        self.input_yorum.clear()
        self.puan_spin.setValue(0)
        self.btn_puan_sil.setVisible(False)
        self.btn_puan_kaydet.setText("⭐ Puanı Kaydet")
        
        self.liste_guncelle()
        self.yorum_listesi.clear()
        self.puan_listesi.clear()

    def liste_guncelle(self):
        self.mekan_listesi.clear()
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        sorgu = '''
            SELECT m.id, m.mekan_adi, m.butce, IFNULL(AVG(NULLIF(z.puan, 0)), 0) as ort_puan
            FROM Mekanlar m LEFT JOIN Ziyaret_ve_Puanlama z ON m.id = z.mekan_id
            WHERE m.sehir_id = ? AND m.sezon = ?
            GROUP BY m.id ORDER BY ort_puan DESC
        '''
        cursor.execute(sorgu, (self.secili_sehir_id, self.secili_sezon))
        for m in cursor.fetchall():
            item = QListWidgetItem(f"{m[1]}\nBütçe: {m[2]} | Puan: {round(m[3], 1)}")
            item.setData(Qt.UserRole, m[0])
            self.mekan_listesi.addItem(item)
        conn.close()

    def kullanicinin_eski_puanini_getir(self, mekan_id):
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("SELECT puan FROM Ziyaret_ve_Puanlama WHERE kullanici_id=? AND mekan_id=? AND puan > 0", 
                       (self.parent.aktif_kullanici_id, mekan_id))
        kayit = cursor.fetchone()
        conn.close()

        if kayit:
            self.puan_spin.setValue(kayit[0])
            self.btn_puan_sil.setVisible(True)
            self.btn_puan_kaydet.setText("⭐ Puanı Güncelle")
        else:
            self.puan_spin.setValue(0)
            self.btn_puan_sil.setVisible(False)
            self.btn_puan_kaydet.setText("⭐ Puanı Kaydet")

    def mekan_detaylarini_getir(self, item):
        self.secili_mekan_id = item.data(Qt.UserRole)
        mekan_adi = item.text().split("\n")[0]
        
        self.lbl_detay_baslik.setText(f"<h2>{mekan_adi}</h2>")
        self.btn_bilgi.setEnabled(True)
        self.btn_google.setEnabled(True)
        self.btn_harita.setEnabled(True)
        
        self.yorumlari_getir(self.secili_mekan_id)
        self.kullanicinin_eski_puanini_getir(self.secili_mekan_id)
        
        self.gorsel_etiket.setStyleSheet("border: none;")
        self.gorsel_etiket.setPixmap(self.varsayilan_kategori_gorseli_ciz(self.secili_sezon, mekan_adi))

    def mekan_bilgisi_goster(self):
        secili_item = self.mekan_listesi.currentItem()
        if not secili_item: return
        mekan_adi = secili_item.text().split("\n")[0]

        dialog = QDialog(self)
        dialog.setWindowTitle(f"{mekan_adi} Rehberi")
        dialog.resize(550, 500)
        dialog.setStyleSheet(self.parent.styleSheet())

        layout = QVBoxLayout(dialog)
        
        text_browser = QTextBrowser()
        text_browser.setHtml(f"<div style='text-align:center; padding-top:40px;'><h3 style='color:#3498db;'>{mekan_adi} Aranıyor...</h3><p>Wikipedia kütüphanesi taranıyor, lütfen bekleyin.</p></div>")
        layout.addWidget(text_browser)

        btn_kapat = QPushButton("Kapat")
        btn_kapat.setMinimumHeight(40)
        btn_kapat.clicked.connect(dialog.accept)
        layout.addWidget(btn_kapat)

        dialog.show()
        QApplication.processEvents() 

        try:
            basliklar = {'User-Agent': 'GeziRehberiProjesi/1.0'}
            arama_url = "https://tr.wikipedia.org/w/api.php"
            
            arama_param = {"action": "query", "list": "search", "srsearch": f'"{mekan_adi}"', "utf8": 1, "format": "json"}
            cevap_arama = requests.get(arama_url, params=arama_param, headers=basliklar, timeout=5)
            sonuclar = cevap_arama.json().get('query', {}).get('search', [])
            
            if not sonuclar:
                arama_param["srsearch"] = f"{mekan_adi} {self.secili_sehir_adi}"
                cevap_arama = requests.get(arama_url, params=arama_param, headers=basliklar, timeout=5)
                sonuclar = cevap_arama.json().get('query', {}).get('search', [])

            if len(sonuclar) > 0:
                gercek_baslik = sonuclar[0]['title'] 
                
                detay_param = {
                    "action": "query",
                    "prop": "extracts",
                    "titles": gercek_baslik,
                    "explaintext": 1, 
                    "format": "json",
                    "utf8": 1
                }
                cevap_detay = requests.get(arama_url, params=detay_param, headers=basliklar, timeout=5)
                sayfalar = cevap_detay.json().get('query', {}).get('pages', {})
                sayfa_verisi = list(sayfalar.values())[0]
                
                if 'extract' in sayfa_verisi:
                    tam_metin = sayfa_verisi['extract']
                    bolumler = tam_metin.split("\n==")
                    
                    ozet_ve_tarih = bolumler[0].strip()
                    gezilecek_metni = "Öne çıkan spesifik bir nokta belirtilmemiş, tamamını keşfedebilirsiniz."
                    ozellik_bulundu = False
                    
                    for bolum in bolumler[1:]:
                        if bolum.startswith("="): 
                            bolum = bolum.lstrip("=") 
                        
                        satirlar = bolum.split("\n", 1)
                        if len(satirlar) == 2:
                            bolum_basligi = satirlar[0].replace("=", "").strip().lower()
                            bolum_icerigi = satirlar[1].strip()
                            
                            if any(k in bolum_basligi for k in ["tarih", "geçmiş", "kuruluş"]):
                                ek_tarih = bolum_icerigi[:350] + "..." if len(bolum_icerigi) > 350 else bolum_icerigi
                                ozet_ve_tarih += f"\n\nTarihsel Not: {ek_tarih}"
                            
                            elif not ozellik_bulundu and any(k in bolum_basligi for k in ["gör", "özellik", "yapı", "bölüm", "coğraf", "mimari"]):
                                gezilecek_metni = bolum_icerigi[:450] + "..." if len(bolum_icerigi) > 450 else bolum_icerigi
                                ozellik_bulundu = True

                    ozet_ve_tarih = ozet_ve_tarih.replace('\n', '<br>')
                    gezilecek_metni = gezilecek_metni.replace('\n', '<br>')

                    html_gosterim = f"""
                    <div style='padding:10px; font-family: "Segoe UI", Arial, sans-serif;'>
                        <h2 style='color:#3498db; margin-top:0; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px;'>{gercek_baslik}</h2>
                        
                        <h4 style='color:#2c3e50; margin-bottom:5px;'>📖 Genel Bilgi ve Tarihi</h4>
                        <p style='font-size:13px; line-height:1.6; margin-top:0;'>{ozet_ve_tarih}</p>
                        
                        <h4 style='color:#27ae60; margin-bottom:5px; margin-top:15px;'>📸 Öne Çıkan Özellikler / Görülecek Yerler</h4>
                        <p style='font-size:13px; line-height:1.6; margin-top:0;'>{gezilecek_metni}</p>
                        
                        <p style='text-align:right; font-size:11px; color:#95a5a6; margin-top: 25px;'><i>Kaynak: Wikipedia API (Otomatik Ayıklama Modülü)</i></p>
                    </div>
                    """
                    text_browser.setHtml(html_gosterim)
                else:
                    text_browser.setHtml(f"<div style='text-align:center; padding-top:40px;'><h3>{mekan_adi}</h3><p>Şu an için detaylı metin çekilemedi.</p></div>")
            else:
                text_browser.setHtml(f"<div style='text-align:center; padding-top:40px;'><h3>{mekan_adi}</h3><p>Wikipedia kütüphanesinde tam eşleşen bir kayıt bulunamadı.</p></div>")
        except Exception:
            text_browser.setHtml(f"<div style='text-align:center; padding-top:40px;'><h3 style='color:#e74c3c;'>Bağlantı Hatası</h3><p>Wikipedia sunucularına ulaşılamadı. İnternet bağlantınızı kontrol edin.</p></div>")

    def internette_ara(self):
        secili_item = self.mekan_listesi.currentItem()
        if secili_item:
            mekan_adi = secili_item.text().split("\n")[0]
            url = f"https://www.google.com/search?q={mekan_adi}+{self.secili_sehir_adi}+gezilecek+yerler"
            QDesktopServices.openUrl(QUrl(url))

    def haritada_gor(self):
        secili_item = self.mekan_listesi.currentItem()
        if secili_item:
            mekan_adi = secili_item.text().split("\n")[0]
            url = f"https://www.google.com/maps/search/?api=1&query={mekan_adi}+{self.secili_sehir_adi}"
            QDesktopServices.openUrl(QUrl(url))

    def yorumlari_getir(self, mekan_id):
        self.yorum_listesi.clear()
        self.puan_listesi.clear()
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT k.kullanici_adi, z.puan, z.yorum FROM Ziyaret_ve_Puanlama z
                          JOIN Kullanicilar k ON z.kullanici_id = k.id
                          WHERE z.mekan_id = ?''', (mekan_id,))
        kayitlar = cursor.fetchall()
        conn.close()
        
        puan_var, yorum_var = False, False
        gosterilen_puanlar = set() 
        
        for y in kayitlar:
            k_adi, puan, yorum = y[0], y[1], y[2]
            
            if puan > 0 and k_adi not in gosterilen_puanlar:
                self.puan_listesi.addItem(f"👤 {k_adi}: {'★' * puan}")
                gosterilen_puanlar.add(k_adi)
                puan_var = True
                
            if i := (yorum and yorum.strip()):
                self.yorum_listesi.addItem(f"👤 {k_adi}: {yorum}")
                yorum_var = True
                
        if not puan_var: self.puan_listesi.addItem("Henüz puan yok.")
        if not yorum_var: self.yorum_listesi.addItem("Henüz yorum yapılmamış.")

    def puan_kaydet_islemi(self):
        if not self.secili_mekan_id: return
        puan = self.puan_spin.value()
        if puan == 0: 
            QMessageBox.information(self, "Bilgi", "Lütfen kaydetmek için 1-5 arası bir puan seçin.")
            return

        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Ziyaret_ve_Puanlama WHERE kullanici_id=? AND mekan_id=? AND puan > 0", 
                       (self.parent.aktif_kullanici_id, self.secili_mekan_id))
        kayit = cursor.fetchone()
        
        if kayit:
            cursor.execute("UPDATE Ziyaret_ve_Puanlama SET puan=? WHERE id=?", (puan, kayit[0]))
        else:
            cursor.execute("INSERT INTO Ziyaret_ve_Puanlama (kullanici_id, mekan_id, puan, yorum) VALUES (?, ?, ?, '')", 
                           (self.parent.aktif_kullanici_id, self.secili_mekan_id, puan))
            
        conn.commit()
        conn.close()
        
        self.btn_puan_sil.setVisible(True)
        self.btn_puan_kaydet.setText("⭐ Puanı Güncelle")
        self.liste_guncelle()
        self.yorumlari_getir(self.secili_mekan_id)
        
    def puan_sil_islemi(self):
        if not self.secili_mekan_id: return
        cevap = QMessageBox.question(self, 'Sil', "Puanınızı kalıcı olarak geri çekmek istiyor musunuz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if cevap == QMessageBox.Yes:
            conn = sqlite3.connect('akilli_rehber.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Ziyaret_ve_Puanlama WHERE kullanici_id=? AND mekan_id=? AND puan > 0", (self.parent.aktif_kullanici_id, self.secili_mekan_id))
            conn.commit()
            conn.close()
            
            self.puan_spin.setValue(0)
            self.btn_puan_sil.setVisible(False)
            self.btn_puan_kaydet.setText("⭐ Puanı Kaydet")
            self.liste_guncelle()
            self.yorumlari_getir(self.secili_mekan_id)

    def yorum_ekle_islemi(self):
        if not self.secili_mekan_id: return
        yorum_metni = self.input_yorum.text().strip()
        if yorum_metni == "": return
        
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ziyaret_ve_Puanlama (kullanici_id, mekan_id, puan, yorum) VALUES (?, ?, 0, ?)", (self.parent.aktif_kullanici_id, self.secili_mekan_id, yorum_metni))
        conn.commit()
        conn.close()
        
        self.input_yorum.clear()
        self.yorumlari_getir(self.secili_mekan_id)

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 850, 650) 
        
        self.ayarlar = QSettings("GeziRehberiProjesi", "Ayarlar")
        kayitli_tema = self.ayarlar.value("karanlik_mod", "false")
        self.karanlik_mod = (kayitli_tema == "true")
        
        if self.karanlik_mod: self.setStyleSheet(TEMA_KARANLIK)
        else: self.setStyleSheet(TEMA_AYDINLIK)
        
        self.aktif_kullanici_id = None
        self.aktif_kullanici_adi = None
        self.secili_sezon = ""

        self.ana_widget = QWidget()
        self.ana_widget.setObjectName("AnaKapsayici") 
        self.setCentralWidget(self.ana_widget)
        ana_layout = QVBoxLayout(self.ana_widget)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(0)

        self.baslik_cubugu = OzelBaslikCubugu(self)
        ana_layout.addWidget(self.baslik_cubugu)

        self.ust_bar = QWidget()
        self.ust_bar.setObjectName("UstBar")
        ust_bar_layout = QHBoxLayout(self.ust_bar)
        ust_bar_layout.setContentsMargins(20, 10, 20, 10)
        
        self.lbl_kullanici_isim = QLabel("Merhaba, Misafir")
        self.lbl_kullanici_isim.setStyleSheet("font-weight: 500;")
        
        self.btn_ana_sayfa = QPushButton("Ana Sayfa")
        self.btn_ana_sayfa.setCursor(Qt.PointingHandCursor)
        self.btn_ana_sayfa.clicked.connect(lambda: self.ekran_degistir(2) if self.aktif_kullanici_id else None)
        
        self.btn_profil_git = QPushButton("Kişisel Alan")
        self.btn_profil_git.setCursor(Qt.PointingHandCursor)
        self.btn_profil_git.clicked.connect(lambda: self.ekran_degistir(5) if self.aktif_kullanici_id else None)

        self.btn_tema = QPushButton("☀️ Aydınlık Mod" if self.karanlik_mod else "🌙 Karanlık Mod")
        self.btn_tema.setCursor(Qt.PointingHandCursor)
        self.btn_tema.clicked.connect(self.tema_degistir)
        
        ust_bar_layout.addWidget(self.lbl_kullanici_isim)
        ust_bar_layout.addSpacing(20)
        ust_bar_layout.addWidget(self.btn_ana_sayfa)
        ust_bar_layout.addWidget(self.btn_profil_git)
        ust_bar_layout.addStretch()
        ust_bar_layout.addWidget(self.btn_tema)
        
        self.ekran_kutusu = QStackedWidget()
        
        self.sayfa_giris = GirisEkran(self)
        self.sayfa_kayit = KayitEkran(self)
        self.sayfa_ana = AnaEkran(self)
        self.sayfa_sehirler = SehirSecimEkran(self)
        self.sayfa_mekanlar = MekanlarEkran(self)
        self.sayfa_profil = ProfilEkran(self) 
        
        self.ekran_kutusu.addWidget(self.sayfa_giris)    
        self.ekran_kutusu.addWidget(self.sayfa_kayit)    
        self.ekran_kutusu.addWidget(self.sayfa_ana)      
        self.ekran_kutusu.addWidget(self.sayfa_sehirler) 
        self.ekran_kutusu.addWidget(self.sayfa_mekanlar) 
        self.ekran_kutusu.addWidget(self.sayfa_profil)   

        ana_layout.addWidget(self.ust_bar)
        ana_layout.addWidget(self.ekran_kutusu)
        self.ust_bar_guncelle(False)
        self.arka_plani_guncelle() 

    def ust_bar_guncelle(self, giris_yapildi):
        self.btn_ana_sayfa.setVisible(giris_yapildi)
        self.btn_profil_git.setVisible(giris_yapildi)

    def arka_plani_guncelle(self):
        renk = "#121212" if self.karanlik_mod else "#FAFAFA"
        self.ana_widget.setStyleSheet(f"#AnaKapsayici {{ background-color: {renk}; }}")

    def tema_degistir(self):
        if self.karanlik_mod:
            self.setStyleSheet(TEMA_AYDINLIK)
            self.btn_tema.setText("🌙 Karanlık Mod")
            self.karanlik_mod = False
            self.ayarlar.setValue("karanlik_mod", "false")
        else:
            self.setStyleSheet(TEMA_KARANLIK)
            self.btn_tema.setText("☀️ Aydınlık Mod")
            self.karanlik_mod = True
            self.ayarlar.setValue("karanlik_mod", "true")
        self.arka_plani_guncelle()

    def rulo_ve_sezon_sec(self, sezon):
        self.secili_sezon = sezon
        self.sayfa_sehirler.sehirleri_yukle(sezon)
        self.ekran_degistir(3)

    def sezon_sec(self, sezon):
        self.secili_sezon = sezon
        self.sayfa_sehirler.sehirleri_yukle(sezon)
        self.ekran_degistir(3)

    def ekran_degistir(self, index):
        if index == 0 or index == 1:
            self.ust_bar_guncelle(False)
            self.lbl_kullanici_isim.setText("Merhaba, Misafir")
            self.aktif_kullanici_id = None
        else: self.ust_bar_guncelle(True)
        
        if index == 5: self.sayfa_profil.kompleteri_ve_notlari_yukle()
        self.ekran_kutusu.setCurrentIndex(index)

if __name__ == "__main__":
    print("Sistem başlatılıyor...")
    try:
        veritabani_olustur() 
        app = QApplication(sys.argv)
        pencere = AnaPencere()
        pencere.show()
        print("Arayüz başarıyla açıldı!")
        sys.exit(app.exec_())
    except Exception as e: print(f"KRİTİK HATA OLUŞTU: {e}")