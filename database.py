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
            logging.info("Veritabanı Tohumlama (Database Seeding) işlemi başlatıldı...")
            
            # Şehirleri Türkiye API'den hızlıca çek (Burası çok stabil çalıştığı için tutuyoruz)
            try:
                cevap = requests.get("https://turkiyeapi.dev/api/v1/provinces", timeout=5) 
                if cevap.status_code == 200:
                    for il in cevap.json()['data']:
                        cursor.execute("INSERT OR IGNORE INTO Sehirler (sehir_adi, bolge) VALUES (?, ?)", (il['name'], il['region']['tr']))
            except Exception:
                logging.warning("Şehirler API'si yanıt vermedi, lokal şehir listesi kullanılıyor.")
                yedek_sehirler = [('İzmir', 'Ege'), ('Bursa', 'Marmara'), ('Balıkesir', 'Marmara'), ('Antalya', 'Akdeniz'), ('Nevşehir', 'İç Anadolu'), ('Muğla', 'Ege'), ('İstanbul', 'Marmara'), ('Rize', 'Karadeniz'), ('Erzurum', 'Doğu Anadolu'), ('Kayseri', 'İç Anadolu'), ('Bolu', 'Karadeniz'), ('Şanlıurfa', 'Güneydoğu Anadolu'), ('Trabzon', 'Karadeniz'), ('Çanakkale', 'Marmara'), ('Aydın', 'Ege'), ('Ankara', 'İç Anadolu'), ('Gaziantep', 'Güneydoğu Anadolu'), ('Mardin', 'Güneydoğu Anadolu')]
                cursor.executemany("INSERT OR IGNORE INTO Sehirler (sehir_adi, bolge) VALUES (?, ?)", yedek_sehirler)

            cursor.execute("INSERT OR IGNORE INTO Kullanicilar (kullanici_adi, sifre) VALUES ('admin', '1234')")

            # --- KUSURSUZ TOHUM VERİLERİ (SEED DATA) ---
            # Gerçek bir kurumsal projede olduğu gibi temiz, onaylanmış ve yüksek kaliteli veri seti.
            tohum_mekanlar = {
                "Antalya": {
                    "Yaz Tatili": ["Kaputaş Plajı", "Konyaaltı Sahili", "Olympos Plajı", "Patara Plajı", "Cleopatra Plajı", "Adrasan Koyu", "Kekova"],
                    "Kış Tatili": ["Saklıkent Kayak Merkezi", "Tahtalı Dağı Teleferik", "Beydağları Zirvesi"],
                    "Doğa & Kamp": ["Düden Şelalesi", "Kurşunlu Şelalesi", "Köprülü Kanyon", "Göynük Kanyonu", "Saklıkent Milli Parkı", "Karain Mağarası"],
                    "Kültür Turu": ["Antalya Arkeoloji Müzesi", "Kaleiçi Eski Şehir", "Aspendos Antik Tiyatrosu", "Termessos Antik Kenti", "Myra Antik Kenti"]
                },
                "Muğla": {
                    "Yaz Tatili": ["Ölüdeniz", "İztuzu Plajı", "Kelebekler Vadisi", "Datça Palamutbükü", "Marmaris İçmeler", "Akyaka Plajı", "İztuzu"],
                    "Kış Tatili": ["Sandras Dağı", "Muğla Karabağlar Yaylası"],
                    "Doğa & Kamp": ["Saklıkent Kanyonu", "Yuvarlakçay", "Dalyan Nehri", "Akyaka Orman Kampı", "Azmak Nehri", "Bafa Gölü"],
                    "Kültür Turu": ["Bodrum Kalesi Sualtı Müzesi", "Knidos Antik Kenti", "Kaunos Antik Kenti", "Letoon Antik Kenti", "Halikarnas Mozolesi"]
                },
                "İzmir": {
                    "Yaz Tatili": ["Çeşme Ilıca Plajı", "Alaçatı Sörf Merkezi", "Seferihisar Sığacık", "Urla Altınköy", "Foça Koyları"],
                    "Kış Tatili": ["Bozdağ Kayak Merkezi", "Spil Dağı Milli Parkı"],
                    "Doğa & Kamp": ["Karagöl Tabiat Parkı", "Şirince Köyü Doğası", "İnciraltı Kent Ormanı", "Gölcük Gölü"],
                    "Kültür Turu": ["Efes Antik Kenti", "İzmir Tarihi Asansör", "Kemeraltı Çarşısı", "İzmir Saat Kulesi", "Bergama Antik Kenti"]
                },
                "Nevşehir": {
                    "Yaz Tatili": [], # Nevşehir'de plaj olmadığı için mimari gereği boş bırakıldı (0 Hata)
                    "Kış Tatili": ["Erciyes Dağı (Yakın Rota)", "Hasan Dağı Kış Tırmanışı"],
                    "Doğa & Kamp": ["Kızılçukur Vadisi", "Aşk Vadisi", "Ihlara Vadisi", "Güvercinlik Vadisi", "Kapadokya Balon Seyir Tepesi"],
                    "Kültür Turu": ["Göreme Açık Hava Müzesi", "Derinkuyu Yeraltı Şehri", "Kaymaklı Yeraltı Şehri", "Uçhisar Kalesi", "Zelve Ören Yeri"]
                },
                "Bursa": {
                    "Yaz Tatili": ["Mudanya Sahili", "Trilye Plajı", "Kumla Sahili"],
                    "Kış Tatili": ["Uludağ Kayak Merkezi", "Uludağ Milli Parkı Zirvesi", "Olympos Teleferik Hattı"],
                    "Doğa & Kamp": ["Gölyazı (Uluabat Gölü)", "Suuçtu Şelalesi", "Saitabat Şelalesi", "İznik Gölü"],
                    "Kültür Turu": ["Bursa Ulu Camii", "Cumalıkızık Köyü", "Yeşil Türbe", "Osman Gazi ve Orhan Gazi Türbeleri", "Bursa Kent Müzesi"]
                },
                "İstanbul": {
                    "Yaz Tatili": ["Şile Plajları", "Kilyos Sahili", "Prens Adaları (Büyükada)", "Caddebostan Sahili"],
                    "Kış Tatili": ["Aydos Ormanı Kar Yürüyüşü", "Çamlıca Tepesi"],
                    "Doğa & Kamp": ["Polonezköy Tabiat Parkı", "Belgrad Ormanı", "Atatürk Arberetumu", "Ağva Nehir Kampı"],
                    "Kültür Turu": ["Ayasofya-i Kebir Cami-i", "Topkapı Sarayı", "Yerebatan Sarnıcı", "Galata Kulesi", "İstanbul Arkeoloji Müzeleri"]
                },
                "Rize": {
                    "Yaz Tatili": ["Fındıklı Sahili", "Çayeli Plajı"],
                    "Kış Tatili": ["Ovit Dağı Kış Sporları Merkezi", "Ayder Yaylası Heliski Alanı", "Kavrun Yaylası"],
                    "Doğa & Kamp": ["Ayder Yaylası", "Pokut Yaylası", "Fırtına Deresi", "Palovit Şelalesi", "Kaçkar Dağları Milli Parkı"],
                    "Kültür Turu": ["Zilkale", "Rize Kalesi", "Şenyuva Köprüsü", "Rize Çay Müzesi"]
                },
                "Erzurum": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Palandöken Kayak Merkezi", "Kandilli Kayak Tesisi", "Konaklı Kayak Merkezi"],
                    "Doğa & Kamp": ["Tortum Şelalesi", "Tortum Gölü", "Narman Peribacaları", "Yedi Göller (İspir)"],
                    "Kültür Turu": ["Çifte Minareli Medrese", "Yakutiye Medresesi", "Erzurum Kalesi", "Üç Kümbetler", "Nene Hatun Tarihi Milli Parkı"]
                },
                "Kayseri": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Erciyes Kayak Merkezi", "Erciyes Yüksek İrtifa Kamp Merkezi"],
                    "Doğa & Kamp": ["Kapuzbaşı Şelaleleri", "Sultansazlığı Milli Parkı", "Aladağlar Milli Parkı", "Ali Dağı"],
                    "Kültür Turu": ["Kayseri Kalesi", "Hunat Hatun Külliyesi", "Selçuklu Uygarlığı Müzesi", "Döner Kümbet"]
                },
                "Çanakkale": {
                    "Yaz Tatili": ["Bozcaada Ayazma Plajı", "Gökçeada Aydıncık Plajı", "Assos Kadırga Koyu", "Kabatepe Plajı"],
                    "Kış Tatili": ["Kazdağları Kış Yürüyüşü"],
                    "Doğa & Kamp": ["Kazdağları Milli Parkı", "Adatepe Köyü Doğası", "Şahinderesi Kanyonu", "Gökçeada Sualtı Milli Parkı"],
                    "Kültür Turu": ["Truva Antik Kenti", "Gelibolu Yarımadası Tarihi Milli Parkı", "Çanakkale Şehitler Abidesi", "Assos Antik Kenti", "Aynalı Çarşı"]
                },
                "Trabzon": {
                    "Yaz Tatili": ["Sürmene Çamburnu Plajı", "Yalıncak Sahili"],
                    "Kış Tatili": ["Uzungöl Kış Festivali Alanı", "Zigana Gümüşkayak Merkezi"],
                    "Doğa & Kamp": ["Uzungöl Tabiat Parkı", "Hıdırnebi Yaylası", "Çal Mağarası", "Sera Gölü Tabiat Parkı", "Karadağ Yaylası"],
                    "Kültür Turu": ["Sümela Manastırı", "Trabzon Ayasofya Müzesi", "Trabzon Atatürk Köşkü", "Trabzon Kalesi"]
                },
                "Ankara": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Elmadağ Kayak Merkezi", "Keldağ Kış Rotaları"],
                    "Doğa & Kamp": ["Eymir Gölü", "Mogan Gölü Tabiat Parkı", "Soğuksu Milli Parkı", "Karagöl (Çubuk)", "Kuğulu Park"],
                    "Kültür Turu": ["Anıtkabir", "Anadolu Medeniyetleri Müzesi", "Ankara Kalesi", "I. TBMM Kurtuluş Savaşı Müzesi", "Rahmi M. Koç Müzesi"]
                },
                "Gaziantep": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Erikçe Kayak Eğitim Merkezi"],
                    "Doğa & Kamp": ["Dülükbaba Ormanı", "Rumkale ve Fırat Nehri Kıyıları", "Burç Tabiat Parkı"],
                    "Kültür Turu": ["Zeugma Mozaik Müzesi", "Gaziantep Kalesi", "Bakırcılar Çarşısı", "Gaziantep Oyun ve Oyuncak Müzesi", "Emine Göğüş Mutfak Müzesi"]
                },
                "Şanlıurfa": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": ["Karacadağ Kayak Merkezi"],
                    "Doğa & Kamp": ["Halfeti Birecik Baraj Gölü", "Gölpınar Tabiat Parkı", "Tek Tek Dağları Milli Parkı"],
                    "Kültür Turu": ["Göbeklitepe", "Balıklıgöl (Halil-ür Rahman)", "Harran Evleri ve Antik Kenti", "Şanlıurfa Arkeoloji Müzesi", "Haleplibahçe Mozaik Müzesi"]
                },
                "Mardin": {
                    "Yaz Tatili": [], 
                    "Kış Tatili": [], 
                    "Doğa & Kamp": ["Beyazsu", "Zinnar Vadisi", "Gurs Vadisi Şelalesi"],
                    "Kültür Turu": ["Deyrulzafaran Manastırı", "Kasımiye Medresesi", "Zinciriye Medresesi", "Mardin Eski Şehir Evleri", "Dara Antik Kenti", "Mardin Ulu Camii"]
                }
            }

            butceler = ["$", "$$", "$$$"]
            toplam_mekan = 0

            for sehir_adi, kategoriler in tohum_mekanlar.items():
                cursor.execute("SELECT id FROM Sehirler WHERE sehir_adi = ?", (sehir_adi,))
                sehir_row = cursor.fetchone()
                if not sehir_row: continue
                sehir_id = sehir_row[0]

                for sezon, mekanlar in kategoriler.items():
                    for mekan in mekanlar:
                        cursor.execute("INSERT INTO Mekanlar (sehir_id, mekan_adi, sezon, butce) VALUES (?, ?, ?, ?)",
                                       (sehir_id, mekan, sezon, random.choice(butceler)))
                        toplam_mekan += 1
                
                logging.info(f"✅ {sehir_adi} tohumlandı.")

            logging.info(f"🚀 SEEDİNG TAMAMLANDI! {toplam_mekan} Yüksek Kaliteli Turizm Noktası Veritabanına Eklendi.")
            conn.commit()

if __name__ == '__main__':
    veritabani_olustur()