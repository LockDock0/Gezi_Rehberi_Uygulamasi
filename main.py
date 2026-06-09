import sys
import sqlite3
import requests
import csv
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter # PDF çıktısı için eklendi
from database import veritabani_olustur

# --- ANYTYPE TARZI AYDINLIK TEMA ---
TEMA_AYDINLIK = """
QWidget { background-color: #FAFAFA; color: #111111; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 14px; }
QLabel { color: #222222; }
QLabel h1, QLabel h2, QLabel h3 { font-weight: 600; color: #000000; letter-spacing: -0.5px; }
QPushButton { background-color: #FFFFFF; color: #111111; border: 1px solid #EAEAEA; border-radius: 8px; padding: 10px 18px; font-weight: 500; }
QPushButton:hover { background-color: #F0F0F0; border: 1px solid #DDDDDD; }
QPushButton:pressed { background-color: #E5E5E5; }
QPushButton#VurguluBtn { background-color: #111111; color: #FFFFFF; border: none; }
QPushButton#VurguluBtn:hover { background-color: #333333; }
QLineEdit, QSpinBox, QTextBrowser, QComboBox { background-color: #FFFFFF; border: 1px solid #EAEAEA; border-radius: 8px; padding: 12px; color: #111111; selection-background-color: #D3E2FD; selection-color: #111111; }
QLineEdit:focus, QSpinBox:focus, QTextBrowser:focus, QComboBox:focus { border: 1px solid #A0A0A0; }
QListWidget { background-color: transparent; border: none; outline: 0; }
QListWidget::item { padding: 14px; margin-bottom: 4px; border-radius: 8px; background-color: #FFFFFF; border: 1px solid #EAEAEA; }
QListWidget::item:selected { background-color: #F0F4FF; color: #111111; border: 1px solid #D3E2FD; font-weight: 500; }
QTabWidget::pane { border: none; background: transparent; top: 10px; }
QTabBar::tab { background: transparent; border: none; padding: 10px 15px; min-width: 140px; margin-right: 5px; color: #666666; font-weight: 500; font-size: 14px; border-bottom: 2px solid transparent; }
QTabBar::tab:selected { color: #111111; border-bottom: 2px solid #111111; font-weight: 600; }
QTabBar::tab:hover:!selected { color: #333333; }
QTableWidget { background-color: #FFFFFF; border: 1px solid #EAEAEA; border-radius: 8px; gridline-color: #EAEAEA; }
QHeaderView::section { background-color: #F0F0F0; padding: 8px; border: 1px solid #EAEAEA; font-weight: bold; }
#UstBar { background-color: #FFFFFF; border-bottom: 1px solid #EAEAEA; }
#OzelBaslik { background-color: #FFFFFF; }
#BaslikBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #111111; }
#BaslikBtn:hover { background-color: #EAEAEA; }
#KapatBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #111111; }
#KapatBtn:hover { background-color: #E81123; color: white; }
"""

# --- ANYTYPE TARZI KARANLIK TEMA (DARK MODE) ---
TEMA_KARANLIK = """
QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 14px; }
QLabel { color: #E0E0E0; }
QLabel h1, QLabel h2, QLabel h3 { font-weight: 600; color: #FFFFFF; letter-spacing: -0.5px; }
QPushButton { background-color: #1E1E1E; color: #E0E0E0; border: 1px solid #2A2A2A; border-radius: 8px; padding: 10px 18px; font-weight: 500; }
QPushButton:hover { background-color: #2C2C2C; border: 1px solid #3A3A3A; }
QPushButton:pressed { background-color: #3A3A3A; }
QPushButton#VurguluBtn { background-color: #E0E0E0; color: #121212; border: none; }
QPushButton#VurguluBtn:hover { background-color: #FFFFFF; }
QLineEdit, QSpinBox, QTextBrowser, QComboBox { background-color: #1E1E1E; border: 1px solid #2A2A2A; border-radius: 8px; padding: 12px; color: #E0E0E0; selection-background-color: #4A4A4A; selection-color: #FFFFFF; }
QLineEdit:focus, QSpinBox:focus, QTextBrowser:focus, QComboBox:focus { border: 1px solid #555555; }
QListWidget { background-color: transparent; border: none; outline: 0; }
QListWidget::item { padding: 14px; margin-bottom: 4px; border-radius: 8px; background-color: #1A1A1A; border: 1px solid #222222; }
QListWidget::item:selected { background-color: #2A2A35; color: #FFFFFF; border: 1px solid #4A4A5A; font-weight: 500; }
QTabWidget::pane { border: none; background: transparent; top: 10px; }
QTabBar::tab { background: transparent; border: none; padding: 10px 15px; min-width: 140px; margin-right: 5px; color: #888888; font-weight: 500; font-size: 14px; border-bottom: 2px solid transparent; }
QTabBar::tab:selected { color: #FFFFFF; border-bottom: 2px solid #FFFFFF; font-weight: 600; }
QTabBar::tab:hover:!selected { color: #AAAAAA; }
QTableWidget { background-color: #1A1A1A; border: 1px solid #222222; border-radius: 8px; gridline-color: #2A2A2A; }
QHeaderView::section { background-color: #222222; padding: 8px; border: 1px solid #2A2A2A; font-weight: bold; color: white; }
#UstBar { background-color: #1A1A1A; border-bottom: 1px solid #222222; }
#OzelBaslik { background-color: #1A1A1A; }
#BaslikBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #E0E0E0; }
#BaslikBtn:hover { background-color: #2A2A2A; }
#KapatBtn { background-color: transparent; border: none; padding: 5px; border-radius: 0px; font-size: 14px; color: #E0E0E0; }
#KapatBtn:hover { background-color: #E81123; color: white; }
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
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (k_adi, sifre))
        kullanici = cursor.fetchone()
        conn.close()

        if kullanici:
            self.parent.aktif_kullanici_id = kullanici[0]
            self.parent.aktif_kullanici_adi = k_adi
            self.parent.lbl_kullanici_isim.setText(f"👤 {k_adi}")
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
        self.liste_gidilecek = QListWidget()
        self.liste_gidilen = QListWidget()
        self.liste_genel = QListWidget()
        self.liste_puanlar = QListWidget() 
        
        # --- YENİ İSTATİSTİK TABLOSU EKLENTİSİ ---
        self.tablo_gecmis = QTableWidget()
        self.tablo_gecmis.setColumnCount(5)
        self.tablo_gecmis.setHorizontalHeaderLabels(["Şehir", "Mekan", "Kategori (Sezon)", "Bütçe", "Verilen Puan"])
        self.tablo_gecmis.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo_gecmis.setEditTriggers(QAbstractItemView.NoEditTriggers) # Tablonun değiştirilmesini engelle
        self.tablo_gecmis.setSelectionBehavior(QAbstractItemView.SelectRows) # Tıklayınca tüm satırı seç
        
        self.sekmeler.addTab(self.liste_gidilecek, "Gidilecek Yerler")
        self.sekmeler.addTab(self.liste_gidilen, "Gidilen Yerler")
        self.sekmeler.addTab(self.liste_genel, "Genel Notlar")
        self.sekmeler.addTab(self.liste_puanlar, "Değerlendirmeler")
        self.sekmeler.addTab(self.tablo_gecmis, "📊 Tüm İstatistikler") # Tablo eklendi
        
        layout.addWidget(self.sekmeler)

        layout.addSpacing(10)
        not_ekleme_layout = QHBoxLayout()
        
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(["Gidilecek Yerler", "Gidilen Yerler", "Genel Notlar"])
        self.kategori_combo.setMinimumHeight(45)
        
        self.input_not = QLineEdit()
        self.input_not.setPlaceholderText("Şehir veya mekan adı yaz, otomatik tamamlansın...")
        self.input_not.setMinimumHeight(45)
        
        btn_not_ekle = QPushButton("Ekle")
        btn_not_ekle.setObjectName("VurguluBtn")
        btn_not_ekle.setMinimumHeight(45)
        btn_not_ekle.clicked.connect(self.not_ekle)
        
        not_ekleme_layout.addWidget(self.kategori_combo)
        not_ekleme_layout.addWidget(self.input_not)
        not_ekleme_layout.addWidget(btn_not_ekle)
        layout.addLayout(not_ekleme_layout)
        self.setLayout(layout)

    def kompleteri_ve_notlari_yukle(self):
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        
        # Kelime Tamamlayıcı
        kelimeler = []
        cursor.execute("SELECT sehir_adi FROM Sehirler")
        kelimeler.extend([row[0] for row in cursor.fetchall()])
        cursor.execute("SELECT mekan_adi FROM Mekanlar")
        kelimeler.extend([row[0] for row in cursor.fetchall()])
        
        tamamlayici = QCompleter(kelimeler)
        tamamlayici.setCaseSensitivity(Qt.CaseInsensitive) 
        tamamlayici.setFilterMode(Qt.MatchContains) 
        self.input_not.setCompleter(tamamlayici)

        # Listeleri Temizle
        self.liste_gidilecek.clear()
        self.liste_gidilen.clear()
        self.liste_genel.clear()
        self.liste_puanlar.clear()
        self.tablo_gecmis.setRowCount(0)

        # Notları Çek
        cursor.execute("SELECT kategori, not_icerik, tarih FROM SeyahatNotlari WHERE kullanici_id = ?", (self.parent.aktif_kullanici_id,))
        for n in cursor.fetchall():
            kategori = n[0]
            metin = f"{n[1]} \n⏱️ {n[2].split()[0]}" 
            
            if kategori == "Gidilecek Yerler": self.liste_gidilecek.addItem(metin)
            elif kategori == "Gidilen Yerler": self.liste_gidilen.addItem(metin)
            else: self.liste_genel.addItem(metin)
            
        # Değerlendirmeleri ve Tablo Verisini Çek
        sorgu = '''SELECT s.sehir_adi, m.mekan_adi, m.sezon, m.butce, z.puan, z.yorum 
                   FROM Ziyaret_ve_Puanlama z
                   JOIN Mekanlar m ON z.mekan_id = m.id
                   JOIN Sehirler s ON m.sehir_id = s.id
                   WHERE z.kullanici_id = ?'''
        cursor.execute(sorgu, (self.parent.aktif_kullanici_id,))
        degerlendirmeler = cursor.fetchall()
        
        if not degerlendirmeler:
            self.liste_puanlar.addItem("Henüz mekan değerlendirmedin.")
        
        for row_idx, d in enumerate(degerlendirmeler):
            sehir_adi, mekan_adi, sezon, butce, puan, yorum = d
            
            # Liste İçin
            puan_str = f"{puan}/5" if puan > 0 else "Puan Yok"
            yrm_str = yorum if yorum else "Yorumsuz"
            self.liste_puanlar.addItem(f"{mekan_adi}\n⭐ {puan_str} | 💬 {yrm_str}")
            
            # Tablo İçin
            self.tablo_gecmis.insertRow(row_idx)
            self.tablo_gecmis.setItem(row_idx, 0, QTableWidgetItem(str(sehir_adi)))
            self.tablo_gecmis.setItem(row_idx, 1, QTableWidgetItem(str(mekan_adi)))
            self.tablo_gecmis.setItem(row_idx, 2, QTableWidgetItem(str(sezon)))
            self.tablo_gecmis.setItem(row_idx, 3, QTableWidgetItem(str(butce)))
            self.tablo_gecmis.setItem(row_idx, 4, QTableWidgetItem("⭐ " * puan if puan > 0 else "-"))
            
        conn.close()

    def not_ekle(self):
        yeni_not = self.input_not.text().strip()
        secilen_kategori = self.kategori_combo.currentText()
        if yeni_not == "": return
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SeyahatNotlari (kullanici_id, kategori, not_icerik) VALUES (?, ?, ?)", 
                       (self.parent.aktif_kullanici_id, secilen_kategori, yeni_not))
        conn.commit()
        conn.close()
        self.input_not.clear()
        self.kompleteri_ve_notlari_yukle() 

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
                       WHERE z.kullanici_id = ? ORDER BY z.puan DESC'''
            cursor.execute(sorgu, (self.parent.aktif_kullanici_id,))
            ziyaretler = cursor.fetchall()
            conn.close()

            # HTML PDF Şablonu
            html_icerik = f"""
            <html>
            <body style='font-family: Arial, sans-serif;'>
            <h1 style='color: #2c3e50; text-align: center;'>🌍 {self.parent.aktif_kullanici_adi.capitalize()} - Seyahat Portföyü</h1>
            <hr>
            <h3 style='color: #34495e;'>Değerlendirilen Mekanlar</h3>
            <table border='1' width='100%' cellspacing='0' cellpadding='8' style='border-collapse: collapse; font-size: 14px;'>
                <tr style='background-color: #34495e; color: white;'>
                    <th>Şehir</th>
                    <th>Mekan Adı</th>
                    <th>Kategori</th>
                    <th>Puan</th>
                </tr>
            """
            
            for s_adi, m_adi, sezon, puan, yorum in ziyaretler:
                puan_gorsel = '⭐' * puan if puan > 0 else '-'
                html_icerik += f"<tr><td>{s_adi}</td><td>{m_adi}</td><td>{sezon}</td><td align='center'>{puan_gorsel}</td></tr>"
            
            html_icerik += """
            </table><br>
            <p style='text-align: right; font-size: 11px; color: gray; margin-top: 20px;'>
            <i>Akıllı Gezi Rehberi &copy; Python ve PyQt5 ile oluşturulmuştur.</i></p>
            </body>
            </html>
            """

            # HTML'i PDF olarak yazdır
            yazici = QPrinter(QPrinter.HighResolution)
            yazici.setOutputFormat(QPrinter.PdfFormat)
            yazici.setOutputFileName(dosya_yolu)

            dokuman = QTextDocument()
            dokuman.setHtml(html_icerik)
            dokuman.print_(yazici)

            QMessageBox.information(self, "Başarılı", f"Kapsamlı Seyahat Raporunuz PDF olarak başarıyla kaydedildi!\n\nDosya: {dosya_yolu}")
        
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
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 30)
        self.baslik = QLabel("<h2>Mekanlar</h2>")
        layout.addWidget(self.baslik)

        self.mekan_listesi = QListWidget()
        self.mekan_listesi.setMaximumHeight(180)
        self.mekan_listesi.itemClicked.connect(self.mekan_detaylarini_getir)
        layout.addWidget(self.mekan_listesi)
        
        self.wiki_kutu = QTextBrowser()
        self.wiki_kutu.setMaximumHeight(80)
        self.wiki_kutu.setPlaceholderText("Listeden mekan seçtiğinde Wikipedia özeti buraya gelecek...")
        layout.addWidget(self.wiki_kutu)

        layout.addSpacing(10)
        self.yorum_listesi = QListWidget()
        self.yorum_listesi.setMinimumHeight(100) 
        layout.addWidget(self.yorum_listesi)

        islem_layout = QHBoxLayout()
        self.puan_spin = QSpinBox()
        self.puan_spin.setRange(0, 5) 
        self.puan_spin.setSpecialValueText("Puan Yok")
        self.puan_spin.setMinimumHeight(45)
        
        self.input_yorum = QLineEdit()
        self.input_yorum.setPlaceholderText("Yorum ekle...")
        self.input_yorum.setMinimumHeight(45)
        
        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.setObjectName("VurguluBtn")
        btn_kaydet.setMinimumHeight(45)
        btn_kaydet.clicked.connect(self.degerlendirme_yap)
        
        islem_layout.addWidget(QLabel("Puan:"))
        islem_layout.addWidget(self.puan_spin)
        islem_layout.addWidget(self.input_yorum, 1)
        islem_layout.addWidget(btn_kaydet)
        layout.addLayout(islem_layout)
        
        self.setLayout(layout)

    def mekanlari_yukle(self, sehir_id, sehir_adi, sezon):
        self.secili_sehir_id = sehir_id
        self.secili_sehir_adi = sehir_adi
        self.secili_sezon = sezon
        self.baslik.setText(f"<h2>{sehir_adi} Gezi Rehberi</h2>")
        self.liste_guncelle()
        self.yorum_listesi.clear()
        self.wiki_kutu.clear()

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

    def mekan_detaylarini_getir(self, item):
        mekan_id = item.data(Qt.UserRole)
        mekan_adi = item.text().split("\n")[0]
        
        self.yorumlari_getir(mekan_id)
        self.wiki_kutu.setText("İnternetten bilgi aranıyor...")
        QApplication.processEvents() 
        
        try:
            basliklar = {'User-Agent': 'GeziRehberiProjesi/1.0'}
            if self.secili_sezon == "Doğa & Kamp": arama_metni = f"{mekan_adi} {self.secili_sehir_adi} doğa tabiat göl kamp"
            elif self.secili_sezon == "Kültür Turu": arama_metni = f"{mekan_adi} {self.secili_sehir_adi} tarih antik müze örenyeri"
            else: arama_metni = f"{mekan_adi} {self.secili_sehir_adi}"
            
            arama_url = "https://tr.wikipedia.org/w/api.php"
            arama_param = {"action": "query", "list": "search", "srsearch": arama_metni, "utf8": 1, "format": "json"}
            
            cevap_arama = requests.get(arama_url, params=arama_param, headers=basliklar, timeout=5)
            arama_verisi = cevap_arama.json()
            sonuclar = arama_verisi.get('query', {}).get('search', [])
            
            if len(sonuclar) > 0:
                gercek_baslik = sonuclar[0]['title'] 
                detay_url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{gercek_baslik}"
                cevap = requests.get(detay_url, headers=basliklar, timeout=5)
                if cevap.status_code == 200:
                    self.wiki_kutu.setText(f"<b>{gercek_baslik}</b><br>{cevap.json().get('extract', 'Özet bulunamadı.')}")
                else:
                    self.wiki_kutu.setText("Bilgiler çekilemedi.")
            else:
                self.wiki_kutu.setText(f"Wikipedia'da eşleşen bir sonuç bulunamadı.")
        except Exception:
            self.wiki_kutu.setText("İnternet bağlantısı kurulamadı.")

    def yorumlari_getir(self, mekan_id):
        self.yorum_listesi.clear()
        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT k.kullanici_adi, z.puan, z.yorum FROM Ziyaret_ve_Puanlama z
                          JOIN Kullanicilar k ON z.kullanici_id = k.id
                          WHERE z.mekan_id = ? AND (z.yorum != '' OR z.puan > 0)''', (mekan_id,))
        yorumlar = cursor.fetchall()
        if not yorumlar:
            self.yorum_listesi.addItem("Henüz değerlendirme yapılmamış.")
        else:
            for y in yorumlar:
                puan_metni = f"{y[1]}/5" if y[1] > 0 else "Puan Yok"
                yorum_metni = y[2] if y[2] else "Sadece puan verildi."
                self.yorum_listesi.addItem(f"👤 {y[0]} ({puan_metni}): {yorum_metni}")
        conn.close()

    def degerlendirme_yap(self):
        secili_item = self.mekan_listesi.currentItem()
        if not secili_item: return
        mekan_id = secili_item.data(Qt.UserRole)
        puan = self.puan_spin.value()
        yorum = self.input_yorum.text().strip()
        
        if puan == 0 and yorum == "": return

        conn = sqlite3.connect('akilli_rehber.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ziyaret_ve_Puanlama (kullanici_id, mekan_id, puan, yorum) VALUES (?, ?, ?, ?)", 
                       (self.parent.aktif_kullanici_id, mekan_id, puan, yorum))
        conn.commit()
        conn.close()
        
        self.input_yorum.clear()
        self.puan_spin.setValue(0)
        
        self.liste_guncelle()
        self.yorumlari_getir(mekan_id)

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setGeometry(100, 100, 850, 650) 
        self.karanlik_mod = False
        self.setStyleSheet(TEMA_AYDINLIK)
        
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
        
        self.lbl_kullanici_isim = QLabel("👤 Misafir")
        self.lbl_kullanici_isim.setStyleSheet("font-weight: 500;")
        
        self.btn_ana_sayfa = QPushButton("Ana Sayfa")
        self.btn_ana_sayfa.setCursor(Qt.PointingHandCursor)
        self.btn_ana_sayfa.clicked.connect(lambda: self.ekran_degistir(2) if self.aktif_kullanici_id else None)
        
        self.btn_profil_git = QPushButton("Kişisel Alan")
        self.btn_profil_git.setCursor(Qt.PointingHandCursor)
        self.btn_profil_git.clicked.connect(lambda: self.ekran_degistir(5) if self.aktif_kullanici_id else None)

        self.btn_tema = QPushButton("🌙 Karanlık Mod")
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
        else:
            self.setStyleSheet(TEMA_KARANLIK)
            self.btn_tema.setText("☀️ Aydınlık Mod")
            self.karanlik_mod = True
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
            self.lbl_kullanici_isim.setText("👤 Misafir")
            self.aktif_kullanici_id = None
        else:
            self.ust_bar_guncelle(True)
        
        if index == 5:
            self.sayfa_profil.kompleteri_ve_notlari_yukle()

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
    except Exception as e:
        print(f"KRİTİK HATA OLUŞTU: {e}")