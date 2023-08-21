## Bu program Creative Commons Atıf Gayri-Ticari 4.0 Uluslararası Kamu Lisansı ile lisanslanmıştır.
## Atıfta bulunurken 'libsoykan-dev' veya 'Naim Salih SOYKAN' olarak belirtebilirsiniz.
## Lisansın bir kopyasını program ile birlikte edinmiş olmanız gerekir. Eğer edinmediyseniz: https://creativecommons.org/licenses/by-nc/4.0/deed.tr

import PySimpleGUI as gka # Grafik kullanıcı arabirimi (gka) içinn kullanılır

import mysql.connector # MYSQL temel fonksiyonlarının ve sorguların çalıştırılması için kullanılır

from datetime import datetime # Zaman damgalarını işlemek için kullanılır

import time # Zaman damgalarını unix formatında elde etmek için kullanılır

import pandas as pd # Excel dosyalarını dönüştürmek için kullanılır

import csv # Dönüştürülen excel dosyalarını tabloya aktarmak için kullanılır

import os # Dosya sistemi fonksiyonlarının işletilmesi için kullanılır

import sys # Sys fonksiyonları

import configparser # Config dosyalarının okunması için kullanılır

config = configparser.ConfigParser()

surum = 'v1.18_20230821'

################################################################################################################################

### TEMEL FONKSİYONLAR

################################################################################################################################

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

        gka.popup('MYSQL Hatası:\n' + hata, keep_on_top=True , title='Hata')

        return None

    netice = kullanim0.fetchall()

    if netice[0][0] > 0:

        return True

    else:

        return False

def olustur(tablo, liste):
        
    try:

        for i in liste:

            kullanim1 = mydb.cursor()

            kullanim1.execute('INSERT INTO ' + tablo + ' VALUES ' + str(tuple(i)) + ';')

    except mysql.connector.Error as hata:

        gka.popup('MYSQL Hatası:\n' + hata, keep_on_top=True , title='Hata')

def sil(tablo, kosul):

        kullanim2 = mydb.cursor()

        try:

            kullanim2.execute('DELETE FROM ' + tablo + ' WHERE ' + kosul + ';')

        except mysql.connector.Error as hata:

            gka.popup('MYSQL Hatası:\n' + hata, keep_on_top=True , title='Hata')

def sorgula(tablo, kosul):

        kullanim3 = mydb.cursor()

        try:

            kullanim3.execute('SELECT * FROM ' + tablo + ' WHERE ' + kosul + ';')

        except mysql.connector.Error as hata:

            gka.popup('MYSQL Hatası:\n' + str(hata), keep_on_top=True , title='Hata')

            [['Hata']]

        return kullanim3.fetchall()

def istemciolustur(istemciadi):
        
    try:

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'kayitlar (kayitno varchar(50), kayitadi varchar(50), kayitkaynagi varchar(50), yayimci varchar(50), kayitturu varchar(50), rafkodu varchar(50), digernitelikler varchar(32768));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'kullanicilar (kullaniciadi varchar(50), sifre varchar(50), yetki varchar(50));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'uyeler (uyeno varchar(50), uyeadi varchar(50), uyesinifi varchar(50));')

        mysqlsorgucalistir('CREATE TABLE IF NOT EXISTS ' + istemciadi + 'emanet (uyeno varchar(50), uyeadi varchar(50), uyesinifi varchar(50), kayitno varchar(50), kayitadi varchar(50), kayitkaynagi varchar(50), yayimci varchar(50), kayitturu varchar(50), rafkodu varchar(50), verildigizaman varchar(50), gunsayisi varchar(50));')

    except mysql.connector.Error as hata:

        gka.popup('MYSQL Hatası:\n' + hata, keep_on_top=True , title='Hata')

################################################################################################################################

### DOSYA KONTROL

################################################################################################################################

if os.path.exists('istemciler.csv') and os.path.exists('devkutup.conf'):

    istemcilistesi = csvac('istemciler.csv')

    config.read_file(open(r'devkutup.conf'))

    try:

        mysqlport = int(config.get('mysql-giris', 'port'))

        mysqlsifre = str(config.get('mysql-giris', 'sifre'))

        mysqlka = str(config.get('mysql-giris', 'kullaniciadi'))

        mysqlip = str(config.get('mysql-giris', 'ip'))

        tema = str(config.get('diger', 'tema'))

        kapatmatercih = int(config.get('diger', 'kapatmatercih'))

        istemci = int(config.get('diger', 'istemci'))

    except configparser.Error as hata:

        gka.popup('Config dosyası yanlış:\n' + str(hata), keep_on_top=True , title='Kritik Hata')

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
    kapatmatercih = 1''', keep_on_top=True , title='Uyarı')

    mysqlport = 3311

    mysqlsifre = ''

    mysqlka = 'root'

    mysqlip = 'localhost'

    istemci = 0
    
    tema = 'Black'

    kapatmatercih =  1

elif os.path.exists('devkutup.conf') and istemci == 1:

    gka.popup('İstemci listesi (istemciler.csv) yüklenemedi.\nİstemci listesi yüklenmesi yapılandırma dosyasında "istemci = 1" olarak ayarlandığında zorunludur.', keep_on_top=True , title='Kritik Hata')

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
    
istemciler.csv, config dosyasında istemci = 0 olarak ayarlandığında zorunlu değildir.''', keep_on_top=True , title='Kritik Hata')

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

    gka.popup('MYSQL Hatası:\n' + str(hata), keep_on_top=True , title='Kritik Hata')

    sys.exit()

mysqlsorgucalistir = mydb.cursor().execute

gka.theme(tema)

################################################################################################################################

### GİRİŞ YAP

################################################################################################################################

girispencere = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullaniciadi')],
                [gka.Text('Şifre', s=(10,1)), gka.Input(key='sifre')],
                [gka.Button('Giriş Yap', key='girisyap')]]

girispencere = gka.Window('DEVKÜTÜP ' + surum + ' Giriş Yap', girispencere, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

girispencere.Hide()

def girisyap(kayitlar, kullanicilar, uyeler, emanet):

    if len(sorgula(kullanicilar, '1=1')) == 0:

        mysqlsorgucalistir('INSERT INTO ' + kullanicilar + ' VALUES ("DEVKÜTÜP", "12345", "Yönetici");')

        gka.popup('Kayıtlı kullanıcı yok. Varsayılan kullanıcı,\nKullanıcı Adı: DEVKÜTÜP\nŞifre: 12345\nYetkiler: Yönetici\noluşturuldu.', keep_on_top=True , title='Uyarı')

    girispencere.UnHide()

    while True:

        girisfiil, girisdeger = girispencere.read()

        if girisfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            girispencere.Hide()

            break

        kullaniciadi = str(girisdeger['kullaniciadi'])

        sifre = str(girisdeger['sifre'])

        if girisfiil == 'girisyap' and kullaniciadi and sifre:

            if '"' in kullaniciadi or '"' in sifre:

                gka.popup("Senin koyun gütmüşlüğün kadar benim çoban dövmüşlüğüm vardır yeğenim. Akıllı ol!", keep_on_top=True , title="Hoop birader ne iş?")

                girispencere.Hide()

                break

            if mevcutmu(kullanicilar, 'kullaniciadi="' + kullaniciadi + '" AND sifre="' + sifre + '"'):

                yetki = sorgula(kullanicilar, 'kullaniciadi="' + kullaniciadi + '"')[0][2]

                if yetki == 'Görevli':

                    yonetici = 0

                elif yetki == 'Yönetici':

                    yonetici = 1

                elif yetki == 'Ziyaretçi':

                    yonetici = 2

                girispencere.Hide()

                program(kayitlar=kayitlar, kullanicilar=kullanicilar, uyeler=uyeler, emanet=emanet, yonetici=yonetici)

            else:

                gka.popup('Kullanıcı Adı veya Şifre yanlış.', keep_on_top=True , title='Hata')

################################################################################################################################

### KULLANICI ANA SAYFASI

################################################################################################################################

anaduzen = [[gka.Text('KAYIT İŞLEMLERİ:', s=(24,1), font=(8)),
             gka.Button('Kayıt Oluştur', key='kayitolustur', s=(24,1), font=(8)), gka.Button('Kayıt Sorgula veya Sil', key='kayitsil', s=(24,1), font=(8))],
            [gka.Text('ÜYE İŞLEMLERİ:', s=(24,1), font=(8)),
             gka.Button('Üye Kaydet', key='uyekaydet', s=(24,1), font=(8)), gka.Button('Üye Sorgula veya Sil', key='uyesil', s=(24,1), font=(8))],
            [gka.Text('EMANET İŞLEMLERİ:', s=(24,1), font=(8)),
             gka.Button('Teslim Al', key='emanetal', s=(24,1), font=(8)), gka.Button('Emanet Ver', key='emanetver', s=(24,1), font=(8))],
            [gka.Text('KULLANICI İŞLEMLERİ:', s=(24,1), font=(8)),
             gka.Button('Kullanıcı Kaydet', key='kullaniciolustur', s=(24,1), font=(8)), gka.Button('Kullanıcı Sil', key='kullanicisil', s=(24,1), font=(8))],
            [gka.Text('RAPOR İŞLEMLERİ:', s=(24,1), font=(8)),
             gka.Button('Emanet Listesi', key='emanetlistesi', s=(24,1), font=(8)), gka.Button('Sayaçlar', key='sayaclar', s=(24,1), font=(8))]]

anapencere = gka.Window('DEVKÜTÜP ' + surum + ' (C) 2022 libsoykan-dev', anaduzen, enable_close_attempted_event=True, finalize=True)

anapencere.Hide()

def program(kayitlar, kullanicilar, uyeler, emanet, yonetici):

    anapencere.UnHide()

    while True:

        anafiil, anadeger = anapencere.read()

        if anafiil == gka.WIN_CLOSE_ATTEMPTED_EVENT:

            anapencere.Hide()

            girispencere.UnHide()

            break

        if anafiil == 'kayitolustur' and yonetici != 2:

            kayitolustur(kayitlar=kayitlar)

        if anafiil == 'kayitsil' and yonetici != 2:

            kayitsil(kayitlar=kayitlar, yonetici=yonetici)

        if anafiil == 'uyekaydet' and yonetici != 2:

            uyekaydet(uyeler=uyeler)

        if anafiil == 'uyesil' and yonetici != 2:

            uyesil(uyeler=uyeler, yonetici=yonetici)

        if anafiil == 'emanetal' and yonetici != 2:

            emanetal(emanet=emanet)

        if anafiil == 'emanetver' and yonetici != 2:

            emanetver(kayitlar=kayitlar, uyeler=uyeler, emanet=emanet)

        if anafiil == 'kullaniciolustur' and yonetici == 1:

            kullaniciolustur(kullanicilar=kullanicilar)

        if anafiil == 'kullanicisil' and yonetici == 1:

            kullanicisil(kullanicilar=kullanicilar)

        if anafiil == 'emanetlistesi' and yonetici != 2:

            emanetlistesi(emanet=emanet)

        if anafiil == 'sayaclar':

            sayaclar(kayitlar=kayitlar, uyeler=uyeler, kullanicilar=kullanicilar, emanet=emanet)

################################################################################################################################

### KAYIT OLUŞTUR

################################################################################################################################

kayitolusturduzen = [[gka.Text('Kayıt No.', s=(10,1)), gka.Input(key='kayitolusturbarkod'), gka.Text('Adı', s=(10,1)), gka.Input(key='kayitolusturadi')],
                     [gka.Text('Yazarı', s=(10,1)), gka.Input(key='kayitolusturkaynagi'), gka.Text('Yayımcı', s=(10,1)), gka.Input(key='kayitolusturyayimci')],
                     [gka.Text('Türü', s=(10,1)), gka.Input(key='kayitolusturturu'), gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='kayitolusturdolapkodu')],
                     [gka.Text('Ek Nitelikler', s=(10,1)), gka.Multiline(s=(103,5), key='kayitolusturnitelikler', )],
                     [gka.Button('Ekle', key='kayitolusturekle'), gka.Button("Excel'den Aktar", key='kayitolusturexcel')],
                     [gka.Table([], ['Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu', 'Ek Nitelikler'], num_rows=20, key='kayitolusturliste', def_col_width=13, auto_size_columns=False, enable_events=True)],
                     [gka.Button('Kaydet', key='kayitolusturonay'), gka.Button('Satırı Sil', key='kayitolusturlistesil'), gka.Text(key='kayitolusturdurum')]]

kayitolusturpencere = gka.Window('Kayıt Kaydet', kayitolusturduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

kayitolusturpencere.Hide()

def kayitolustur(kayitlar):

    kayitolusturpenliste = []

    kayitolusturlistesecilen = -1

    kayitolusturpencere.UnHide()

    while True:

        kayitolusturfiil, kayitolusturdeger = kayitolusturpencere.read()

        if kayitolusturfiil == 'kayitolusturekle':

            kayitolusturbarkod = str(kayitolusturdeger['kayitolusturbarkod'])

            kayitolusturadi = str(kayitolusturdeger['kayitolusturadi'])

            kayitolusturkaynagi = str(kayitolusturdeger['kayitolusturkaynagi'])

            kayitolusturyayimci = str(kayitolusturdeger['kayitolusturyayimci'])

            kayitolusturturu = str(kayitolusturdeger['kayitolusturturu'])

            kayitolusturdolapkodu = str(kayitolusturdeger['kayitolusturdolapkodu'])

            kayitolusturnitelikler = str(kayitolusturdeger['kayitolusturnitelikler'])

            if kayitolusturbarkod and kayitolusturadi and kayitolusturkaynagi and kayitolusturyayimci and kayitolusturturu and kayitolusturdolapkodu and kayitolusturnitelikler:

                if '"' not in kayitolusturbarkod and '"' not in kayitolusturadi and '"' not in kayitolusturkaynagi and '"' not in kayitolusturyayimci and '"' not in kayitolusturturu and '"' not in kayitolusturdolapkodu and '"' not in kayitolusturnitelikler:

                    kayitolusturpensatir = []

                    kayitolusturbarkodeslesme = 0

                    for i in [kayitolusturbarkod, kayitolusturadi, kayitolusturkaynagi, kayitolusturyayimci, kayitolusturturu, kayitolusturdolapkodu, kayitolusturnitelikler]:

                        kayitolusturpensatir.append(i)

                    for i in range(0, len(kayitolusturpenliste)):

                        if kayitolusturpenliste[i][0] == kayitolusturbarkod:

                            kayitolusturbarkodeslesme += 1

                    if kayitolusturbarkodeslesme > 0 or mevcutmu(kayitlar, ('kayitno="' + str(kayitolusturbarkod) + '"')):

                        gka.popup(kayitolusturbarkod + ' No.lu kayıt zaten oluşturulmuş.\nKayıt No. eşsiz olmalıdır.', keep_on_top=True , title='Hata')

                    else:

                        kayitolusturpenliste.append(kayitolusturpensatir)

                    kayitolusturpencere['kayitolusturliste'].update(values=kayitolusturpenliste)

                elif '"' in kayitolusturbarkod or '"' in kayitolusturadi or '"' in kayitolusturkaynagi or '"' in kayitolusturyayimci or '"' in kayitolusturturu or '"' in kayitolusturdolapkodu or '"' in kayitolusturnitelikler: 

                    gka.popup('Geçersiz karakter kullandınız.', keep_on_top=True , title='Hata')

            else:

                gka.popup('Boş alan kalamaz!', keep_on_top=True , title='Hata')

        if kayitolusturfiil == 'kayitolusturonay' and len(kayitolusturpenliste) > 0:
                
            olustur(kayitlar, tuple(kayitolusturpenliste))

            kayitolusturpencere['kayitolusturdurum'].update(str(len(kayitolusturpenliste)) + ' kayıt işlendi.')

            kayitolusturpenliste = []

            kayitolusturpencere['kayitolusturliste'].update(values=kayitolusturpenliste)

        elif kayitolusturfiil == 'kayitolusturonay':

            gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', keep_on_top=True , title='Hata')

        if kayitolusturfiil == 'kayitolusturexcel':

            kayitolusturpenliste = exceldenaktar(True, kayitolusturpenliste, 'kayitlar', 7)

            kayitolusturpencere['kayitolusturliste'].update(values=kayitolusturpenliste)

        if kayitolusturfiil == 'kayitolusturliste':

            kayitolusturlistesecilen = kayitolusturdeger['kayitolusturliste'][0]

        if kayitolusturfiil == 'kayitolusturlistesil' and kayitolusturlistesecilen != -1 and gka.popup_yes_no(str(kayitolusturpenliste[kayitolusturlistesecilen][0]) + ' No.lu kayit ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?', keep_on_top=True, title='Onay') == 'Yes':
        
            kayitolusturpenliste.pop(kayitolusturlistesecilen)

            kayitolusturpencere['kayitolusturliste'].update(values=kayitolusturpenliste)

            kayitolusturlistesecilen = -1

        if kayitolusturfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            kayitolusturpencere.Hide()

            break

################################################################################################################################

### KAYIT SORGULA VEYA SİL

################################################################################################################################

kayitsilduzen = [[gka.Text('Kayıt No.', s=(10,1)), gka.Input(key='kayitsilbarkod', s=(48,1)), gka.Text('Adı', s=(10,1)), gka.Input(key='kayitsiladi', s=(48,1))],
                  [gka.Text('Yazarı', s=(10,1)), gka.Input(key='kayitsilkaynagi', s=(48,1)), gka.Text('Yayımcı', s=(10,1)), gka.Input(key='kayitsilyayimci', s=(48,1))],
                  [gka.Text('Türü', s=(10,1)), gka.Input(key='kayitsilturu', s=(48,1)), gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='kayitsildolapkodu', s=(48,1))],
                  [gka.Text('Ek Nitelikler', s=(10,1)), gka.Multiline(s=(110,5),  key='kayitsilnitelikleri')],
                  [gka.Table([], ['Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu', 'Ek Nitelikler', 'Kütüphane'], num_rows=20, key='kayitsilsorgu', def_col_width=12, auto_size_columns=False, enable_events=True)],
                  [gka.Output(s=(123,15), key='kayitsildetay')],
                  [gka.Button('Sorgula', key='kayitsilsorguonay'), gka.Button('Tüm Kütüphanelerde Sorgula', key='kayitsilistemcisorguonay'), gka.Button('Listedekileri Sil', key='kayitsiltopluonay'), gka.Button("Excel'e Aktar", key='kayitsilexcel'), gka.Text(key='kayitsildurum')]]

kayitsilpencere = gka.Window('Kayıt Sil', kayitsilduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

kayitsilpencere.Hide()

def kayitsil(kayitlar, yonetici):

    sorgusonuc = []

    kayitsilpencere.UnHide()

    while True:

        kayitsilfiil, kayitsildeger = kayitsilpencere.read()

        kmt = ''

        kayitsilbarkod = str(kayitsildeger['kayitsilbarkod'])

        kayitsiladi = str(kayitsildeger['kayitsiladi'])

        kayitsilkaynagi = str(kayitsildeger['kayitsilkaynagi'])

        kayitsilyayimci = str(kayitsildeger['kayitsilyayimci'])

        kayitsilturu = str(kayitsildeger['kayitsilturu'])

        kayitsildolapkodu = str(kayitsildeger['kayitsildolapkodu'])

        kayitsilnitelikleri = str(kayitsildeger['kayitsilnitelikleri'])

        if kayitsilbarkod:

            kmt += 'kayitno LIKE "%' + kayitsilbarkod + '%" '

        else:

            kmt += '1=1 '

        if kayitsiladi:

            kmt += ' AND kayitadi LIKE "%' + kayitsiladi + '%" '

        if kayitsilkaynagi:

            kmt += ' AND kayitkaynagi LIKE "%' + kayitsilkaynagi + '%" '

        if kayitsilyayimci:

            kmt += ' AND yayimci LIKE "%' + kayitsilyayimci + '%" '

        if kayitsilturu:

            kmt += ' AND kayitturu LIKE "%' + kayitsilturu + '%" '

        if kayitsildolapkodu:

            kmt += ' AND rafkodu LIKE "%' + kayitsildolapkodu + '%" '

        if kayitsilnitelikleri:

            kmt += ' AND digernitelikler LIKE "%' + kayitsilnitelikleri + '%" '

        if kayitsilfiil == 'kayitsilsorguonay':

            istemcisorgu = False

            sorgusonuc = sorgula(kayitlar, kmt)

            kayitsilpencere['kayitsilsorgu'].update(values=sorgusonuc)

            kayitsilpencere['kayitsildurum'].update(str(len(sorgusonuc)) + ' kayıt listelendi.')

        if kayitsilfiil == 'kayitsilsorgu':

            multilinetemp = ''''''

            secilensatir = sorgusonuc[kayitsildeger['kayitsilsorgu'][0]]

            for i in range(7):

                baslikliste = ['Kayıt No.', '\nAdı: ', '\nYazarı: ', '\nYayımcı: ', '\nTürü: ', '\nRaf Kodu: ', '\nEk Nitelikler: ']

                multilinetemp += (baslikliste[i] + secilensatir[i])

            kayitsilpencere['kayitsildetay'].update(multilinetemp)

        if kayitsilfiil == 'kayitsiltopluonay' and yonetici == 1 and len(sorgusonuc) > 0:

            if kayitsilfiil == 'kayitsiltopluonay' and istemcisorgu == False and gka.popup_yes_no(str(len(sorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?', keep_on_top=True, title='Onay') == 'Yes':

                for i in sorgusonuc:

                    sil(kayitlar, ('kayitno="' + i[0] + '"'))

                kayitsilpencere['kayitsildurum'].update(str(len(sorgusonuc)) + ' adet kayit silindi.')

                sorgusonuc = sorgula(kayitlar, kmt)

                kayitsilpencere['kayitsilsorgu'].update(values=sorgusonuc)

        elif kayitsilfiil == 'kayitsiltopluonay' and yonetici != 1:

            gka.popup('Yönetici yetkilerine sahip değilsiniz.', keep_on_top=True , title='Hata')

        if kayitsilfiil == 'kayitsiltopluonay' and istemcisorgu == True:

            gka.popup('Diğer istemcilerin kayıtları yalnızca okunabilir.', keep_on_top=True , title='Hata')

        if kayitsilfiil == 'kayitsilexcel':

            exceleaktar(sorgusonuc, sutunlar=['Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu', 'Ek Nitelikler', 'Kütüphane'])

        if kayitsilfiil == 'kayitsilistemcisorguonay' and istemci == 1:

            sorgusonuc = []

            istemcisorgu = True

            for i in istemcilistesi:

                for a in sorgula((i[1] + 'kayitlar'), kmt):

                    kayitsiltempsatir = []

                    for b in a:

                        kayitsiltempsatir.append(b)

                    kayitsiltempsatir.append(i[0])
                    
                    sorgusonuc.append(kayitsiltempsatir)

            kayitsilpencere['kayitsilsorgu'].update(values=sorgusonuc)

            kayitsilpencere['kayitsildurum'].update(str(len(sorgusonuc)) + ' kayıt listelendi.')

        if kayitsilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            kayitsilpencere.Hide()

            break

################################################################################################################################

### ÜYE KAYDET

################################################################################################################################

uyekaydetduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='uyekaydetuyeno')],
                  [gka.Text('Üye Adı', s=(10,1)), gka.Input(key='uyekaydetuyeadi')],
                  [gka.Text('Üye Sınıfı', s=(10,1)), gka.Input(key='uyekaydetuyesinifi')],
                  [gka.Button('Ekle', key='uyekaydetekle'), gka.Button("Excel'den Aktar", key='uyekaydetexcel')],
                  [gka.Table([], ['Üye No.', 'Üye Adı', 'Üye Sınıfı'], num_rows=20, key='uyekaydetliste', def_col_width=15, auto_size_columns=False, enable_events=True)],
                  [gka.Button('Kaydet', key='uyekaydetonay'), gka.Button('Satırı Sil', key='uyekaydetlistesil'), gka.Text(key='uyekaydetdurum')]]

uyekaydetpencere = gka.Window('Üye Kaydet', uyekaydetduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

uyekaydetpencere.Hide()

def uyekaydet(uyeler):

    uyekaydetpenliste = []

    uyekaydetlistesecilen = -1

    uyekaydetpencere.UnHide()

    while True:

        uyekaydetfiil, uyekaydetdeger = uyekaydetpencere.read()

        if uyekaydetfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            uyekaydetpencere.Hide()

            break

        if uyekaydetfiil == 'uyekaydetekle':

            uyekaydetuyeno = str(uyekaydetdeger['uyekaydetuyeno'])

            uyekaydetuyeadi = str(uyekaydetdeger['uyekaydetuyeadi'])

            uyekaydetuyesinifi = str(uyekaydetdeger['uyekaydetuyesinifi'])

            if uyekaydetuyeno and uyekaydetuyeadi and uyekaydetuyesinifi and '"' not in uyekaydetuyeno and '"' not in uyekaydetuyeadi and '"' not in uyekaydetuyesinifi:

                    uyekaydetpensatir = []

                    uyekaydetnoeslesme = 0

                    for i in [uyekaydetuyeno, uyekaydetuyeadi, uyekaydetuyesinifi]:

                        uyekaydetpensatir.append(i)

                    for i in range(0, len(uyekaydetpenliste)):

                        if uyekaydetpenliste[i][0] == uyekaydetuyeno:

                            uyekaydetnoeslesme += 1

                    if uyekaydetnoeslesme > 0 or mevcutmu(uyeler, ('uyeno="' + str(uyekaydetuyeno) + '"')):

                        gka.popup(uyekaydetuyeno + ' No.lu üye zaten kaydedilmiş.\nÜye No. eşsiz olmalıdır.', keep_on_top=True , title='Hata')

                    else:

                        uyekaydetpenliste.append(uyekaydetpensatir)

                    uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

            elif uyekaydetuyeno and uyekaydetuyeadi and uyekaydetuyesinifi and '"' in uyekaydetuyeno or '"' in uyekaydetuyeadi or '"' in uyekaydetuyesinifi:

                gka.popup('Geçersiz karakter kullandınız.', keep_on_top=True , title='Hata')

            else:

                gka.popup('Boş alan kalamaz!', keep_on_top=True , title='Hata')

        if uyekaydetfiil == 'uyekaydetonay' and len(uyekaydetpenliste) > 0:
                
            olustur(uyeler, tuple(uyekaydetpenliste))

            uyekaydetpencere['uyekaydetdurum'].update(str(len(uyekaydetpenliste)) + ' kayıt işlendi.')

            uyekaydetpenliste = []

            uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

        elif uyekaydetfiil == 'uyekaydetonay':

            gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', keep_on_top=True , title='Hata')

        if uyekaydetfiil == 'uyekaydetexcel':

            uyekaydetpenliste = exceldenaktar(True, uyekaydetpenliste, 'uyeler', 3)

            uyekaydetpencere['kayitolusturliste'].update(values=uyekaydetpenliste)

        if uyekaydetfiil == 'uyekaydetliste':

            uyekaydetlistesecilen = uyekaydetdeger['uyekaydetliste'][0]

        if uyekaydetfiil == 'uyekaydetlistesil' and uyekaydetlistesecilen != -1 and gka.popup_yes_no(str(uyekaydetpenliste[uyekaydetlistesecilen][0]) + ' No.lu üye ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?', keep_on_top=True, title='Onay') == 'Yes':
        
            uyekaydetpenliste.pop(uyekaydetlistesecilen)

            uyekaydetpencere['uyekaydetliste'].update(values=uyekaydetpenliste)

            uyekaydetlistesecilen = -1

################################################################################################################################

### ÜYE SORGULA VEYA SİL

################################################################################################################################

uyesilduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='uyesiluyeno', s=(70,1))],
            [gka.Text('Üye Adı', s=(10,1)), gka.Input(key='uyesiladisoyadi', s=(70,1))],
            [gka.Text('Üye Sınıfı', s=(10,1)), gka.Input(key='uyesilsinifi', s=(70,1))],
            [gka.Table([], ['Üye No.', 'Üye Adı-Soyadı', 'Üye Sınıfı', 'Kütüphane'], num_rows=20, key='uyesilsorgu', def_col_width=16, auto_size_columns=False)],
            [gka.Button('Sorgula', key='uyesilsorguonay'), gka.Button('Tüm Kütüphanelerde Sorgula', key='uyesilistemcisorguonay'), gka.Button('Listedekileri Sil', key='uyesiltopluonay'), gka.Button("Excel'e Aktar", key='uyesilexcel'), gka.Text(key='uyesildurum')]]

uyesilpencere = gka.Window('Üye Sil', uyesilduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

uyesilpencere.Hide()

def uyesil(uyeler, yonetici):

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

            istemcisorgu = False

            uyesorgusonuc = sorgula(uyeler, kmt)

            uyesilpencere['uyesilsorgu'].update(values=uyesorgusonuc)

            uyesilpencere['uyesildurum'].update(str(len(uyesorgusonuc)) + ' kayıt listelendi.')

        if uyesilfiil == 'uyesilsorgu':

            multilinetemp = ''''''

            secilensatir = uyesorgusonuc[uyesildeger['uyesilsorgu'][0]]

            for i in range(7):

                baslikliste = ['Üye No.', '\nÜye Adı: ', '\nÜye Sınıfı: ']

                multilinetemp += (baslikliste[i] + secilensatir[i])

            uyesilpencere['uyesildetay'].update(multilinetemp)

        if uyesilfiil == 'uyesiltopluonay' and yonetici == 1 and len(uyesorgusonuc) > 0:

            if uyesilfiil == 'uyesiltopluonay' and istemcisorgu == False and gka.popup_yes_no(str(len(uyesorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?', keep_on_top=True, title='Onay') == 'Yes':

                for i in uyesorgusonuc:

                    sil(uyeler, ('uyeno="' + i[0] + '"'))

                uyesilpencere['uyesildurum'].update(str(len(uyesorgusonuc)) + ' adet kayit silindi.')

                uyesorgusonuc = sorgula(uyeler, kmt)

                uyesilpencere['uyesilsorgu'].update(values=uyesorgusonuc)

        elif uyesilfiil == 'uyesiltopluonay' and yonetici != 1:

            gka.popup('Yönetici yetkilerine sahip değilsiniz.', keep_on_top=True , title='Hata')

        if uyesilfiil == 'uyesiltopluonay' and istemcisorgu == True:

            gka.popup('Diğer istemcilerin kayıtları yalnızca okunabilir.', keep_on_top=True , title='Hata')

        if uyesilfiil == 'uyesilexcel':

            exceleaktar(uyesorgusonuc, sutunlar=['Üye No.', 'Üye Adı-Soyadı', 'Üye Sınıfı', 'Kütüphane'])

        if uyesilfiil == 'uyesilistemcisorguonay' and istemci == 1:

            uyesorgusonuc = []

            istemcisorgu = True

            for i in istemcilistesi:

                for a in sorgula((i[1] + 'uyeler'), kmt):

                    uyesiltempsatir = []

                    for b in a:

                        uyesiltempsatir.append(b)

                    uyesiltempsatir.append(i[0])
                    
                    uyesorgusonuc.append(uyesiltempsatir)

            uyesilpencere['uyesilsorgu'].update(values=uyesorgusonuc)

            uyesilpencere['uyesildurum'].update(str(len(uyesorgusonuc)) + ' kayıt listelendi.')

        if uyesilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            uyesilpencere.Hide()

            break

################################################################################################################################

### KULLANICI OLUŞTUR

################################################################################################################################

kullaniciduzen = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullaniciolusturadi')],
                  [gka.Text('Şifre', s=(10,1)), gka.Input(key='kullaniciolustursifre')],
                  [gka.Text('Yetkileri', s=(10,1)), gka.Combo(['Ziyaretçi', 'Görevli', 'Yönetici'], default_value='Görevli', s=(15,22), enable_events=True, readonly=True, key='kullaniciolusturyetki')],
                  [gka.Button('Ekle', key='kullaniciolusturekle')],
                  [gka.Table([], ['Kullanıcı Adı', 'Kullanıcı Şifresi', 'Kullanıcı Rütbesi'], num_rows=20, key='kullaniciolusturliste', def_col_width=30, auto_size_columns=True, enable_events=True)],
                  [gka.Button('Kaydet', key='kullaniciolusturonay'), gka.Button('Satırı Sil', key='kullaniciolusturlistesil'), gka.Text(key='kullaniciolusturdurum')]]

kullaniciolusturpencere = gka.Window('Kullanıcı Kaydet', kullaniciduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

kullaniciolusturpencere.Hide()

def kullaniciolustur(kullanicilar):

    kullaniciolusturpenliste = []

    kullaniciolusturlistesecilen = -1

    kullaniciolusturpencere.UnHide()

    while True:

        kullaniciolusturfiil, kullaniciolusturdeger = kullaniciolusturpencere.read()

        if kullaniciolusturfiil == 'kullaniciolusturekle':

            kullaniciolusturadi = str(kullaniciolusturdeger['kullaniciolusturadi'])

            kullaniciolustursifre = str(kullaniciolusturdeger['kullaniciolustursifre'])

            kullaniciolusturyetki = str(kullaniciolusturdeger['kullaniciolusturyetki'])

            if kullaniciolusturadi and kullaniciolustursifre and kullaniciolusturyetki:
                    
                if '"' not in kullaniciolusturadi and '"' not in kullaniciolustursifre:

                    kullaniciolusturpensatir = []

                    kullaniciolusturnoeslesme = 0

                    for i in [kullaniciolusturadi, kullaniciolustursifre, kullaniciolusturyetki]:

                        kullaniciolusturpensatir.append(i)

                    for i in range(0, len(kullaniciolusturpenliste)):

                        if kullaniciolusturpenliste[i][0] == kullaniciolusturadi:

                            kullaniciolusturnoeslesme += 1

                    if kullaniciolusturnoeslesme > 0 or mevcutmu(kullanicilar, ('kullaniciadi="' + str(kullaniciolusturadi) + '"')):

                        gka.popup(kullaniciolusturadi + ' adlı kullanıcı zaten oluşturulmuş.\nKullanıcı Adı eşsiz olmalıdır.', keep_on_top=True , title='Hata')

                    else:

                        kullaniciolusturpenliste.append(kullaniciolusturpensatir)

                    kullaniciolusturpencere['kullaniciolusturliste'].update(values=kullaniciolusturpenliste)

                elif '"' in kullaniciolusturadi or '"' in kullaniciolustursifre:

                    gka.popup('Geçersiz karakter kullandınız.', keep_on_top=True , title='Hata')

            else:

                gka.popup('Boş alan kalamaz!', keep_on_top=True , title='Hata')

        if kullaniciolusturfiil == 'kullaniciolusturonay' and len(kullaniciolusturpenliste) > 0:
                
            olustur(kullanicilar, tuple(kullaniciolusturpenliste))

            kullaniciolusturpencere['kullaniciolusturdurum'].update(str(len(kullaniciolusturpenliste)) + ' kayıt işlendi.')

            kullaniciolusturpenliste = []

            kullaniciolusturpencere['kullaniciolusturliste'].update(values=kullaniciolusturpenliste)

        elif kullaniciolusturfiil == 'kullaniciolusturonay':

            gka.popup('Kaydınız zaten işlendi veya kayıt yapmadınız.', keep_on_top=True , title='Hata')

        if kullaniciolusturfiil == 'kullaniciolusturliste':

            kullaniciolusturlistesecilen = kullaniciolusturdeger['kullaniciolusturliste'][0]

        if kullaniciolusturfiil == 'kullaniciolusturlistesil' and kullaniciolusturlistesecilen != -1 and gka.popup_yes_no(str(kullaniciolusturpenliste[kullaniciolusturlistesecilen][0]) + ' adlı kullanıcı ön kayıt tablosundan silinecek.\nOnaylıyor musunuz?', keep_on_top=True, title='Onay') == 'Yes':
            
            kullaniciolusturpenliste.pop(kullaniciolusturlistesecilen)

            kullaniciolusturpencere['kullaniciolusturliste'].update(values=kullaniciolusturpenliste)

            kullaniciolusturlistesecilen = -1
        
        if kullaniciolusturfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            kullaniciolusturpencere.Hide()

            break

################################################################################################################################

### KULLANICI SİL

################################################################################################################################

kullanicisilduzen = [[gka.Text('Kullanıcı Adı', s=(10,1)), gka.Input(key='kullanicisiladi')],
                     [gka.Text('Kullanıcı Şifre', s=(10,1)), gka.Input(key='kullanicisilsifre')],
                     [gka.Text('Kullanıcı Yetkileri', s=(10,1)), gka.Combo(['Görevli', 'Yönetici', 'Ziyaretçi'], default_value='Görevli', s=(15,22), enable_events=True, readonly=True, k='kullanicisilyetki')],
                     [gka.Table([], ['Kullanıcı Adı', 'Kullanıcı Şifresi', 'Kullanıcı Yetkileri'], num_rows=20, key='kullanicisilliste', def_col_width=30, auto_size_columns=True)],
                     [gka.Button('Sorgula', key='kullanicisilsorguonay'), gka.Button('Listedekileri Sil', key='kullanicisiltopluonay'), gka.Text(key='kullanicisildurum')]]

kullanicisilpencere = gka.Window('Kullanıcı Sil', kullanicisilduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

kullanicisilpencere.Hide()

def kullanicisil(kullanicilar):

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

        if kullanicisilfiil == 'kullanicisiltopluonay' and len(kullanicisorgusonuc) > 0:

            if kullanicisilfiil == 'kullanicisiltopluonay' and gka.popup_yes_no(str(len(kullanicisorgusonuc)) + ' kayıt silinecek.\nEmin misiniz?', keep_on_top=True, title='Onay') == 'Yes':

                for i in kullanicisorgusonuc:

                    sil(kullanicilar, ('kullaniciadi="' + i[0] + '"'))

                if len(sorgula(kullanicilar, '1=1')) == 0:

                    mysqlsorgucalistir('INSERT INTO ' + kullanicilar + ' VALUES ("DEVKÜTÜP", "12345", "Yönetici");')

                    gka.popup('Kullanıcıların tamamını sildiniz.\nProgramın kilitlenmesini önlemek için varsayılan kullanıcı,\nKullanıcı Adı: DEVKÜTÜP\nŞifre: 12345\nYetkiler: Yönetici\noluşturuldu.', keep_on_top=True , title='Uyarı')

                kullanicisilpencere['kullanicisildurum'].update(str(len(kullanicisorgusonuc)) + ' adet kayıt silindi.')

                kullanicisorgusonuc = sorgula(kullanicilar, kmt)

                kullanicisilpencere['kullanicisilliste'].update(values=kullanicisorgusonuc)

        if kullanicisilfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            kullanicisilpencere.Hide()

            break


################################################################################################################################

### EMANET AL (TESLİM AL)

################################################################################################################################

emanetalduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='emanetaluyeno', s=(36,1)), gka.Text('Üye Sınıfı.', s=(10,1)), gka.Input(key='emanetaluyesinifi', s=(36,1)), gka.Text('Üye Adı', s=(10,1)), gka.Input(key='emanetaluyeadi', s=(36,1))],
                 [gka.Text('Kayıt No.', s=(10,1)), gka.Input(key='emanetalbarkod', s=(36,1)), gka.Text('Adı', s=(10,1)), gka.Input(key='emanetaladi', s=(36,1)), gka.Text('Yazarı', s=(10,1)), gka.Input(key='emanetalkaynagi', s=(36,1))],
                 [gka.Text('Yayımcı', s=(10,1)), gka.Input(key='emanetalyayimci', s=(36,1)), gka.Text('Türü', s=(10,1)), gka.Input(key='emanetalturu', s=(36,1)), gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='emanetaldolapkodu', s=(36,1))],
                 [gka.Table([], ['Üye No.', 'Üye Adı', 'Üye Sınıfı.', 'Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu'], num_rows=20, key='emanetalsorgu', def_col_width=13, auto_size_columns=False, enable_events=True)],
                 [gka.Button('Sorgula', key='emanetalsorguonay'), gka.Button('Seçilen Kaydı Teslim Al', key='emanetalonay'), gka.Button("Excel'e Aktar", key='emanetalexcel'), gka.Text(key='emanetaldurum')]]

emanetalpencere = gka.Window('Teslim Al', emanetalduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

emanetalpencere.Hide()

def emanetal(emanet):

    emanetalsorgusonuc = []

    emanetalpencere.UnHide()

    while True:

        emanetalfiil, emanetaldeger = emanetalpencere.read()

        kmt = ''

        emanetaluyesinifi = str(emanetaldeger['emanetaluyesinifi'])

        emanetaluyeno = str(emanetaldeger['emanetaluyeno'])

        emanetaluyeadi = str(emanetaldeger['emanetaluyeadi'])

        emanetalbarkod = str(emanetaldeger['emanetalbarkod'])

        emanetaladi = str(emanetaldeger['emanetaladi'])

        emanetalkaynagi = str(emanetaldeger['emanetalkaynagi'])

        emanetalyayimci = str(emanetaldeger['emanetalyayimci'])

        emanetalturu = str(emanetaldeger['emanetalturu'])

        emanetaldolapkodu = str(emanetaldeger['emanetaldolapkodu'])

        if emanetaluyeno:

            kmt += 'uyeno LIKE "%' + emanetalbarkod + '%" '

        else:

            kmt += '1=1 '

        if emanetaluyeadi:

            kmt += ' AND uyeadi LIKE "%' + emanetaluyeadi + '%" '

        if emanetaluyesinifi:

            kmt += ' AND uyesinifi LIKE "%' + emanetaluyesinifi + '%" '

        if emanetalbarkod:

            kmt += ' AND kayitno LIKE "%' + emanetalbarkod + '%" '

        if emanetaladi:

            kmt += ' AND kayitadi LIKE "%' + emanetaladi + '%" '

        if emanetalkaynagi:

            kmt += ' AND kayitkaynagi LIKE "%' + emanetalkaynagi + '%" '

        if emanetalyayimci:

            kmt += ' AND yayimci LIKE "%' + emanetalyayimci + '%" '

        if emanetalturu:

            kmt += ' AND kayitturu LIKE "%' + emanetalturu + '%" '

        if emanetaldolapkodu:

            kmt += ' AND rafkodu LIKE "%' + emanetaldolapkodu + '%" '

        if emanetalfiil == 'emanetalsorguonay':

            emanetalsorgusonuc = sorgula(emanet, kmt)

            emanetalpencere['emanetalsorgu'].update(values=emanetalsorgusonuc)

            emanetalpencere['emanetaldurum'].update(str(len(emanetalsorgusonuc)) + ' kayıt listelendi.')

        if emanetalfiil == 'emanetalsorgu':

            secilensatir = emanetalsorgusonuc[emanetaldeger['emanetalsorgu'][0]]

        if emanetalfiil == 'emanetalonay' and secilensatir and gka.popup_yes_no('Üye No. ' + secilensatir[0] + '\nÜye Adı: ' + secilensatir[1] + 'Yukarıda bilgileri verilen üyeden\n' + secilensatir[3] + ' No.lu\n' + secilensatir[4] + ' adlı kayıt teslim alınacaktır.\nOnaylıyor musunuz?', keep_on_top=True, title='Onay') == 'Yes':

            sil(emanet, ('kayitno="' + secilensatir[3] + '"'))

            emanetalsorgusonuc = sorgula(emanet, kmt)

            emanetalpencere['emanetalsorgu'].update(values=emanetalsorgusonuc)

            emanetalpencere['emanetaldurum'].update(str(len(emanetalsorgusonuc)) + ' kayıt listelendi.')

        elif emanetalfiil == 'emanetalonay':

            gka.popup('Lütfen listeden kayıt seçin.', keep_on_top=True , title='Hata')

        if emanetalfiil == 'emanetalexcel':

            exceleaktar(emanetalsorgusonuc, sutunlar=['Üye No.', 'Üye Adı', 'Üye Sınıfı.', 'Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu'])

        if emanetalfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            emanetalpencere.Hide()

            break

################################################################################################################################

### EMANET VER

################################################################################################################################

emanetverduzen = [[gka.Text('Üye No.', s=(10,1)), gka.Input(key='emanetveruyeno', s=(24,1)), gka.Text('Üye Sınıfı.', s=(10,1)), gka.Input(key='emanetveruyesinifi', s=(24,1)), gka.Text('Üye Adı', s=(10,1)), gka.Input(key='emanetveruyeadi', s=(24,1))],
                  [gka.Table([], ['Üye No.', 'Üye Adı', 'Üye Sınıfı'], num_rows=12, key='emanetveruyesorgu', def_col_width=30, auto_size_columns=False, enable_events=True)],
                  [gka.Button('Sorgula', key='emanetveruyesorguonay'),  gka.Button('Üye Seç', key='emanetveruyesec'), gka.Text(key='emanetveruyedurum')],
                  [gka.Text('Kayıt No.', s=(10,1)), gka.Input(key='emanetverbarkod', s=(24,1)), gka.Text('Adı', s=(10,1)), gka.Input(key='emanetveradi', s=(24,1)), gka.Text('Yazarı', s=(10,1)), gka.Input(key='emanetverkaynagi', s=(24,1))],
                  [gka.Text('Yayımcı', s=(10,1)), gka.Input(key='emanetveryayimci', s=(24,1)), gka.Text('Türü', s=(10,1)), gka.Input(key='emanetverturu', s=(24,1)), gka.Text('Raf Kodu', s=(10,1)), gka.Input(key='emanetverdolapkodu', s=(24,1))],
                  [gka.Table([], ['Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu'], num_rows=12, key='emanetverkayitsorgu', def_col_width=15, auto_size_columns=False, enable_events=True)],
                  [gka.Button('Sorgula', key='emanetverkayitsorguonay'), gka.Button('Kayıt Seç', key='emanetverkayitsec'), gka.Text('Gün Sayısı', s=(10,1)), gka.Input(key='emanetvergunsayisi', s=(5,1)), gka.Button('ONAYLA', key='emanetveronay'), gka.Text(key='emanetverkayitdurum')]]

emanetverpencere = gka.Window('Emanet Ver', emanetverduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

emanetverpencere.Hide()

def emanetver(kayitlar, uyeler, emanet):

    emanetverpencere.UnHide()

    while True:

        emanetverfiil, emanetverdeger = emanetverpencere.read()

        if emanetverfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            emanetverpencere.Hide()

            break

        kmt = ''

        kmt0 = ''

        emanetveruyesinifi = str(emanetverdeger['emanetveruyesinifi'])

        emanetveruyeno = str(emanetverdeger['emanetveruyeno'])

        emanetveruyeadi = str(emanetverdeger['emanetveruyeadi'])

        emanetverbarkod = str(emanetverdeger['emanetverbarkod'])

        emanetveradi = str(emanetverdeger['emanetveradi'])

        emanetverkaynagi = str(emanetverdeger['emanetverkaynagi'])

        emanetveryayimci = str(emanetverdeger['emanetveryayimci'])

        emanetverturu = str(emanetverdeger['emanetverturu'])

        emanetverdolapkodu = str(emanetverdeger['emanetverdolapkodu'])

        emanetvergunsayisi = str(emanetverdeger['emanetvergunsayisi'])

        if emanetveruyeno:

            kmt += 'uyeno LIKE "%' + emanetveruyeno + '%" '

        else:

            kmt += '1=1 '

        if emanetveruyeadi:

            kmt += ' AND uyeadi LIKE "%' + emanetveruyeadi + '%" '

        if emanetveruyesinifi:

            kmt += ' AND uyesinifi LIKE "%' + emanetveruyesinifi + '%" '

        if emanetverbarkod:

            kmt0 += 'kayitno LIKE "%' + emanetverbarkod + '%" '

        else:

            kmt0 += '1=1 '

        if emanetveradi:

            kmt0 += ' AND kayitadi LIKE "%' + emanetveradi + '%" '

        if emanetverkaynagi:

            kmt0 += ' AND kayitkaynagi LIKE "%' + emanetverkaynagi + '%" '

        if emanetveryayimci:

            kmt0 += ' AND yayimci LIKE "%' + emanetveryayimci + '%" '

        if emanetverturu:

            kmt0 += ' AND kayitturu LIKE "%' + emanetverturu + '%" '

        if emanetverdolapkodu:

            kmt0 += ' AND rafkodu LIKE "%' + emanetverdolapkodu + '%" '

        if emanetverfiil == 'emanetverkayitsorguonay':

            emanetverkayitsorgusonuc = sorgula(kayitlar, kmt0)

            emanetverpencere['emanetverkayitsorgu'].update(values=emanetverkayitsorgusonuc)

        if emanetverfiil == 'emanetverkayitsorgu':

            emanetverkayitsecilensatir = emanetverkayitsorgusonuc[emanetverdeger['emanetverkayitsorgu'][0]]

            emanetverpencere['emanetverkayitdurum'].update(emanetverkayitsecilensatir[0] + ' ' + emanetverkayitsecilensatir[1])

        if emanetverfiil == 'emanetverkayitsec' and emanetverkayitsecilensatir:

            kayitbilgileri = emanetverkayitsecilensatir

            emanetverpencere['emanetverkayitdurum'].update(emanetverkayitsecilensatir[0] + ' ' + emanetverkayitsecilensatir[1] + ' SEÇİLDİ')

        elif emanetverfiil == 'emanetverkayitsec':

            gka.popup('Olmayan girdi seçilemez.', keep_on_top=True , title='Hata')

        if emanetverfiil == 'emanetveruyesorguonay':

            emanetveruyesorgusonuc = sorgula(uyeler, kmt)

            emanetverpencere['emanetveruyesorgu'].update(values=emanetveruyesorgusonuc)

        if emanetverfiil == 'emanetveruyesorgu':

            emanetveruyesecilensatir = emanetveruyesorgusonuc[emanetverdeger['emanetveruyesorgu'][0]]

            emanetverpencere['emanetveruyedurum'].update(emanetveruyesecilensatir[0] + ' ' + emanetveruyesecilensatir[1])

        if emanetverfiil == 'emanetveruyesec' and emanetveruyesecilensatir:

            uyebilgileri = emanetveruyesecilensatir

            emanetverpencere['emanetveruyedurum'].update(emanetveruyesecilensatir[0] + ' ' + emanetveruyesecilensatir[1] + ' SEÇİLDİ')

        elif emanetverfiil == 'emanetveruyesec':

            gka.popup('Olmayan girdi seçilemez.', keep_on_top=True , title='Hata')

        if emanetverfiil == 'emanetveronay' and kayitbilgileri and uyebilgileri and emanetvergunsayisi and mevcutmu(emanet, 'kayitno="' + emanetverbarkod + '"') != True and gka.popup_yes_no(kayitbilgileri[1] + ' adlı kayıt,\n' + uyebilgileri[1] + ' adlı üyeye\nverilecektir.\nOnaylıyor musunuz?', keep_on_top=True , title='Bilgi') == 'Yes':

            templiste1 = []

            for i in uyebilgileri:

                templiste1.append(i)

            for i in range(6):
            
                templiste1.append(kayitbilgileri[i])

            templiste1.append(str(int(time.time())))

            templiste1.append(str(emanetvergunsayisi))

            olustur(emanet, [templiste1])

            gka.popup("İşlem başarılı.", keep_on_top=True , title='Bilgi')

        elif emanetverfiil == 'emanetveronay':

            gka.popup('Lütfen gerekliliklerin sağlandığından emin olun.', keep_on_top=True , title='Hata')

################################################################################################################################

### EMANET LİSTESİ

################################################################################################################################

emanetlisteduzen = [[gka.Table([], ['Üye No.', 'Üye Adı', 'Üye Sınıfı.', 'Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu', 'Verildiği Zaman', 'Teslim Alınacak', 'Kalan Gün'], num_rows=20, key='emanetlistesorgu', def_col_width=13, auto_size_columns=False, enable_events=True)],
                    [gka.Button('Güncelle', key='emanetlisteguncelle'), gka.Button("Excel'e Aktar", key='emanetlisteexcel'), gka.Text(key='emanetlistedurum')]]

emanetlistepencere = gka.Window('Emanet Listesi', emanetlisteduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

emanetlistepencere.Hide()

def emanetlistesi(emanet):

    def emanetlisteguncelle(emanet=emanet):

        listetemp = sorgula(emanet, '1=1')

        guncelliste = []

        for i in range(0, len(listetemp)):

            guncellistesatir = []

            for a in range(9):

                guncellistesatir.append(listetemp[i][a])

            listetempzaman = int(listetemp[i][9])

            listetempgun = int(listetemp[i][10])

            listetempverildigizaman = str(datetime.fromtimestamp(listetempzaman))

            guncellistesatir.append(listetempverildigizaman)

            guncellistesatir.append(str(datetime.fromtimestamp(listetempzaman + (listetempgun * 24 * 3600))))

            guncellistesatir.append(str(int(((listetempzaman + (listetempgun * 24 * 3600)) - time.time()) / (24 * 3600))))

            guncelliste.append(guncellistesatir)

        return guncelliste

    emanetlistepencere['emanetlistesorgu'].update(values=emanetlisteguncelle())

    emanetlistepencere['emanetlistedurum'].update(str(len(emanetlisteguncelle())) + ' kayıt listelendi.')

    emanetlistepencere.UnHide()

    while True:

        emanetlistefiil, emanetlistedeger = emanetlistepencere.read()

        if emanetlistefiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            emanetlistepencere.Hide()

            break

        if emanetlistefiil == 'emanetlisteguncelle':

            emanetlistepencere['emanetlistesorgu'].update(values=emanetlisteguncelle())

            emanetlistepencere['emanetlistedurum'].update(str(len(emanetlisteguncelle())) + ' kayıt listelendi.')

        if emanetlistefiil == 'emanetlisteexcel':

            exceleaktar(aktarilacaktablo=emanetlisteguncelle(), sutunlar=['Üye No.', 'Üye Adı', 'Üye Sınıfı.', 'Kayıt No.', 'Adı', 'Yazarı', 'Yayımcı', 'Türü', 'Raf Kodu', 'Verildiği Zaman', 'Teslim Alınacak', 'Kalan Gün'])

################################################################################################################################

### SAYAÇLAR

################################################################################################################################

sayaclarduzen = [[gka.Multiline(s=(30,4), key='sayaclar')]]

sayaclarpencere = gka.Window('Sayaçlar', sayaclarduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

sayaclarpencere.Hide()

def sayaclar(kayitlar, uyeler, kullanicilar, emanet):

    sayaclarmline = ""

    sayaclarmline += ('Kayıtlar: ' + str(len(sorgula(kayitlar, '1=1'))))

    sayaclarmline += ('\nÜyeler: ' + str(len(sorgula(uyeler, '1=1'))))

    sayaclarmline += ('\nKullanıcılar: ' + str(len(sorgula(kullanicilar, '1=1'))))

    sayaclarmline += ('\nEmanet: ' + str(len(sorgula(emanet, '1=1'))))

    sayaclarpencere.UnHide()

    sayaclarpencere['sayaclar'].update(sayaclarmline)

    while True:

        sayaclarfiil, sayaclardeger = sayaclarpencere.read()

        if sayaclarfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            sayaclarpencere.Hide()

            break

################################################################################################################################

### EXCEL'DEN AKTAR

################################################################################################################################

kayitexcelduzen = [[gka.Text("Excel'den Aktar")],
                   [gka.Input(key='kayitexcelgirdi'), gka.FileBrowse("Dosya Aç", file_types=(('Excel Dökümanı', '.xlsx'),)), gka.Button('İçe Aktar', key='kayitexceleaktaronay')]]

kayitexcelpencere = gka.Window("Excel'den Aktar", kayitexcelduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

kayitexcelpencere.Hide()

def exceldenaktar(eslesmekontrol, etkilesilenpenceretablo=None, tablo=None, birimsayisi=None):
    
    kayitexcelpencere.UnHide()

    while True:

        kayitexcelfiil, kayitexceldeger = kayitexcelpencere.read()

        if kayitexcelfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            kayitexcelpencere.Hide()

            break

        kayitexcelgirdi = kayitexceldeger['kayitexcelgirdi']

        if kayitexcelfiil == 'kayitexceleaktaronay' and kayitexcelgirdi:

            kayitexcelliste = []

            exceldosya = pd.read_excel(kayitexcelgirdi, engine='openpyxl')

            exceldosya.to_csv('temp.csv', index = None, header=True)

            data = csvac('temp.csv')

            os.remove('temp.csv')

            if eslesmekontrol == True:

                for satir in data:

                    if len(satir) != birimsayisi:

                        gka.popup('Açtığınız excel dosyasında boşluklar var. Lütfen boşluk bırakmayınız!', keep_on_top=True , title='Hata')

                        break

                    kayitexceleslesme = 0

                    for i in etkilesilenpenceretablo:

                        if i[0] == satir[0]:

                            kayitexceleslesme += 1

                    if kayitexceleslesme > 0 or mevcutmu(tablo, ('kayitno="' + str(satir[0]) + '"')):

                        gka.popup(satir[0] + ' No.lu kayit zaten oluşturulmuş.\nKayıt No. eşsiz olmalıdır.', keep_on_top=True , title='Hata')

                        break

                    else:

                        kayitexcelliste.append(satir)

                kayitexcelpencere.Hide()

                return kayitexcelliste
            
            else:

                kayitexcelpencere.Hide()

                return data
            
################################################################################################################################

### EXCEL'E AKTAR

################################################################################################################################

disaexcelduzen = [[gka.Text("Excel'e Aktar")],
                  [gka.Input(key='disaexcelgirdi'), gka.FileSaveAs("Kayıt Yeri Belirle", file_types=(('Excel Dökümanı', '.xlsx'),)), gka.Button('Dışa Aktar', key='disaexceleaktaronay')]]

disaexcelpencere = gka.Window("Excel'e Aktar", disaexcelduzen, enable_close_attempted_event=True, finalize=True, keep_on_top=True)

disaexcelpencere.Hide()

def exceleaktar(aktarilacaktablo, sutunlar=None):
    
    disaexcelpencere.UnHide()

    while True:

        disaexcelfiil, disaexceldeger = disaexcelpencere.read()

        if disaexcelfiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            disaexcelpencere.Hide()

            break

        disaexcelgirdi = disaexceldeger['disaexcelgirdi']

        if disaexcelfiil == 'disaexceleaktaronay' and disaexcelgirdi:

            df = pd.DataFrame(aktarilacaktablo, columns=sutunlar)

            df.to_excel(disaexcelgirdi)

            gka.popup('Dosya ' + disaexcelgirdi + ' olarak kaydedildi.', keep_on_top=True , title='Bilgi')

            disaexcelpencere.Hide()

            break

################################################################################################################################

## İSTEMCİ EKRANI

################################################################################################################################

if istemci == 1:

    istemciduzen = [[gka.Text('Lütfen istemci seçiniz.')]]

    for i in istemcilistesi:

        istemciduzen.append([gka.Button(i[0], key=i[1], s=(40,1), font=(8))])

    istemcipencere = gka.Window('DEVKÜTÜP ' + surum + ' İstemci Formu', istemciduzen, enable_close_attempted_event=True, finalize=True)

    while True:

        istemcipencerefiil, istemcipenceredeger = istemcipencere.read()

        for i in istemcilistesi:

            istemciolustur(i[1])

            if istemcipencerefiil == i[1]:

                istemcipencere.Hide()

                girisyap(i[1] + 'kayitlar', i[1] + 'kullanicilar', i[1] + 'uyeler', i[1] + 'emanet')

                istemcipencere.UnHide()

        if istemcipencerefiil == gka.WINDOW_CLOSE_ATTEMPTED_EVENT:

            if kapatmatercih == 1:

                gka.popup('Program, yöneticiniz tarafından kapatılamayacak şekilde ayarlandı.', keep_on_top=True , title='Hata')

            if kapatmatercih == 0:

                sys.exit()

else:

    istemciolustur('')

    istemcilistesi = [['', '']]

    girisyap('kayitlar', 'kullanicilar', 'uyeler', 'emanet')

    sys.exit()
