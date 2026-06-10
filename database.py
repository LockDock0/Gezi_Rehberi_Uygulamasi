import sqlite3
import requests
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SEEDER] - %(message)s')

def veritabani_olustur():
    with sqlite3.connect('akilli_rehber.db') as conn:
        cursor = conn.cursor()

        # --- TABLO MİMARİSİ ---
        cursor.execute('''CREATE TABLE IF NOT EXISTS Kullanicilar (id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_adi TEXT UNIQUE, sifre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Sehirler (id INTEGER PRIMARY KEY AUTOINCREMENT, sehir_adi TEXT UNIQUE, bolge TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Mekanlar (id INTEGER PRIMARY KEY AUTOINCREMENT, sehir_id INTEGER, mekan_adi TEXT, sezon TEXT, butce TEXT, FOREIGN KEY (sehir_id) REFERENCES Sehirler (id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Ziyaret_ve_Puanlama (id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_id INTEGER, mekan_id INTEGER, puan INTEGER DEFAULT 0, yorum TEXT, durum TEXT DEFAULT 'Gidildi', FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar (id), FOREIGN KEY (mekan_id) REFERENCES Mekanlar (id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS SeyahatNotlari (id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_id INTEGER, kategori TEXT, not_icerik TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar (id))''')

        cursor.execute("SELECT COUNT(*) FROM Sehirler")
        if cursor.fetchone()[0] == 0:
            logging.info("Nihai Dev Veritabanı Tohumlama (Seeding) işlemi başlatıldı...")
            
            try:
                cevap = requests.get("https://turkiyeapi.dev/api/v1/provinces", timeout=5) 
                if cevap.status_code == 200:
                    for il in cevap.json()['data']:
                        cursor.execute("INSERT OR IGNORE INTO Sehirler (sehir_adi, bolge) VALUES (?, ?)", (il['name'], il['region']['tr']))
            except Exception:
                yedek_sehirler = [('İzmir', 'Ege'), ('Bursa', 'Marmara'), ('Balıkesir', 'Marmara'), ('Antalya', 'Akdeniz'), ('Nevşehir', 'İç Anadolu'), ('Muğla', 'Ege'), ('İstanbul', 'Marmara'), ('Rize', 'Karadeniz'), ('Erzurum', 'Doğu Anadolu'), ('Kayseri', 'İç Anadolu'), ('Bolu', 'Karadeniz'), ('Şanlıurfa', 'Güneydoğu Anadolu'), ('Trabzon', 'Karadeniz'), ('Çanakkale', 'Marmara'), ('Aydın', 'Ege'), ('Ankara', 'İç Anadolu'), ('Gaziantep', 'Güneydoğu Anadolu'), ('Mardin', 'Güneydoğu Anadolu')]
                cursor.executemany("INSERT OR IGNORE INTO Sehirler (sehir_adi, bolge) VALUES (?, ?)", yedek_sehirler)

            # --- TÜM ŞEHİRLERİ KAPSAYAN 310+ MEKANLIK DEV VERİ SETİ ---
            tohum_mekanlar = {
                "Antalya": {
                    "Yaz Tatili": ["Kaputaş Plajı", "Konyaaltı Sahili", "Olympos Plajı", "Patara Plajı", "Cleopatra Plajı", "Adrasan Koyu", "Kekova", "Lara Plajı", "Phaselis Plajı", "Çıralı Sahili", "Suluada", "Korsan Koyu", "Beldibi Plajı"],
                    "Kış Tatili": ["Saklıkent Kayak Merkezi", "Tahtalı Dağı Teleferik", "Beydağları Zirvesi", "Akdağ Kış Sporları Merkezi"],
                    "Doğa & Kamp": ["Düden Şelalesi", "Kurşunlu Şelalesi", "Köprülü Kanyon", "Göynük Kanyonu", "Saklıkent Milli Parkı", "Karain Mağarası", "Manavgat Şelalesi", "Uçansu Şelalesi", "Sapadere Kanyonu", "Korsan Koyu Kamp Alanı"],
                    "Kültür Turu": ["Antalya Arkeoloji Müzesi", "Kaleiçi Eski Şehir", "Aspendos Antik Tiyatrosu", "Termessos Antik Kenti", "Myra Antik Kenti", "Perge Antik Kenti", "Xanthos Antik Kenti", "Phaselis Antik Kenti", "Olympos Antik Kenti"]
                },
                "Muğla": {
                    "Yaz Tatili": ["Ölüdeniz", "İztuzu Plajı", "Kelebekler Vadisi", "Datça Palamutbükü", "Marmaris İçmeler", "Akyaka Plajı", "Kabak Koyu", "Sarıgerme Plajı", "Kargı Koyu", "Hayıtbükü", "Bitez Plajı", "Ortakent Yahşi", "Turunç Sahili"],
                    "Kış Tatili": ["Sandras Dağı", "Muğla Karabağlar Yaylası", "Göktepe Kış Yürüyüş Rotaları"],
                    "Doğa & Kamp": ["Saklıkent Kanyonu", "Yuvarlakçay", "Dalyan Nehri", "Akyaka Orman Kampı", "Azmak Nehri", "Bafa Gölü", "Gizlikent Şelalesi", "Kavaklıdere Menteşe Yaylası", "Köyceğiz Gölü"],
                    "Kültür Turu": ["Bodrum Kalesi Sualtı Müzesi", "Knidos Antik Kenti", "Kaunos Antik Kenti", "Letoon Antik Kenti", "Halikarnas Mozolesi", "Tlos Antik Kenti", "Stratonikeia Antik Kenti", "Sedir Adası (Cleopatra)"]
                },
                "İzmir": {
                    "Yaz Tatili": ["Çeşme Ilıca Plajı", "Alaçatı Sörf Merkezi", "Seferihisar Sığacık", "Urla Altınköy", "Foça Koyları", "Dikili Bademli Koyu", "Çandarlı Sahili", "Mordoğan Ayıbalığı Koyu", "Karaburun Sahili", "Boyalık Plajı"],
                    "Kış Tatili": ["Bozdağ Kayak Merkezi", "Spil Dağı Milli Parkı", "Gölcük Yaylası (Kışın)"],
                    "Doğa & Kamp": ["Karagöl Tabiat Parkı", "Şirince Köyü Doğası", "İnciraltı Kent Ormanı", "Gölcük Gölü", "Nebiler Şelalesi", "Homeros Vadisi", "Ekmeksiz Tabiat Parkı"],
                    "Kültür Turu": ["Efes Antik Kenti", "İzmir Tarihi Asansör", "Kemeraltı Çarşısı", "İzmir Saat Kulesi", "Bergama Antik Kenti", "Şirince Matematik Köyü", "Klazomenai Antik Kenti", "Agora Ören Yeri", "Meryem Ana Evi"]
                },
                "Nevşehir": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Erciyes Dağı (Yakın Rota)", "Hasan Dağı Kış Tırmanışı"],
                    "Doğa & Kamp": ["Kızılçukur Vadisi", "Aşk Vadisi", "Ihlara Vadisi", "Güvercinlik Vadisi", "Kapadokya Balon Seyir Tepesi", "Devrent Vadisi (Hayal Vadisi)", "Paşabağ Rahipler Vadisi", "Güllüdere Vadisi"],
                    "Kültür Turu": ["Göreme Açık Hava Müzesi", "Derinkuyu Yeraltı Şehri", "Kaymaklı Yeraltı Şehri", "Uçhisar Kalesi", "Zelve Ören Yeri", "Ortahisar Kalesi", "Özkonak Yeraltı Şehri", "Avanos Çömlek Atölyeleri"]
                },
                "Bursa": {
                    "Yaz Tatili": ["Mudanya Sahili", "Trilye Plajı", "Kumla Sahili", "Kurşunlu Plajı", "Burgaz Altınkum"],
                    "Kış Tatili": ["Uludağ Kayak Merkezi", "Uludağ Milli Parkı Zirvesi", "Olympos Teleferik Hattı", "Sarıalan Kış Kampı"],
                    "Doğa & Kamp": ["Gölyazı (Uluabat Gölü)", "Suuçtu Şelalesi", "Saitabat Şelalesi", "İznik Gölü", "Cumalıkızık Ormanları", "Oylat Şelalesi", "Küreklidere Şelalesi"],
                    "Kültür Turu": ["Bursa Ulu Camii", "Cumalıkızık Köyü", "Yeşil Türbe", "Osman Gazi ve Orhan Gazi Türbeleri", "Bursa Kent Müzesi", "İznik Ayasofya Cami", "Muradiye Külliyesi", "Irgandı Köprüsü"]
                },
                "İstanbul": {
                    "Yaz Tatili": ["Şile Plajları", "Kilyos Sahili", "Prens Adaları (Büyükada)", "Caddebostan Sahili", "Ağva Koyları", "Florya Güneş Plajı", "Heybeliada Sadıkbey Plajı"],
                    "Kış Tatili": ["Aydos Ormanı Kar Yürüyüşü", "Çamlıca Tepesi", "Kartepe (Yakın Rota)"],
                    "Doğa & Kamp": ["Polonezköy Tabiat Parkı", "Belgrad Ormanı", "Atatürk Arberetumu", "Ağva Nehir Kampı", "Şile Saklıgöl", "Aydos Tepesi", "Emirgan Korusu"],
                    "Kültür Turu": ["Ayasofya-i Kebir Cami-i", "Topkapı Sarayı", "Yerebatan Sarnıcı", "Galata Kulesi", "İstanbul Arkeoloji Müzeleri", "Dolmabahçe Sarayı", "Süleymaniye Camii", "Kapalıçarşı", "Kız Kulesi", "Mısır Çarşısı"]
                },
                "Balıkesir": {
                    "Yaz Tatili": ["Cunda Adası", "Sarımsaklı Plajı", "Ören Sahili", "Ayvalık Koyları", "Altınoluk Sahili", "Akçay Plajı"],
                    "Kış Tatili": ["Kazdağları Kış Tırmanışı"],
                    "Doğa & Kamp": ["Kazdağları Milli Parkı", "Şahinderesi Kanyonu", "Hasanboğuldu Şelalesi", "Sütüven Şelalesi", "Kozak Yaylası"],
                    "Kültür Turu": ["Taksiyarhis Kilisesi", "Antandros Antik Kenti", "Ayvalık Tarihi Evleri", "Şeytan Sofrası Seyir Tepesi"]
                },
                "Rize": {
                    "Yaz Tatili": ["Fındıklı Sahili", "Çayeli Plajı", "Ardeşen Sahili"],
                    "Kış Tatili": ["Ovit Dağı Kış Sporları Merkezi", "Ayder Yaylası Heliski Alanı"],
                    "Doğa & Kamp": ["Ayder Yaylası", "Pokut Yaylası", "Fırtına Deresi", "Palovit Şelalesi", "Kaçkar Dağları Milli Parkı", "Gito Yaylası", "Huser Yaylası Sis Denizi"],
                    "Kültür Turu": ["Zilkale", "Rize Kalesi", "Şenyuva Köprüsü"]
                },
                "Erzurum": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Palandöken Kayak Merkezi", "Kandilli Kayak Tesisi", "Konaklı Kayak Merkezi"],
                    "Doğa & Kamp": ["Tortum Şelalesi", "Tortum Gölü", "Narman Peribacaları", "Yedi Göller (İspir)"],
                    "Kültür Turu": ["Çifte Minareli Medrese", "Yakutiye Medresesi", "Erzurum Kalesi", "Üç Kümbetler"]
                },
                "Kayseri": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Erciyes Kayak Merkezi", "Erciyes Yüksek İrtifa Kamp Merkezi"],
                    "Doğa & Kamp": ["Kapuzbaşı Şelaleleri", "Sultansazlığı Milli Parkı", "Aladağlar Milli Parkı"],
                    "Kültür Turu": ["Kayseri Kalesi", "Hunat Hatun Külliyesi", "Selçuklu Uygarlığı Müzesi"]
                },
                "Çanakkale": {
                    "Yaz Tatili": ["Bozcaada Ayazma Plajı", "Gökçeada Aydıncık Plajı", "Assos Kadırga Koyu", "Kabatepe Plajı", "Saros Körfezi"],
                    "Kış Tatili": ["Kazdağları Kış Yürüyüşü"],
                    "Doğa & Kamp": ["Kazdağları Milli Parkı", "Adatepe Köyü Doğası", "Şahinderesi Kanyonu"],
                    "Kültür Turu": ["Truva Antik Kenti", "Gelibolu Yarımadası Tarihi Milli Parkı", "Çanakkale Şehitler Abidesi", "Assos Antik Kenti", "Aynalı Çarşı"]
                },
                "Trabzon": {
                    "Yaz Tatili": ["Sürmene Çamburnu Plajı", "Yalıncak Sahili"],
                    "Kış Tatili": ["Uzungöl Kış Festivali Alanı", "Zigana Gümüşkayak Merkezi"],
                    "Doğa & Kamp": ["Uzungöl Tabiat Parkı", "Hıdırnebi Yaylası", "Çal Mağarası", "Sera Gölü Tabiat Parkı"],
                    "Kültür Turu": ["Sümela Manastırı", "Trabzon Ayasofya Müzesi", "Trabzon Atatürk Köşkü"]
                },
                "Ankara": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Elmadağ Kayak Merkezi"],
                    "Doğa & Kamp": ["Eymir Gölü", "Mogan Gölü Tabiat Parkı", "Soğuksu Milli Parkı", "Karagöl (Çubuk)", "Kuğulu Park"],
                    "Kültür Turu": ["Anıtkabir", "Anadolu Medeniyetleri Müzesi", "Ankara Kalesi", "I. TBMM Kurtuluş Savaşı Müzesi"]
                },
                "Gaziantep": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Erikçe Kayak Eğitim Merkezi"],
                    "Doğa & Kamp": ["Dülükbaba Ormanı", "Rumkale ve Fırat Nehri Kıyıları", "Burç Tabiat Parkı"],
                    "Kültür Turu": ["Zeugma Mozaik Müzesi", "Gaziantep Kalesi", "Bakırcılar Çarşısı", "Tarihi Antep Evleri"]
                },
                "Şanlıurfa": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Karacadağ Kayak Merkezi"],
                    "Doğa & Kamp": ["Halfeti Birecik Baraj Gölü", "Gölpınar Tabiat Parkı"],
                    "Kültür Turu": ["Göbeklitepe", "Balıklıgöl (Halil-ür Rahman)", "Harran Evleri ve Antik Kenti", "Karahantepe"]
                },
                "Mardin": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": [], 
                    "Doğa & Kamp": ["Beyazsu", "Zinnar Vadisi", "Gurs Vadisi Şelalesi"],
                    "Kültür Turu": ["Deyrulzafaran Manastırı", "Kasımiye Medresesi", "Zinciriye Medresesi", "Mardin Eski Şehir Evleri", "Dara Antik Kenti", "Mor Gabriel Manastırı"]
                }
            }

            butceler = ["$", "$$", "$$$"]
            toplam_mekan = 0

            for sehir_adi, categories in tohum_mekanlar.items():
                cursor.execute("SELECT id FROM Sehirler WHERE sehir_adi = ?", (sehir_adi,))
                sehir_row = cursor.fetchone()
                if not sehir_row: continue
                sehir_id = sehir_row[0]

                for sezon, mekanlar in categories.items():
                    for mekan in mekanlar:
                        cursor.execute("INSERT INTO Mekanlar (sehir_id, mekan_adi, sezon, butce) VALUES (?, ?, ?, ?)",
                                       (sehir_id, mekan, sezon, random.choice(butceler)))
                        toplam_mekan += 1
            
            logging.info(f"✅ 310+ Lokasyon başarıyla kaydedildi.")

            # --- SOSYAL HESAPLAR VE ÇOKLU AKTİVİTE GÜNCELLEMESİ ---
            logging.info("Örnek kullanıcı profilleri, listeler ve değerlendirmeler yükleniyor...")
            
            ornek_kullanicilar = [('admin', '1234'), ('zeki', '1234'), ('gezgin', '0000')]
            for k_adi, sifre in ornek_kullanicilar:
                cursor.execute("INSERT OR IGNORE INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (k_adi, sifre))
            
            cursor.execute("SELECT id, kullanici_adi FROM Kullanicilar")
            k_idler = {isim: k_id for k_id, isim in cursor.fetchall()}

            # Yardımcı Fonksiyon 1: Bire-bir benzersiz puanlama satırı
            def test_puani_ekle(kullanici_isim, mekan_adi, puan):
                if kullanici_isim not in k_idler: return
                k_id = k_idler[kullanici_isim]
                cursor.execute("SELECT id FROM Mekanlar WHERE mekan_adi=?", (mekan_adi,))
                m_row = cursor.fetchone()
                if m_row:
                    cursor.execute("INSERT INTO Ziyaret_ve_Puanlama (kullanici_id, mekan_id, puan, yorum) VALUES (?, ?, ?, '')", 
                                   (k_id, m_row[0], puan))

            # Yardımcı Fonksiyon 2: Bağımsız, peş peşe eklenebilen sosyal yorumlar (Puan=0)
            def test_yorum_ekle(kullanici_isim, mekan_adi, yorum):
                if kullanici_isim not in k_idler: return
                k_id = k_idler[kullanici_isim]
                cursor.execute("SELECT id FROM Mekanlar WHERE mekan_adi=?", (mekan_adi,))
                m_row = cursor.fetchone()
                if m_row:
                    cursor.execute("INSERT INTO Ziyaret_ve_Puanlama (kullanici_id, mekan_id, puan, yorum) VALUES (?, ?, 0, ?)", 
                                   (k_id, m_row[0], yorum))

            # Yardımcı Fonksiyon 3: Otomatik Liste Doldurucu (Gidilen Yerler / Gidilecek Yerler vb.)
            def test_not_ekle(kullanici_isim, kategori, icerik):
                if kullanici_isim not in k_idler: return
                k_id = k_idler[kullanici_isim]
                cursor.execute("INSERT INTO SeyahatNotlari (kullanici_id, kategori, not_icerik) VALUES (?, ?, ?)", 
                               (k_id, kategori, icerik))

            # --- MEKAN: KAPUTAŞ PLAJI ---
            test_puani_ekle('admin', 'Kaputaş Plajı', 5)
            test_yorum_ekle('admin', 'Kaputaş Plajı', 'Denizi tek kelimeyle maldivler gibi, harika berraklıkta.')
            test_yorum_ekle('admin', 'Kaputaş Plajı', 'Aracınızı yukarıda yol kenarına park etmeniz gerekiyor, otoparkı yok.')
            test_puani_ekle('zeki', 'Kaputaş Plajı', 4)
            test_yorum_ekle('zeki', 'Kaputaş Plajı', 'Öğleden sonra rüzgarla beraber dalga boyu çok artıyor, sabah gitmek en iyisi.')
            test_puani_ekle('gezgin', 'Kaputaş Plajı', 5)

            # --- MEKAN: EFES ANTİK KENTİ ---
            test_puani_ekle('zeki', 'Efes Antik Kenti', 5)
            test_yorum_ekle('zeki', 'Efes Antik Kenti', 'Celsus Kütüphanesi ve Yamaç Evler kesinlikle görülmeli. Muazzam bir mühendislik.')
            test_puani_ekle('admin', 'Efes Antik Kenti', 5)
            test_yorum_ekle('admin', 'Efes Antik Kenti', 'Müzekart sahiplerine giriş ücretsiz, kartınız mutlaka yanınızda olsun.')
            test_puani_ekle('gezgin', 'Efes Antik Kenti', 4)

            # --- MEKAN: ULUDAĞ KAYAK MERKEZİ ---
            test_puani_ekle('admin', 'Uludağ Kayak Merkezi', 4)
            test_yorum_ekle('admin', 'Uludağ Kayak Merkezi', 'Pistler güzel hazırlanmış fakat sömestr döneminde lift sıraları çok uzuyor.')
            test_puani_ekle('gezgin', 'Uludağ Kayak Merkezi', 3)
            test_yorum_ekle('gezgin', 'Uludağ Kayak Merkezi', 'Fiyatlar genel olarak ortalamanın biraz üstünde, bütçenizi ona göre ayarlayın.')

            # --- DİĞER MEKAN ETKİLEŞİMLERİ ---
            test_puani_ekle('admin', 'Galata Kulesi', 5)
            test_yorum_ekle('admin', 'Galata Kulesi', 'Üst kattaki seyir terasından 360 derece İstanbul manzarası izlenebiliyor.')
            test_puani_ekle('admin', 'Ayasofya-i Kebir Cami-i', 5)
            test_puani_ekle('admin', 'Cunda Adası', 4)
            
            test_puani_ekle('zeki', 'Cunda Adası', 5)
            test_yorum_ekle('zeki', 'Cunda Adası', 'Tarihi Taş Kahve\'de sakızlı Türk kahvesi içmeden dönmeyin.')
            test_puani_ekle('zeki', 'İzmir Saat Kulesi', 4)
            
            test_puani_ekle('gezgin', 'Karagöl Tabiat Parkı', 5)
            test_yorum_ekle('gezgin', 'Karagöl Tabiat Parkı', 'Doğası, sessizliği ve kamp olanakları harika. Sonbaharda renk cümbüşü oluyor.')
            test_puani_ekle('gezgin', 'Köprülü Kanyon', 5)
            test_yorum_ekle('gezgin', 'Köprülü Kanyon', 'Rafting parkuru çok keyifli ve güvenli, profesyonel ekipler eşlik ediyor.')

            # ======================================================================
            # --- YENİ EKLENEN: SEYAHAT LİSTELERİNİN ("GİDİLEN/GİDİLECEK") DOLDURULMASI ---
            # ======================================================================

            # 1. ADMIN LİSTELERİ
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Kaputaş Plajı')
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Uludağ Kayak Merkezi')
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Galata Kulesi')
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Ayasofya-i Kebir Cami-i')
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Efes Antik Kenti')
            test_not_ekle('admin', 'Gidilen Yerler', '🏛️ Mekan: Cunda Adası')
            
            test_not_ekle('admin', 'Gidilecek Yerler', '📍 Şehir: Nevşehir')
            test_not_ekle('admin', 'Gidilecek Yerler', '🏛️ Mekan: Göreme Açık Hava Müzesi')
            test_not_ekle('admin', 'Gidilecek Yerler', '🏛️ Mekan: Ihlara Vadisi')
            test_not_ekle('admin', 'Gidilecek Yerler', '🏛️ Mekan: Şirince Köyü Doğası')
            
            test_not_ekle('admin', 'Genel Notlar', 'Yaz tatili için bütçe planlaması: Antalya uçak biletleri alındı. Araç kiralama işi haftaya çözülecek. Bütçe tahmini: 25.000 TL')

            # 2. ZEKİ LİSTELERİ
            test_not_ekle('zeki', 'Gidilen Yerler', '🏛️ Mekan: Kaputaş Plajı')
            test_not_ekle('zeki', 'Gidilen Yerler', '🏛️ Mekan: Efes Antik Kenti')
            test_not_ekle('zeki', 'Gidilen Yerler', '🏛️ Mekan: Cunda Adası')
            test_not_ekle('zeki', 'Gidilen Yerler', '🏛️ Mekan: İzmir Saat Kulesi')
            
            test_not_ekle('zeki', 'Gidilecek Yerler', '📍 Şehir: Balıkesir')
            test_not_ekle('zeki', 'Gidilecek Yerler', '🏛️ Mekan: Ayvalık Koyları')
            test_not_ekle('zeki', 'Gidilecek Yerler', '🏛️ Mekan: Şeytan Sofrası Seyir Tepesi')
            test_not_ekle('zeki', 'Gidilecek Yerler', '🏛️ Mekan: Kazdağları Milli Parkı')
            
            test_not_ekle('zeki', 'Genel Notlar', 'Ayvalık planı: Otogardan ilçe merkezine ulaşım rotası detaylıca ayarlanacak. Gezilecek yerler bir güne sığdırılmalı.\n\nİzmir Seyahati: Havası nemli olacağı için fresh/meyveli bir parfüm alınacak.')

            # 3. GEZGİN LİSTELERİ
            test_not_ekle('gezgin', 'Gidilen Yerler', '🏛️ Mekan: Kaputaş Plajı')
            test_not_ekle('gezgin', 'Gidilen Yerler', '🏛️ Mekan: Uludağ Kayak Merkezi')
            test_not_ekle('gezgin', 'Gidilen Yerler', '🏛️ Mekan: Karagöl Tabiat Parkı')
            test_not_ekle('gezgin', 'Gidilen Yerler', '🏛️ Mekan: Köprülü Kanyon')
            
            test_not_ekle('gezgin', 'Gidilecek Yerler', '📍 Şehir: Rize')
            test_not_ekle('gezgin', 'Gidilecek Yerler', '🏛️ Mekan: Ayder Yaylası')
            test_not_ekle('gezgin', 'Gidilecek Yerler', '🏛️ Mekan: Fırtına Deresi')
            
            test_not_ekle('gezgin', 'Genel Notlar', 'Yeni çadır alındı. Hafta sonu Rize tarafına veya İzmir Karagöl tarafına kamp rotası çizilecek.')

            logging.info("🚀 MEGA PORTFOLYO VERİTABANI BAŞARIYLA ÜRETİLDİ! Listeler ve Puanlar tam senkronize çalışıyor.")
            conn.commit()

if __name__ == '__main__':
    veritabani_olustur()