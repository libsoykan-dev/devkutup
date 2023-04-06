## Bu program Creative Commons Atıf Gayri-Ticari 4.0 Uluslararası Kamu Lisansı ile lisanslanmıştır.
## Atıfta bulunurken 'libsoykan-dev' veya 'Naim Salih SOYKAN' olarak belirtebilirsiniz.
## Lisansın bir kopyasını program ile birlikte edinmiş olmanız gerekir. Eğer edinmediyseniz: https://creativecommons.org/licenses/by-nc/4.0/deed.tr

import PySimpleGUI as gka # Grafik Kullanıcı Arabirimi için PySimpleGUI kütüphanesi gka olarak içe aktarılır (for implementing graphical user interface)

import mysql.connector # MYSQL temel fonksiyonlarının ve sorguların çalıştırılması için kullanılır (for running MYSQL queries)

import time # Veri tabanına kaydedilen zaman damgalarının belirlenmesi için kullanılır (for saving timestamps to database)

from datetime import datetime # Kaydedilen zaman damgalarını dönüştürmek için kullanılır (for converting timestamps to human readable time format)

import pandas as pd # Excel dosyalarını dönüştürmek için kullanılır (for converting excel files)

import csv # Dönüştürülen excel dosyalarını tabloya aktarmak için kullanılır (for importing converted excel files to python list format)

import os # Dosya sistemi fonksiyonlarının işletilmesi için kullanılır (for implementing file system functions)

import sys # Sys fonksiyonları

import configparser # Config dosyalarının okunması için kullanılır (for reading config files)

config = configparser.ConfigParser()   

def csvac(yol):

    csvacilacak = open(yol, 'r', encoding='utf-8')
    
    csvacilan = list(csv.reader(csvacilacak, delimiter=','))
    
    csvacilacak.close()

    return csvacilan

def mevcutmu(tablo, kosul):

    kullanim0 = mydb.cursor()

    try:

        kullanim0.execute('SELECT EXISTS(SELECT * FROM ' + tablo + ' WHERE ' + kosul + ');')

    except mysql.connector.Error as hata:

        gka.popup('MYSQL Hatası:\n' + hata, title='Hata')

    netice = kullanim0.fetchall()

    if netice[0][0] > 0:

        return True

    else:

        return False

def kaydet(tablo, liste):
        
    try:

        for i in liste:

            kullanim1 = mydb.cursor()

            kullanim1.execute('INSERT INTO ' + tablo + ' VALUES ' + str(tuple(i)) + ';')

    except mysql.connector.Error as hata:

        gka.popup('MYSQL Hatası:\n' + hata, title='Hata')

def sil(tablo, kosul):

        kullanim2 = mydb.cursor()

        try:

            kullanim2.execute('DELETE FROM ' + tablo + ' WHERE ' + kosul + ';')

        except mysql.connector.Error as hata:

            gka.popup('MYSQL Hatası:\n' + hata, title='Hata')

def sorgula(tablo, kosul):

        kullanim3 = mydb.cursor()

        try:

            kullanim3.execute('SELECT * FROM ' + tablo + ' WHERE ' + kosul + ';')

        except mysql.connector.Error as hata:

            gka.popup('MYSQL Hatası:\n' + hata, title='Hata')

        return kullanim3.fetchall()

if os.path.exists('istemciler.csv') and os.path.exists('devkutup.conf'):

    istemcilistesi = csvac('istemciler.csv')

    config.read_file(open(r'devkutup.conf'))

    surum = 'v1.00_20230401'

    try:

        mysqlport = int(config.get('mysql-giris', 'port'))

        mysqlsifre = str(config.get('mysql-giris', 'sifre'))

        mysqlka = str(config.get('mysql-giris', 'kullaniciadi'))

        mysqlip = str(config.get('mysql-giris', 'ip'))

        tema = str(config.get('diger', 'tema'))

        kapatmatercih = int(config.get('diger', 'kapatmatercih'))

        istemci = int(config.get('diger', 'istemci'))

    except configparser.Error as hata:

        gka.popup('Config dosyası yanlış:\n' + str(hata), title='Kritik Hata')

        sys.exit()

elif os.path.exists('istemciler.csv'):

    gka.popup('''Ayarları barındıran dosya (devkutup.conf) yüklenemedi.
    Varsayılan ayarlar:
    [mysql-giris]
    host = localhost
    port = 3311
    user = root
    password = ""
    [diger]
    tema = "Black"
    kapatmatercih = 1''', title='Uyarı')

    mysqlport = 3311

    mysqlsifre = ''

    mysqlka = 'root'

    mysqlip = 'localhost'

    istemci = 0
    
    tema = 'Black'

    kapatmatercih =  1

elif os.path.exists('devkutup.conf'):

    gka.popup('İstemci listesi (istemciler.csv) yüklenemedi.\nİstemci listesi yüklenmesi zorunludur.', title='Kritik Hata')

    sys.exit()

else:

    gka.popup('''Programın çalışması için zorunlu olan bir veya daha fazla dosya yüklenemedi.
Bu dosyaları oluşturmadıysanız şimdi oluşturunuz.\nAşağıdaki gibi:

    ---devkutup.conf---
    [mysql-giris]
    ip = <mysql ip adresi(str)>
    kullaniciadi = <mysql kullanıcı adı(str)>
    sifre = <mysql şifre(str)>
    port = <mysql port(int)>
    [diger]
    tema = <PySimpleGUI teması(str)>
    kapatmatercih = <kapatma özelliği(int 1-0)>
    istemci = <istemci özelliği(int 1-0)>
    
    ---istemciler.csv---
    İstemci Adı, istemciadi
    ...
    
istemciler.csv, config dosyasında istemci = 0 olarak ayarlandığında zorunlu değildir.''', title='Kritik Hata')

    sys.exit()

try:

    mydb = mysql.connector.connect(

    host=mysqlip,

    user=mysqlka,

    password=mysqlsifre,

    database="devkutup",

    port=mysqlport,

    )

except mysql.connector.Error as hata:

    gka.popup('MYSQL Hatası:\n' + str(hata), title='Kritik Hata')

    sys.exit()

mysqlsorgucalistir = mydb.cursor().execute

def istemcikaydet(istemciadi):
        
    try:

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'kitaplar (kitapno varchar(50), kitapadi varchar(50), kitapyazari varchar(50), yayinevi varchar(50), kitapturu varchar(50), rafkodu varchar(50));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'kullanicilar (kullaniciadi varchar(50), sifre varchar(50), yetki varchar(50));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'uyeler (uyeno varchar(50), uyeadi varchar(50), uyesinifi varchar(50));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'verilenkitaplar (uyeno varchar(50), kitapno varchar(50), kitapadi varchar(50), kitapyazari varchar(50), yayinevi varchar(50), kitapturu varchar(50), rafkodu varchar(50), verildigizaman varchar(50), gunsayisi varchar(50));')

    except mysql.connector.Error as hata:

        gka.popup('MYSQL Hatası:\n' + hata, title='Hata')

gka.theme(tema)

def program(kitaplar, kullanicilar, uyeler, verilenkitaplar):

    def getirmeyenguncelle():

        liste0temp = sorgula(verilenkitaplar, '1=1')

        guncelliste = []

        for i in range(0, len(liste0temp)):

            guncellistesatir = []

            liste1temp = sorgula(uyeler, 'uyeno="' + liste0temp[i][0] + '"')

            listetempzaman = int(liste0temp[i][7])

            listetempgun = int(liste0temp[i][8])

            liste9temp = str(datetime.fromtimestamp(listetempzaman))

            listetempkalan = str(int(((listetempzaman + (listetempgun * 24 * 3600)) - time.time()) / (24 * 3600)))

            for a in range(3):

                guncellistesatir.append(liste1temp[0][a])

            for b in range(1, 7):

                guncellistesatir.append(liste0temp[i][b])

            guncellistesatir.append(liste9temp)

            guncellistesatir.append(str(datetime.fromtimestamp(listetempzaman + (listetempgun * 24 * 3600))))

            guncellistesatir.append(listetempkalan)

            guncelliste.append(guncellistesatir)

        anapencere['getirmeyenler'].update(values=guncelliste)

        return guncelliste

    if len(sorgula(kullanicilar, '1=1')) == 0:

        mysqlsorgucalistir('INSERT INTO ' + kullanicilar + ' VALUES ("DEVKÜTÜP", "12345", "Yönetici");')

        gka.popup('Kayıtlı kullanıcı yok. Varsayılan kullanıcı,\nKullanıcı Adı: DEVKÜTÜP\nŞifre: 12345\nYetkiler: Yönetici\noluşturuldu.', title='Uyarı')

    anaduzen = [[gka.Text('KİTAP İŞLEMLERİ:', s=(20,1), font=(8)),
                gka.Button('Kitap Al', key='kitapal', s=(20,1), font=(8)), gka.Button('Kitap Ver', key='kitapver', s=(20,1), font=(8)), gka.Button('Kitap Kaydet', key='kitapkaydet', s=(20,1), font=(8)), gka.Button('Kitap Sorgula veya Sil', key='kitapsil', s=(20,1), font=(8))],
                [gka.Text('ÜYE İŞLEMLERİ:', s=(20,1), font=(8)),
                gka.Button('Üye Kaydet', key='uyekaydet', s=(20,1), font=(8)), gka.Button('Üye Sorgula veya Sil', key='uyesil', s=(20,1), font=(8))],
                [gka.Text('KULLANICI İŞLEMLERİ:', s=(20,1), font=(8)),
                gka.Button('Kullanıcı Kaydet', key='kullanicikaydet', s=(20,1), font=(8)), gka.Button('Kullanıcı Sil', key='kullanicisil', s=(20,1), font=(8))],
                [gka.Text('Kitap Getirmeyenler')],
                [gka.Button('Listeyi Güncelle', key='guncelle')],
                [gka.Table([], ['Üye No.', 'Üye Adı', 'Üye Sınıfı',  'Kitap No.', 'Kitabın Adı', 'Kitabın Yazarı', 'Yayınevi', 'Kitabın Türü', 'Raf Kodu', 'Verildiği Zaman', 'Alınacağı Zaman', 'Kalan Gün Sayısı'], num_rows=20, key='getirmeyenler', def_col_width=12, auto_size_columns=False)],
                [gka.Text("Excel'e Aktar")],
                [gka.Input(key='anaexcelgirdi'), gka.FileSaveAs("Kayıt Yeri Belirle", file_types=(('Excel Dökümanı', '.xlsx'),)), gka.Button('Dışa Aktar', key='anaexceleaktaronay')]]

    kitapalduzen = [[gka.Text('Kitap No.', s=(10,1)), gka.Input(key='kitapalbarkod'), gka.Button('Kitap Al', key='kitapalonay')],
                    [gka.Text('Üye No. ile Verilen Kitap Sorgulama')],
                    [gka.Text('Üye No.', s=(10,1)), gka.Input(key='kitapaluyeno'), gka.Button('Sorgula', key='kitapalsorgula')],
                    [gka.Table([], ['Üye No.', 'Kitap No.', 'Kitabın Adı', 'Kitabın Yazarı', 'Yayınevi', 'Kitabın Türü', 'Raf Kodu'], num_rows=20, key='kitapalsorgu', def_col_width=10, auto_size_columns=False)]]

    kitapverduzen = [[gka.Text('Kitap No.', s=(10,1)), gka.Input(key='kitapverbarkod')],
                     [gka.Text('Üye No.', s=(10,1)), gka.Input(key='kitapveruyeno')],
                     [gka.Text('Gün Sayısı', s=(10,1)), gka.Input(key='kitapvergunsayisi')],
                     [gka.Button('Kitap Ver', key='kitapveronay')]]

    kitapkaydetduzen = [[gka.Text('Kitap No.', s=(10,1)), gka.Input(key='kitapkaydetbarkod')],
                        [gka.Text('Kitabın Adı', s=(10,1)), gka.Input(key='kitapkaydetadi')],
                        [gka.Text('Kitabın Yazarı', s=(10,1)), gka.Input(key='kitapkaydetyazari')],
                        [gka.Text('Yayınevi', s=(10,1)), gka.Input(key='kitapkaydetyayinevi')],
                        [gka.Text('Kitabın Türü', s=(10,1)), gka.Input(key='kitapkaydetkitabinturu')],
                        [gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='kitapkaydetdolapkodu')],
                        [gka.Button('Ekle', key='kitapkaydetekle'), gka.Button("Excel'den Aktar", key='kitapkaydetexcel')],
                        [gka.Table([], ['Kitap No.', 'Kitabın Adı', 'Kitabın Yazarı', 'Yayınevi', 'Kitabın Türü', 'Raf Kodu'], num_rows=20, key='kitapkaydetliste', def_col_width=10, auto_size_columns=False, enable_events=True)],
                        [gka.Button('Kaydet', key='kitapkaydetonay'), gka.Button('Satırı Sil', key='kitapkaydetlistesil'), gka.Text(key='kitapkaydetdurum')]]

    kitapsilduzen = [[gka.Text('Kitap No.', s=(10,1)), gka.Input(key='kitapsilbarkod')],
                    [gka.Text('Kitabın Adı', s=(10,1)), gka.Input(key='kitapsiladi')],
                    [gka.Text('Kitabın Yazarı', s=(10,1)), gka.Input(key='kitapsilyazari')],
                    [gka.Text('Yayınevi', s=(10,1)), gka.Input(key='kitapsilyayinevi')],
                    [gka.Text('Kitabın Türü', s=(10,1)), gka.Input(key='kitapsilkitabinturu')],
                    [gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='kitapsildolapkodu')],
                    [gka.Table([], ['Kitap No.', 'Kitabın Adı', 'Kitabın Yazarı', 'Yayınevi', 'Kitabın Türü', 'Raf Kodu', 'Bulunduğu Yer'], num_rows=20, key='kitapsilsorgu', def_col_width=10, auto_size_columns=False)],
                    [gka.Button('Sorgula', key='kitapsilsorguonay'), gka.Button('Listedekileri Sil', key='kitapsiltopluonay'), gka.Text(key='kitapsildurum')]]

    uyekaydetduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='uyekaydetuyeno')],
                    [gka.Text('Üye Adı', s=(10,1)), gka.Input(key='uyekaydetuyeadi')],
                    [gka.Text('Üye Sınıfı', s=(10,1)), gka.Input(key='uyekaydetuyesinifi')],
                    [gka.Button('Ekle', key='uyekaydetekle'), gka.Button("Excel'den Aktar", key='uyekaydetexcel')],
                    [gka.Table([], ['Üye No.', 'Üye Adı-Soyadı', 'Üye Sınıfı'], num_rows=20, key='uyekaydetliste', def_col_width=30, auto_size_columns=True, enable_events=True)],
                    [gka.Button('Kaydet', key='uyekaydetonay'), gka.Button('Satırı Sil', key='uyekaydetlistesil'), gka.Text(key='uyekaydetdurum')]]

    uyesilduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='uyesiluyeno')],
                [gka.Text('Üye Adı', s=(10,1)), gka.Input(key='uyesiladisoyadi')],
                [gka.Text('Üye Sınıfı', s=(10,1)), gka.Input(key='uyesilsinifi')],
                [gka.Table([], ['Üye No.', 'Üye Adı-Soyadı', 'Üye Sınıfı', 'Üye Kayıt Yeri'], num_rows=20, key='uyesilliste', def_col_width=30, auto_size_columns=True)],
                [gka.Button('Sorgula', key='uyesilsorguonay'), gka.Button('Listedekileri Sil', key='uyesiltopluonay'), gka.Text(key='uyesildurum')]]

    kullaniciduzen = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullanicikaydetadi')],
                    [gka.Text('Şifre', s=(10,1)), gka.Input(key='kullanicikaydetsifre')],
                    [gka.Text('Yetkileri', s=(10,1)), gka.Combo(['Ziyaretçi', 'Görevli', 'Yönetici'], default_value='Görevli', s=(15,22), enable_events=True, readonly=True, key='kullanicikaydetyetki')],
                    [gka.Button('Ekle', key='kullanicikaydetekle')],
                    [gka.Table([], ['Kullanıcı Adı', 'Kullanıcı Şifresi', 'Kullanıcı Rütbesi'], num_rows=20, key='kullanicikaydetliste', def_col_width=30, auto_size_columns=True, enable_events=True)],
                    [gka.Button('Kaydet', key='kullanicikaydetonay'), gka.Button('Satırı Sil', key='kullanicikaydetlistesil'), gka.Text(key='kullanicikaydetdurum')]]

    kullanicisilduzen = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullanicisiladi')],
                        [gka.Text('Kullanıcı Şifre', s=(10,1)), gka.Input(key='kullanicisilsifre')],
                        [gka.Text('Kullanıcı Yetkileri', s=(10,1)), gka.Combo(['Görevli', 'Yönetici'], default_value='Görevli', s=(15,22), enable_events=True, readonly=True, k='kullanicisilyetki')],
                        [gka.Table([], ['Kullanıcı Adı', 'Kullanıcı Şifresi', 'Kullanıcı Yetkileri'], num_rows=20, key='kullanicisilliste', def_col_width=30, auto_size_columns=True)],
                        [gka.Button('Sorgula', key='kullanicisilsorguonay'), gka.Button('Listedekileri Sil', key='kullanicisiltopluonay'), gka.Text(key='kullanicisildurum')]]

    kitapexcelduzen = [[gka.Text("Excel'den Aktar")],
                    [gka.Input(key='kitapexcelgirdi'), gka.FileBrowse("Dosya Aç", file_types=(('Excel Dökümanı', '.xlsx'),)), gka.Button('İçe Aktar', key='kitapexceleaktaronay')]]

    uyeexcelduzen = [[gka.Text("Excel'den Aktar")],
                    [gka.Input(key='uyeexcelgirdi'), gka.FileBrowse("Dosya Aç", file_types=(('Excel Dökümanı', '.xlsx'),)), gka.Button('İçe Aktar', key='uyeexceleaktaronay')]]

    girispencere = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullaniciadi')],
                    [gka.Text('Şifre', s=(10,1)), gka.Input(key='sifre')],
                    [gka.Button('Giriş Yap', key='girisyap')]]

    girispencere = gka.Window('DEVKÜTÜP ' + surum + ' Giriş Yap', girispencere, enable_close_attempted_event=True, finalize=True)

    anapencere = gka.Window('DEVKÜTÜP ' + surum + ' (C) 2022 libsoykan-dev', anaduzen, enable_close_attempted_event=True, finalize=True)

    anapencere.Hide()

    kitapalpencere = gka.Window('Kitap Al', kitapalduzen, enable_close_attempted_event=True, finalize=True)

    kitapalpencere.Hide()

    kitapverpencere = gka.Window('Kitap Ver', kitapverduzen, enable_close_attempted_event=True, finalize=True)

    kitapverpencere.Hide()

    kitapkaydetpencere = gka.Window('Kitap Kaydet', kitapkaydetduzen, enable_close_attempted_event=True, finalize=True)

    kitapkaydetpencere.Hide()

    kitapsilpencere = gka.Window('Kitap Sil', kitapsilduzen, enable_close_attempted_event=True, finalize=True)

    kitapsilpencere.Hide()

    uyekaydetpencere = gka.Window('Üye Kaydet', uyekaydetduzen, enable_close_attempted_event=True, finalize=True)

    uyekaydetpencere.Hide()

    uyesilpencere = gka.Window('Üye Sil', uyesilduzen, enable_close_attempted_event=True, finalize=True)

    uyesilpencere.Hide()

    kullanicikaydetpencere = gka.Window('Kullanıcı Kaydet', kullaniciduzen, enable_close_attempted_event=True, finalize=True)

    kullanicikaydetpencere.Hide()

    kullanicisilpencere = gka.Window('Kullanıcı Sil', kullanicisilduzen, enable_close_attempted_event=True, finalize=True)

    kullanicisilpencere.Hide()

    kitapexcelpencere = gka.Window("Excel'den Aktar", kitapexcelduzen, enable_close_attempted_event=True, finalize=True)

    kitapexcelpencere.Hide()

    uyeexcelpencere = gka.Window("Excel'den Aktar", uyeexcelduzen, enable_close_attempted_event=True, finalize=True)

    uyeexcelpencere.Hide()

    def anadongu():

        kitapkaydetpenliste = []

        uyekaydetpenliste = []

        kullanicikaydetpenliste = []

        anapencere.UnHide()

        while True:

            anafiil, anadeger = anapencere.read()

            anaexcelgirdi = anadeger['anaexcelgirdi']

            if anafiil == gka.WIN_CLOSE_ATTEMPTED_EVENT:

                anapencere.Hide()

                girispencere.UnHide()

                break

            if anafiil == 'anaexceleaktaronay' and anaexcelgirdi and yonetici != 2:

                df = pd.DataFrame(getirmeyenguncelle(), columns=['Üye No.', 'Üye Adı', 'Üye Sınıfı',  'Kitap No.', 'Kitabın Adı', 'Kitabın Yazarı', 'Yayınevi', 'Kitabın Türü', 'Raf Kodu', 'Verildiği Zaman', 'Alınacağı Zaman', 'Kalan Gün Sayısı'])

                df.to_excel(anaexcelgirdi)

            elif anafiil == 'anaexcelaktaronay':

                gka.popup('Eksik ya da hatalı dosya adı girdiniz.', title='Hata')

            if anafiil == 'guncelle' and yonetici != 2:

                getirmeyenguncelle()

            if anafiil == 'kitapal' and yonetici != 2:

                kitapalpencere.UnHide()

                gka.popup('Kitap alımı yaparken sadece "Kitap No." yeterlidir.', title='Bilgi')

                while True:

                    kitapalfiil, kitapaldeger = kitapalpencere.read()

                    kitapalbarkod = str(kitapaldeger['kitapalbarkod'])

                    kitapaluyeno = str(kitapaldeger['kitapaluyeno'])

                    if kitapalfiil == 'kitapalonay' and kitapalbarkod and mevcutmu(verilenkitaplar, ('kitapno="' + kitapalbarkod + '"')) and gka.popup_yes_no(sorgula(kitaplar, ('kitapno="' + kitapalbarkod + '"'))[0][1] + ' adlı kitap,\n' + str(sorgula(uyeler, sorgula(verilenkitaplar, 'kitapno="' + kitapalbarkod + '"')[0][0])[0][1]) + ' adlı üyeden\n\nteslim alınacaktır.\nOnaylıyor musunuz?') == 'Yes':

                        sil(verilenkitaplar, ('kitapno="' + kitapalbarkod + '"'))

                        kitapalpencere['kitapalsorgu'].update(values=sorgula(verilenkitaplar, ('uyeno="' + kitapaluyeno + '"')))

                    elif kitapalfiil == 'kitapalonay':

                        gka.popup('İşlem iptal edildi veya Kitap No. yanlış.', title='Hata')

                    if kitapalfiil == 'kitapalsorgula' and kitapaluyeno:

                        kitapalpencere['kitapalsorgu'].update(values=sorgula(verilenkitaplar, ('uyeno="' + kitapaluyeno + '"')))

                    elif kitapalfiil == 'kitapalsorgula':

                        gka.popup('Üye No. boş bırakılamaz.', title='Hata')

                    if kitapalfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kitapalpencere.Hide()

                        break

            elif anafiil == 'kitapal' and yonetici == 2:

                gka.popup('Ziyaretçiler yalnızca sorgulama yapabilir.', title='Hata')

            if anafiil == 'kitapver' and yonetici != 2:

                kitapverpencere.UnHide()

                while True:

                    kitapverfiil, kitapverdeger = kitapverpencere.read()

                    kitapverbarkod = str(kitapverdeger['kitapverbarkod'])

                    kitapveruyeno = str(kitapverdeger['kitapveruyeno'])

                    kitapvergunsayisi = str(kitapverdeger['kitapvergunsayisi'])

                    if kitapverfiil == 'kitapveronay' and kitapverbarkod and kitapveruyeno and kitapvergunsayisi and mevcutmu(kitaplar, 'kitapno="' + kitapverbarkod + '"') and mevcutmu(verilenkitaplar, 'kitapno="' + kitapverbarkod + '"') != True and mevcutmu(uyeler, 'uyeno="' + kitapveruyeno + '"') and gka.popup_yes_no(str(sorgula(kitaplar, ('kitapno="' + kitapverbarkod + '"'))[0][1]) + ' adlı kitap,\n' + str(sorgula(uyeler, ('uyeno="' + kitapveruyeno + '"'))[0][1]) + ' adlı üyeye\n\nverilecektir.\nOnaylıyor musunuz?') == 'Yes':

                        templiste1 = []

                        templiste1.append(kitapveruyeno)
                        
                        for i in range(0, 6):

                            templiste1.append(sorgula(kitaplar, 'kitapno="' + kitapverbarkod + '"')[0][i])

                        templiste1.append(str(int(time.time())))

                        templiste1.append(kitapvergunsayisi)

                        kaydet(verilenkitaplar, [templiste1])

                    elif kitapverfiil == 'kitapveronay':

                        gka.popup('Geçersiz giriş yaptınız. Kontrol ediniz.', title='Hata')

                    if kitapverfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kitapverpencere.Hide()

                        break

            elif anafiil == 'kitapver' and yonetici == 2:

                gka.popup('Ziyaretçiler yalnızca sorgulama yapabilir.', title='Hata')

            if anafiil == 'kitapkaydet' and yonetici != 2:

                kitapkaydetlistesecilen = -1

                kitapkaydetpencere.UnHide()

                while True:

                    kitapkaydetfiil, kitapkaydetdeger = kitapkaydetpencere.read()

                    if kitapkaydetfiil == 'kitapkaydetekle':

                        kitapkaydetbarkod = str(kitapkaydetdeger['kitapkaydetbarkod'])

                        kitapkaydetadi = str(kitapkaydetdeger['kitapkaydetadi'])

                        kitapkaydetyazari = str(kitapkaydetdeger['kitapkaydetyazari'])

                        kitapkaydetyayinevi = str(kitapkaydetdeger['kitapkaydetyayinevi'])

                        kitapkaydetkitabinturu = str(kitapkaydetdeger['kitapkaydetkitabinturu'])

                        kitapkaydetdolapkodu = str(kitapkaydetdeger['kitapkaydetdolapkodu'])

                        if kitapkaydetbarkod and kitapkaydetadi and kitapkaydetyazari and kitapkaydetyayinevi and kitapkaydetkitabinturu and kitapkaydetdolapkodu:

                            kitapkaydetpensatir = []

                            kitapkaydetbarkodeslesme = 0

                            for i in [kitapkaydetbarkod, kitapkaydetadi, kitapkaydetyazari, kitapkaydetyayinevi, kitapkaydetkitabinturu, kitapkaydetdolapkodu]:

                                kitapkaydetpensatir.append(i)

                            for i in range(0, len(kitapkaydetpenliste)):

                                if kitapkaydetpenliste[i][0] == kitapkaydetbarkod:

                                    kitapkaydetbarkodeslesme += 1

                            if kitapkaydetbarkodeslesme > 0 or mevcutmu(kitaplar, ('kitapno="' + str(kitapkaydetbarkod) + '"')):

                                gka.popup(kitapkaydetbarkod + ' No.lu kitap zaten kaydedilmiş.\nKitap No. eşsiz olmalıdır.', title='Hata')

                            else:

                                kitapkaydetpenliste.append(kitapkaydetpensatir)

                            kitapkaydetpencere['kitapkaydetliste'].update(values=kitapkaydetpenliste)

                        else:

                            gka.popup('Boş alan kalamaz!', title='Hata')

                    if kitapkaydetfiil == 'kitapkaydetonay' and len(kitapkaydetpenliste) > 0:
                            
                        kaydet(kitaplar, tuple(kitapkaydetpenliste))

                        kitapkaydetpencere['kitapkaydetdurum'].update(str(len(kitapkaydetpenliste)) + ' kayıt işlendi.')

                        kitapkaydetpenliste = []

                        kitapkaydetpencere['kitapkaydetliste'].update(values=kitapkaydetpenliste)

                    elif kitapkaydetfiil == 'kitapkaydetonay':

                        gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', title='Hata')

                    if kitapkaydetfiil == 'kitapkaydetexcel':

                        kitapexcelpencere.UnHide()

                        while True:

                            kitapexcelfiil, kitapexceldeger = kitapexcelpencere.read()

                            kitapexcelgirdi = kitapexceldeger['kitapexcelgirdi']

                            if kitapexcelfiil == 'kitapexceleaktaronay' and kitapexcelgirdi:

                                exceldosya = pd.read_excel(kitapexcelgirdi, engine='openpyxl')
                                
                                exceldosya.to_csv('temp.csv', index = None, header=True)

                                data = csvac('temp.csv')
                                
                                os.remove('temp.csv')
                                    
                                for i in data:

                                    if len(i) == 6:

                                        kitapkaydetbarkod = str(i[0])

                                        kitapkaydetadi = str(i[1])

                                        kitapkaydetyazari = str(i[2])

                                        kitapkaydetyayinevi = str(i[3])

                                        kitapkaydetkitabinturu = str(i[4])

                                        kitapkaydetdolapkodu = str(i[5])

                                    else:

                                        gka.popup('Açtığınız excel dosyasında boşluklar var. Lütfen boşluk bırakmayınız!', title='Hata')

                                        break

                                    if kitapkaydetbarkod and kitapkaydetadi and kitapkaydetyazari and kitapkaydetyayinevi and kitapkaydetkitabinturu and kitapkaydetdolapkodu:

                                        kitapkaydetpensatir = []

                                        kitapkaydetbarkodeslesme = 0

                                        for i in [kitapkaydetbarkod, kitapkaydetadi, kitapkaydetyazari, kitapkaydetyayinevi, kitapkaydetkitabinturu, kitapkaydetdolapkodu]:

                                            kitapkaydetpensatir.append(i)

                                        for i in range(0, len(kitapkaydetpenliste)):

                                            if kitapkaydetpenliste[i][0] == kitapkaydetbarkod:

                                                kitapkaydetbarkodeslesme += 1

                                        if kitapkaydetbarkodeslesme > 0 or mevcutmu(kitaplar, ('kitapno="' + str(kitapkaydetbarkod) + '"')):

                                            gka.popup(kitapkaydetbarkod + ' No.lu kitap zaten kaydedilmiş.\nKitap No. eşsiz olmalıdır.', title='Hata')

                                            break

                                        else:

                                            kitapkaydetpenliste.append(kitapkaydetpensatir)

                                        kitapkaydetpencere['kitapkaydetliste'].update(values=kitapkaydetpenliste)

                                    else:

                                        gka.popup('Boş alan kalamaz!', title='Hata')

                                        break

                            if kitapexcelfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                                kitapexcelpencere.Hide()

                                break

                    if kitapkaydetfiil == 'kitapkaydetliste':

                        kitapkaydetlistesecilen = kitapkaydetdeger['kitapkaydetliste'][0]

                    if kitapkaydetfiil == 'kitapkaydetlistesil' and kitapkaydetlistesecilen != -1 and gka.popup_yes_no(str(kitapkaydetpenliste[kitapkaydetlistesecilen][0]) + ' No.lu kitap ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?') == 'Yes':
                    
                        kitapkaydetpenliste.pop(kitapkaydetlistesecilen)

                        kitapkaydetpencere['kitapkaydetliste'].update(values=kitapkaydetpenliste)

                        kitapkaydetlistesecilen = -1

                    if kitapkaydetfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kitapkaydetpencere.Hide()

                        break

            if anafiil == 'kitapsil' and yonetici != 2:

                sorgusonuc = []

                tabloliste = []

                kitapsilpencere.UnHide()

                while True:

                    kitapsilfiil, kitapsildeger = kitapsilpencere.read()

                    kmt = ''

                    kitapsilbarkod = str(kitapsildeger['kitapsilbarkod'])

                    kitapsiladi = str(kitapsildeger['kitapsiladi'])

                    kitapsilyazari = str(kitapsildeger['kitapsilyazari'])

                    kitapsilyayinevi = str(kitapsildeger['kitapsilyayinevi'])

                    kitapsilkitabinturu = str(kitapsildeger['kitapsilkitabinturu'])

                    kitapsildolapkodu = str(kitapsildeger['kitapsildolapkodu'])

                    if kitapsilbarkod:

                        kmt += 'kitapno="' + kitapsilbarkod + '" '

                    else:

                        kmt += '1=1 '

                    if kitapsiladi:

                        kmt += ' AND kitapadi LIKE "%' + kitapsiladi + '%" '

                    if kitapsilyazari:

                        kmt += ' AND kitapyazari LIKE "%' + kitapsilyazari + '%" '

                    if kitapsilyayinevi:

                        kmt += ' AND yayinevi LIKE "%' + kitapsilyayinevi + '%" '

                    if kitapsilkitabinturu:

                        kmt += ' AND kitapturu LIKE "%' + kitapsilkitabinturu + '%" '

                    if kitapsildolapkodu:

                        kmt += ' AND rafkodu LIKE "%' + kitapsildolapkodu + '%" '

                    if kitapsilfiil == 'kitapsilsorguonay':

                        tabloliste = []

                        sorgusonuc = sorgula(kitaplar, kmt)

                        for istemciadi in istemcilistesi:

                            istemcidensorgu = sorgula(istemciadi[1] + 'kitaplar', kmt)

                            for i in istemcidensorgu:

                                temptablo = list(i)

                                temptablo.append(istemciadi[0])

                                tabloliste.append(temptablo)

                        kitapsilpencere['kitapsilsorgu'].update(values=tabloliste)

                        kitapsilpencere['kitapsildurum'].update(str(len(tabloliste)) + ' kayıt listelendi.')

                    if kitapsilfiil == 'kitapsiltopluonay' and yonetici == 1 and len(sorgusonuc) > 0:

                        if kitapsilfiil == 'kitapsiltopluonay' and gka.popup_yes_no(str(len(sorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?') == 'Yes':

                            for i in sorgusonuc:

                                sil(kitaplar, ('kitapno="' + i[0] + '"'))

                                sil(verilenkitaplar, ('kitapno="' + i[0] + '"'))

                            kitapsilpencere['kitapsildurum'].update(str(len(sorgusonuc)) + ' adet kitap silindi.')

                            kitapsilpencere['kitapsilsorgu'].update(values=sorgusonuc)

                    elif kitapsilfiil == 'kitapsiltopluonay' and yonetici != 1:

                        gka.popup('Yönetici yetkilerine sahip değilsiniz.', title='Hata')

                    if kitapsilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kitapsilpencere.Hide()

                        break

            elif anafiil == 'uyesil' and yonetici == 2:

                gka.popup('Yalnızca kitap sorgulayabilirsiniz.')

            if anafiil == 'uyekaydet' and yonetici != 2:

                uyekaydetlistesecilen = -1

                uyekaydetpencere.UnHide()

                while True:

                    uyekaydetfiil, uyekaydetdeger = uyekaydetpencere.read()

                    if uyekaydetfiil == 'uyekaydetekle':

                        uyekaydetuyeno = str(uyekaydetdeger['uyekaydetuyeno'])

                        uyekaydetuyeadi = str(uyekaydetdeger['uyekaydetuyeadi'])

                        uyekaydetuyesinifi = str(uyekaydetdeger['uyekaydetuyesinifi'])

                        if uyekaydetuyeno and uyekaydetuyeadi and uyekaydetuyesinifi:

                            uyekaydetpensatir = []

                            uyekaydetnoeslesme = 0

                            for i in [uyekaydetuyeno, uyekaydetuyeadi, uyekaydetuyesinifi]:

                                uyekaydetpensatir.append(i)

                            for i in range(0, len(uyekaydetpenliste)):

                                if uyekaydetpenliste[i][0] == uyekaydetuyeno:

                                    uyekaydetnoeslesme += 1

                            if uyekaydetnoeslesme > 0 or mevcutmu(uyeler, ('uyeno="' + str(uyekaydetuyeno) + '"')):

                                gka.popup(uyekaydetuyeno + ' No.lu üye zaten kaydedilmiş.\nÜye No. eşsiz olmalıdır.', title='Hata')

                            else:

                                uyekaydetpenliste.append(uyekaydetpensatir)

                            uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

                        else:

                            gka.popup('Boş alan kalamaz!', title='Hata')

                    if uyekaydetfiil == 'uyekaydetonay' and len(uyekaydetpenliste) > 0:
                            
                        kaydet(uyeler, tuple(uyekaydetpenliste))

                        uyekaydetpencere['uyekaydetdurum'].update(str(len(uyekaydetpenliste)) + ' kayıt işlendi.')

                        uyekaydetpenliste = []

                        uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

                    elif uyekaydetfiil == 'uyekaydetonay':

                        gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', title='Hata')

                    if uyekaydetfiil == 'uyekaydetexcel':

                        uyekaydetlistesecilen = -1

                        uyeexcelpencere.UnHide()

                        while True:

                            uyeexcelfiil, uyeexceldeger = uyeexcelpencere.read()

                            uyeexcelgirdi = uyeexceldeger['uyeexcelgirdi']

                            if uyeexcelfiil == 'uyeexceleaktaronay' and uyeexcelgirdi:

                                exceldosya = pd.read_excel(uyeexcelgirdi, engine='openpyxl')
                                
                                exceldosya.to_csv('temp.csv', index = None, header=True)

                                data = csvac('temp.csv')
                                
                                os.remove('temp.csv')
                                    
                                for i in data:
                                        
                                    if len(i) == 3:

                                        uyekaydetuyeno = str(i[0])

                                        uyekaydetuyeadi = str(i[1])

                                        uyekaydetuyesinifi = str(i[2])

                                    else:

                                        gka.popup('Açtığınız excel dosyasında boşluklar var. Lütfen boşluk bırakmayınız!', title='Hata')

                                    if uyekaydetuyeno and uyekaydetuyeadi and uyekaydetuyesinifi:

                                        uyekaydetpensatir = []

                                        uyekaydetbarkodeslesme = 0

                                        for i in [uyekaydetuyeno, uyekaydetuyeadi, uyekaydetuyesinifi]:

                                            uyekaydetpensatir.append(i)

                                        for i in range(0, len(uyekaydetpenliste)):

                                            if uyekaydetpenliste[i][0] == uyekaydetuyeno:

                                                uyekaydetbarkodeslesme += 1

                                        if uyekaydetbarkodeslesme > 0 or mevcutmu(uyeler, ('uyeno="' + str(uyekaydetuyeno) + '"')):

                                            gka.popup(uyekaydetuyeno + ' No.lu üye zaten kaydedilmiş.\nÜye No. eşsiz olmalıdır.', title='Hata')

                                            break

                                        else:

                                            uyekaydetpenliste.append(uyekaydetpensatir)

                                        uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

                                    else:

                                        gka.popup('Boş alan kalamaz!', title='Hata')

                                        break

                            if uyeexcelfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                                uyeexcelpencere.Hide()

                                break

                    if uyekaydetfiil == 'uyekaydetliste':

                        uyekaydetlistesecilen = uyekaydetdeger['uyekaydetliste'][0]

                    if uyekaydetfiil == 'uyekaydetlistesil' and uyekaydetlistesecilen != -1 and gka.popup_yes_no(str(uyekaydetpenliste[uyekaydetlistesecilen][0]) + ' No.lu üye ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?') == 'Yes':
                    
                        uyekaydetpenliste.pop(uyekaydetlistesecilen)

                        uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

                        uyekaydetlistesecilen = -1
                    
                    if uyekaydetfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        uyekaydetpencere.Hide()

                        break

            elif anafiil == 'uyekaydet' and yonetici == 2:

                gka.popup('Ziyaretçiler yalnızca sorgulama yapabilir.', title='Hata')

            if anafiil == 'uyesil':

                uyesorgusonuc = []

                uyesilpencere.UnHide()

                while True:

                    uyesilfiil, uyesildeger = uyesilpencere.read()

                    kmt = ''

                    uyesiluyeno = str(uyesildeger['uyesiluyeno'])

                    uyesiladisoyadi = str(uyesildeger['uyesiladisoyadi'])

                    uyesilsinifi = str(uyesildeger['uyesilsinifi'])

                    if uyesiluyeno:

                        kmt += 'uyeno="' + uyesiluyeno + '" '

                    else:

                        kmt += '1=1 '

                    if uyesiladisoyadi:

                        kmt += ' AND uyeadi LIKE "%' + uyesiladisoyadi + '%" '

                    if uyesilsinifi:

                        kmt += ' AND uyesinifi LIKE "%' + uyesilsinifi + '%" '

                    if uyesilfiil == 'uyesilsorguonay':

                        tabloliste = []

                        uyesorgusonuc = sorgula(uyeler, kmt)

                        for istemciadi in istemcilistesi:

                            istemcidensorgu = sorgula(istemciadi[1] + 'uyeler', kmt)

                            for i in istemcidensorgu:

                                temptablo = list(i)

                                temptablo.append(istemciadi[0])

                                tabloliste.append(temptablo)

                        uyesilpencere['uyesilliste'].update(values=tabloliste)

                        uyesilpencere['uyesildurum'].update(str(len(tabloliste)) + ' kayıt listelendi.')
 
                    if uyesilfiil == 'uyesiltopluonay' and yonetici == 1 and len(uyesorgusonuc) > 0:

                        if uyesilfiil == 'uyesiltopluonay' and gka.popup_yes_no(str(len(uyesorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?') == 'Yes':

                            for i in uyesorgusonuc:

                                sil(verilenkitaplar, ('uyeno="' + i[0] + '"'))

                                sil(uyeler, ('uyeno="' + i[0] + '"'))

                            uyesilpencere['uyesildurum'].update(str(len(uyesorgusonuc)) + ' adet kayıt silindi.')

                            uyesorgusonuc = sorgula(uyeler, kmt)

                            uyesilpencere['uyesilliste'].update(values=uyesorgusonuc)

                    elif uyesilfiil == 'uyesiltopluonay' and yonetici != 1:

                        gka.popup('Yönetici yetkilerine sahip değilsiniz.', title='Hata')

                    if uyesilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        uyesilpencere.Hide()

                        break

            if anafiil == 'kullanicikaydet' and yonetici == 1:

                kullanicikaydetlistesecilen = -1

                kullanicikaydetpencere.UnHide()

                while True:

                    kullanicikaydetfiil, kullanicikaydetdeger = kullanicikaydetpencere.read()

                    if kullanicikaydetfiil == 'kullanicikaydetekle':

                        kullanicikaydetadi = str(kullanicikaydetdeger['kullanicikaydetadi'])

                        kullanicikaydetsifre = str(kullanicikaydetdeger['kullanicikaydetsifre'])

                        kullanicikaydetyetki = str(kullanicikaydetdeger['kullanicikaydetyetki'])

                        if kullanicikaydetadi and kullanicikaydetsifre and kullanicikaydetyetki:

                            kullanicikaydetpensatir = []

                            kullanicikaydetnoeslesme = 0

                            for i in [kullanicikaydetadi, kullanicikaydetsifre, kullanicikaydetyetki]:

                                kullanicikaydetpensatir.append(i)

                            for i in range(0, len(kullanicikaydetpenliste)):

                                if kullanicikaydetpenliste[i][0] == kullanicikaydetadi:

                                    kullanicikaydetnoeslesme += 1

                            if kullanicikaydetnoeslesme > 0 or mevcutmu(kullanicilar, ('kullaniciadi="' + str(kullanicikaydetadi) + '"')):

                                gka.popup(kullanicikaydetadi + ' adlı kullanıcı zaten kaydedilmiş.\nKullanıcı Adı eşsiz olmalıdır.', title='Hata')

                            else:

                                kullanicikaydetpenliste.append(kullanicikaydetpensatir)

                            kullanicikaydetpencere['kullanicikaydetliste'].update(values=kullanicikaydetpenliste)

                        else:

                            gka.popup('Boş alan kalamaz!', title='Hata')

                    if kullanicikaydetfiil == 'kullanicikaydetonay' and len(kullanicikaydetpenliste) > 0:
                            
                        kaydet(kullanicilar, tuple(kullanicikaydetpenliste))

                        kullanicikaydetpencere['kullanicikaydetdurum'].update(str(len(kullanicikaydetpenliste)) + ' kayıt işlendi.')

                        kullanicikaydetpenliste = []

                        kullanicikaydetpencere['kullanicikaydetliste'].update(values=kullanicikaydetpenliste)

                    elif kullanicikaydetfiil == 'kullanicikaydetonay':

                        gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', title='Hata')

                    if kullanicikaydetfiil == 'kullanicikaydetliste':

                        kullanicikaydetlistesecilen = kullanicikaydetdeger['kullanicikaydetliste'][0]

                    if kullanicikaydetfiil == 'kullanicikaydetlistesil' and kullanicikaydetlistesecilen != -1 and gka.popup_yes_no(str(kullanicikaydetpenliste[kullanicikaydetlistesecilen][0]) + ' adlı kullanıcı ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?') == 'Yes':
                        
                        kullanicikaydetpenliste.pop(kullanicikaydetlistesecilen)

                        kullanicikaydetpencere['kullanicikaydetliste'].update(values=kullanicikaydetpenliste)

                        kullanicikaydetlistesecilen = -1
                    
                    if kullanicikaydetfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kullanicikaydetpencere.Hide()

                        break

            elif anafiil == 'kullanicikaydet' and yonetici == 0:

                gka.popup('Yönetici yetkilerine sahip değilsiniz', title='Hata')

            if anafiil == 'kullanicisil' and yonetici == 1:

                kullanicisorgusonuc = []

                kullanicisilpencere.UnHide()

                while True:

                    kullanicisilfiil, kullanicisildeger = kullanicisilpencere.read()

                    kmt = ''

                    kullanicisiladi = str(kullanicisildeger['kullanicisiladi'])

                    kullanicisilsifre = str(kullanicisildeger['kullanicisilsifre'])

                    kullanicisilyetki = str(kullanicisildeger['kullanicisilyetki'])

                    if kullanicisiladi:

                        kmt += 'kullaniciadi="' + kullanicisiladi + '" '

                    else:

                        kmt += '1=1 '

                    if kullanicisilsifre:

                        kmt += ' AND sifre="' + kullanicisilsifre + '" '

                    if kullanicisilyetki:

                        kmt += ' AND yetki="' + kullanicisilyetki + '" '

                    if kullanicisilfiil == 'kullanicisilsorguonay':

                        kullanicisorgusonuc = sorgula(kullanicilar, kmt)

                        kullanicisilpencere['kullanicisilliste'].update(values=kullanicisorgusonuc)

                        kullanicisilpencere['kullanicisildurum'].update(str(len(kullanicisorgusonuc)) + ' kayıt listelendi.')

                    if kullanicisilfiil == 'kullanicisiltopluonay' and yonetici == 1 and len(kullanicisorgusonuc) > 0:

                        if kullanicisilfiil == 'kullanicisiltopluonay' and gka.popup_yes_no(str(len(kullanicisorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?') == 'Yes':

                            for i in kullanicisorgusonuc:

                                sil(kullanicilar, ('kullaniciadi="' + i[0] + '"'))

                            if len(sorgula(kullanicilar, '1=1')) == 0:

                                mysqlsorgucalistir('INSERT INTO ' + kullanicilar + ' VALUES ("DEVKÜTÜP", "12345", "Yönetici");')

                                gka.popup('Kullanıcıların tamamını sildiniz.\nProgramın kilitlenmesini önlemek için varsayılan kullanıcı,\nKullanıcı Adı: DEVKÜTÜP\nŞifre: 12345\nYetkiler: Yönetici\noluşturuldu.', title='Uyarı')

                            kullanicisilpencere['kullanicisildurum'].update(str(len(kullanicisorgusonuc)) + ' adet kayıt silindi.')

                            kullanicisorgusonuc = sorgula(kullanicilar, kmt)

                            kullanicisilpencere['kullanicisilliste'].update(values=kullanicisorgusonuc)

                    if kullanicisilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

                        kullanicisilpencere.Hide()

                        break

            elif anafiil == 'kullanicisil' and yonetici == 0:

                gka.popup('Yönetici yetkilerine sahip değilsiniz', title='Hata')

    while True:

        girisfiil, girisdeger = girispencere.read()

        if girisfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            girispencere.Hide()

            break

        kullaniciadi = str(girisdeger['kullaniciadi'])

        sifre = str(girisdeger['sifre'])

        if girisfiil == 'girisyap' and kullaniciadi and sifre:

            if mevcutmu(kullanicilar, 'kullaniciadi="' + kullaniciadi + '" AND sifre="' + sifre + '"'):

                yetki = sorgula(kullanicilar, 'kullaniciadi="' + kullaniciadi + '"')[0][2]

                if yetki == 'Görevli':

                    yonetici = 0

                elif yetki == 'Yönetici':

                    yonetici = 1

                elif yetki == 'Ziyaretçi':

                    yonetici = 2

                girispencere.Hide()

                anadongu()

                girispencere.UnHide()

            else:

                gka.popup('Kullanıcı Adı veya Şifre yanlış.', title='Hata')

if istemci == 1:

    istemciduzen = [[gka.Text('Lütfen istemci seçiniz.')]]

    for i in istemcilistesi:

        istemciduzen.append([gka.Button(i[0], key=i[1], s=(40,1), font=(8))])

    istemcipencere = gka.Window('DEVKÜTÜP ' + surum + ' İstemci Formu', istemciduzen, enable_close_attempted_event=True, finalize=True)

    while True:

        istemcipencerefiil, istemcipenceredeger = istemcipencere.read()

        for i in istemcilistesi:

            istemcikaydet(i[1])

            if istemcipencerefiil == i[1]:

                istemcipencere.Hide()

                program(i[1] + 'kitaplar', i[1] + 'kullanicilar', i[1] + 'uyeler', i[1] + 'verilenkitaplar')

                istemcipencere.UnHide()

        if istemcipencerefiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            if kapatmatercih == 1:

                gka.popup('Program, yöneticiniz tarafından kapatılamayacak şekilde ayarlandı.', title='Hata')

            if kapatmatercih == 0:

                sys.exit()

else:

    istemcikaydet('')

    istemcilistesi = [['', '']]

    program('kitaplar', 'kullanicilar', 'uyeler', 'verilenkitaplar')

    sys.exit()
