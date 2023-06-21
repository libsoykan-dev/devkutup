# DEVKÜTÜP
Kütüphane otomasyon programı. Resmî ve şahsî kütüphaneler için tasarlanmıştır.

# Çoklu İstemci Ekranı (v2.00_20230406 ve üstü)
![resim](https://user-images.githubusercontent.com/103260281/230802018-0adb57da-b739-4e53-b2ae-30af3e693edb.png)

Programın çoklu istemci özelliği sayesinde birden fazla kurum tek bir sunucuya bağlanarak farklı istemcilerdeki kitapları ve üyeleri hangi kurumda kayıtlı olduğuyla birlikte görüntüleyebilir. Yani "BİR İDAM MAHKUMUNUN SON GÜNÜ" adlı kitap herhangi bir istemciden sorgulandığında kitabın bulunduğu kurum ile birlikte kitabın detayları listelenir. Aynı durum üye sorgusu için de geçerlidir.



Programa istediğiniz kadar istemciyi ana klasörde "istemciler.csv" dosyasına "A Kütüphanesi, akutuphanesikodu" gibi satırlar ekleyerek güncelleyebilirsiniz. Bu özellik devkutup.conf dosyasına eklenecek "istemci = 1" ile aktif edilebilir. Eğer aktif edilmezse bu ekran program tarafından otomatik olarak atlanır ve giriş ekranına geçiş yapılır.

# Giriş Ekranı
![resim](https://user-images.githubusercontent.com/103260281/230802110-cbd6572a-f268-4b18-8164-f5fbe510f194.png)

Kullanıcı adı ve şifre girilerek giriş yapılan ekrandır. Varsayılan hesap için kullanıcı adı "DEVKÜTÜP", şifre "12345" olup bu hesap yönetici yetkilerine sahiptir.

# Ana Ekran
![resim](https://user-images.githubusercontent.com/103260281/229325788-5b2a6437-eb10-440c-ac2d-a81946804e52.png)

Ana ekranda kitap, üye, ve kullanıcı işlemleri; kitap teslim edeceklerin veya etmeyenlerin listesi ile bu listeyi dışa aktarmaya yarayan form yer almaktadır.
# Kaydetme
![resim](https://user-images.githubusercontent.com/103260281/229325489-e24d4774-50e1-464b-8209-23abc80f1097.png)

Kayıt sekmelerinde kaydedilecek değerler girilerek "Ekle"ye tıklanır. Toplu kayıt için excel dosyalarını içe aktarabilirsiniz. Kaydetmeye karar verdiğinizde "Kaydet" butonuna tıklarsınız. Hatalı bir giriş yapıp "Ekle"ye tıkladığınızda hatalı satırı seçip "Satırı Sil" tıklayabilirsiniz.
# Kayıt Silme
![resim](https://user-images.githubusercontent.com/103260281/230803840-3929de9a-2b00-4c14-900c-a682c851a488.png)

Silme işlemleri için de silmek istediğiniz değer(ler)i forma girip "Sorgula"ya bastığınızda tablodaki veriler işlenir. "Listedekileri Sil" butonu tabloda bulunan ve yalnızca bulunduğunuz kurumun veri tabanına ait değerleri siler. Aynı durum üye silme işlemleri için de geçerlidir. Bu işlem geri alınamaz.
# Kullanıcılar
![resim](https://user-images.githubusercontent.com/103260281/230803897-44970121-fa8c-4950-b5e4-b9b7e0d16dbd.png)

MYSQL veri tabanında "<istemci adı>kullanicilar" olarak barındırılan veri tabanında kullaniciadi, sifre ve yetki olmak üzere 3 adet sütün kayıtlıdır. Bu sütünlardan ilk ikisi kullanıcı adı ve şifreyi barındırırken sonuncusu yani yetki sütunu kullanıcının yetkisini belirler. yetki sütununa "Yönetici, Görevli, Ziyaretçi" olmak üzere toplamda 3 adet yetki girişi yapılabilir.

![resim](https://user-images.githubusercontent.com/103260281/230802846-cf0d39ae-4f33-4df1-a56d-7e0993826908.png)

Yukarıdaki tabloda hesapların erişim düzeyleri verilmiştir. Yönetici tüm ekranlara erişebilirken Görevli sadece Kitap Alma ve Verme, Kaydetme ve Sorgulama gibi temel ekranlara erişebilir. Ziyaretçiler yalnızca kitap sorgulayabilir. Bu yetki düzeylerinin erişim izinleri if koşullarındaki "yonetici" değişkeni Görevli, Yönetici ve Ziyaretçi için sırasıyla 0, 1 veya 2 şeklinde ayarlanarak değiştirilebilir. Varsayılan Kullanıcı Adı "DEVKÜTÜP", şifre ise "12345"tir. Eğer tüm kullanıcıları silerseniz program kilitlenmemek için varsayılan kullanıcıyı tekrar oluşturur.

# Yapılandırma Dosyası (devkutup.conf)
Bu dosya 2 bölüm içerir: mysql-giris ve diger



>[mysql-giris]

Bu bölümde MYSQL itimatnamesi ve sunucu giriş bilgileri yer alır

>ip = localhost

MYSQL sunucusunun ip adresi burada tanımlanır

>kullaniciadi = root

MYSQL sunucusuna giriş için kullanıcı adınızdır

>sifre =

MYSQL sunucusna giriş için şifrenizdir

>port = 3311

MYSQL sunucusunun portu burada tanımlanır

>[diger]

Bu bölümde ise programın diğer ayarları atanır

>tema = Black

Program teması (alabileceği değerler için PySimpleGUI dökümantasyonuna bakınız)

>kapatmatercih = 1

Programın kapanmasını engelleyen özelliktir. Bu sayede eğer kütüphanenizdeki bilgisayarın sadece programla kullanılmasını istiyorsanız Windows'ta grup ilkesi belirleyerek varsayılan arayüz programını DEVKÜTÜP'e atayabilirsiniz.
Linux tabanlı sistemlerde ise masaüstü yöneticisinden sonra otomatik çalışmasını istediğiniz programı systemd gibi bir yönetimle DEVKÜTÜP olarak atayabilirsiniz.

>istemci = 1

İstemci özelliğinin açık olup olmayacağıdır

Neticede varsayılan olarak

>[mysql-giris]<br />
>ip = localhost<br />
>kullaniciadi = root<br />
>sifre =<br />
>port = 3311<br />
>[diger]<br />
>tema = Black<br />
>kapatmatercih = 1<br />
>istemci = 1<br />

ayarları geçerlidir. Eğer yapılandırma dosyanız mevcut değilse bu ayarlarla program başlatılır.

# Lisans
Bu program Creative Commons Atıf Gayri-Ticari 4.0 Uluslararası Kamu Lisansı ile lisanslanmıştır.
Atıfta bulunurken 'libsoykan-dev' veya 'Naim Salih SOYKAN' olarak belirtebilirsiniz.
