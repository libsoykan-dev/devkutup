# DEVKÜTÜP
Kütüphane otomasyon programı. Resmî ve şahsî kütüphaneler için tasarlanmıştır.

- [Çoklu İstemci Ekranı](https://github.com/libsoykan-dev/devkutup#%C3%A7oklu-i%CC%87stemci-ekran%C4%B1-v200_20230406-ve-%C3%BCst%C3%BC)
- [Giriş Ekranı](https://github.com/libsoykan-dev/devkutup#giri%C5%9F-ekran%C4%B1)
- [Ana Ekran](https://github.com/libsoykan-dev/devkutup#ana-ekran)
- [Kayıt İşlemleri (Kaydetme)](https://github.com/libsoykan-dev/devkutup#kaydetme)
- [Kayıt İşlemleri (Silme)](https://github.com/libsoykan-dev/devkutup#kay%C4%B1t-silme)
- [Kullanıcılar](https://github.com/libsoykan-dev/devkutup#kullan%C4%B1c%C4%B1lar)
- [Yapılandırma](https://github.com/libsoykan-dev/devkutup#yap%C4%B1land%C4%B1rma-dosyas%C4%B1-devkutupconf)
- [Lisans](https://github.com/libsoykan-dev/devkutup#lisans)
- [Raporlar](https://github.com/libsoykan-dev/devkutup#raporlar)

# Çoklu İstemci Ekranı (v2.00_20230406 ve üstü)
![resim](https://user-images.githubusercontent.com/103260281/230802018-0adb57da-b739-4e53-b2ae-30af3e693edb.png)

Programın çoklu istemci özelliği sayesinde birden fazla kurum tek bir sunucuya bağlanarak farklı istemcilerdeki kayıtları ve üyeleri hangi kurumda kayıtlı olduğuyla birlikte görüntüleyebilir. Yani "BİR İDAM MAHKUMUNUN SON GÜNÜ" adlı kitap herhangi bir istemciden sorgulandığında kitabın detayları listelenir. Aynı durum üye sorgusu için de geçerlidir.

Programa istediğiniz kadar istemciyi ana klasörde "istemciler.csv" dosyasına "A Kütüphanesi, akutuphanesikodu" gibi satırlar ekleyerek güncelleyebilirsiniz. Bu özellik devkutup.conf dosyasına eklenecek "istemci = 1" ile aktif edilebilir. Eğer aktif edilmezse bu ekran program tarafından otomatik olarak atlanır ve giriş ekranına geçiş yapılır.

# Giriş Ekranı
![resim](https://user-images.githubusercontent.com/103260281/230802110-cbd6572a-f268-4b18-8164-f5fbe510f194.png)

Kullanıcı adı ve şifre girilerek giriş yapılan ekrandır. Varsayılan hesap için kullanıcı adı "DEVKÜTÜP", şifre "12345" olup bu hesap yönetici yetkilerine sahiptir.

# Ana Ekran
![resim](https://github.com/libsoykan-dev/devkutup/assets/103260281/37692ff7-5d37-4b6c-9387-6376445b234e)

Ana ekranda kayıt, üye, kullanıcı, emanet ve rapor işlemleri yer almaktadır.
# Kaydetme
![resim](https://github.com/libsoykan-dev/devkutup/assets/103260281/d51b7ea0-a11d-4e79-9be1-fc1a43510b36)

Kayıt sekmelerinde kaydedilecek değerler girilerek "Ekle"ye tıklanır. Toplu kayıt için excel dosyalarını içe aktarabilirsiniz. Kaydetmeye karar verdiğinizde "Kaydet" butonuna tıklarsınız. Hatalı bir giriş yapıp "Ekle"ye tıkladığınızda hatalı satırı seçip "Satırı Sil" tıklayabilirsiniz. Ek niteliklere 32768 harfi geçmeyecek şekilde istediğiniz bilgiyi girebilirsiniz.
# Kayıt Silme
![resim](https://github.com/libsoykan-dev/devkutup/assets/103260281/59ac0fad-b563-479d-a7e1-91777b4b06ef)

Silme işlemleri için de silmek istediğiniz değer(ler)i forma girip "Sorgula"ya bastığınızda tablodaki veriler işlenir. "Listedekileri Sil" butonu tabloda bulunan ve yalnızca bulunduğunuz kurumun veri tabanına ait değerleri siler. Aynı durum üye silme işlemleri için de geçerlidir. Bu işlem geri alınamaz. Ayrıca diğer istemcilerle irtibatı sağlamak ve üyeleri kaydın bulunduğu kütüphaneye yönlendirmek için "tüm Kütüphanelerde Sorgula" butonu eklenmiştir.
# Teslim Al
![resim](https://github.com/libsoykan-dev/devkutup/assets/103260281/51c86c0f-f70c-409f-afc4-5dbec29b1332)

Bu ekranda görülen boşluklarda filtreleme yapabilirsiniz. Arama yapıp listeden kayıt seçtikten sonra "Seçilen Kaydı Teslim Al" butonuna tıklamanız yeterli.
# Emanet Ver
![resim](https://github.com/libsoykan-dev/devkutup/assets/103260281/1f7810d3-aa44-4bea-af6e-65cefbf20b7e)

Bu ekranda 2 arama tablosundan ilkinde üye bilgileri ikincisinde kitap bilgileri her tablonun seçme butonuyla seçilir. Daha sonra gün sayısı yazan boşluğa gün sayısı girilir ve "ONAYLA" tıklanır.
# Kullanıcılar
![resim](https://user-images.githubusercontent.com/103260281/230803897-44970121-fa8c-4950-b5e4-b9b7e0d16dbd.png)

MYSQL veri tabanında "<istemci adı>kullanicilar" olarak barındırılan veri tabanında kullaniciadi, sifre ve yetki olmak üzere 3 adet sütün kayıtlıdır. Bu sütünlardan ilk ikisi kullanıcı adı ve şifreyi barındırırken sonuncusu yani yetki sütunu kullanıcının yetkisini belirler. yetki sütununa "Yönetici, Görevli, Ziyaretçi" olmak üzere toplamda 3 adet yetki girişi yapılabilir.

Yönetici tüm ekranlara erişebilirken Görevli sadece Emanet Alma ve Verme, Kaydetme ve Sorgulama gibi temel ekranlara erişebilir. Ziyaretçiler yalnızca kayıt sorgulayabilir. Bu yetki düzeylerinin erişim izinleri if koşullarındaki "yonetici" değişkeni Görevli, Yönetici ve Ziyaretçi için sırasıyla 0, 1 veya 2 şeklinde ayarlanarak değiştirilebilir. Varsayılan Kullanıcı Adı "DEVKÜTÜP", şifre ise "12345"tir. Eğer tüm kullanıcıları silerseniz program kilitlenmemek için varsayılan kullanıcıyı tekrar oluşturur.

# Raporlama

Emanet listesi ve sayaçlar mevcuttur. Temel ögelerin sayılması ve emanet verilen kayıtların düzenlenmesi için kullanılır.

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
