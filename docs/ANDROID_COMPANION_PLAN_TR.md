# Android Yardımcı Uygulama Planı (Türkçe)

## Amaç
DIABLO Immortal Assistant'ın Samsung Android tablette, oyuncunun açıkça etkinleştirdiği bir yardımcı uygulama olarak çalışabilmesinin teknik fizibilitesini değerlendirmek.

Uzun vadeli hedef, oyuncu oyunda değilken PvE alanında karakterin yaratıklara karşı tekrarlanan saldırılarını yönetebilmektir. Bu belge çalışan otomasyon bulunduğu anlamına gelmez.

## Mevcut durum
- Depodaki mevcut uygulama Python tabanlıdır.
- Karakter profili, ekran görüntüsü OCR ve PvE raporu vardır.
- Mevcut GitHub Actions iş akışı yalnızca kod testlerini çalıştırır.
- Python betiği tek başına Android oyun ekranına dokunamaz.
- Henüz Android uygulaması veya Android cihazda çalışan kontrol servisi yoktur.

## Önerilen mimari
1. **Android yardımcı uygulaması (Kotlin):** Ayrı bir Android Studio projesi olarak geliştirilir.
2. **Açık kullanıcı izni:** Ekran yakalama gerekiyorsa Android MediaProjection izni, dokunma denetimi gerekiyorsa kullanıcının Ayarlar'dan etkinleştirdiği Android AccessibilityService kullanılır.
3. **Ekran algılama:** İlk prototip yalnızca ekran görüntüsünü alır; OCR/algılama sonuçlarını gösterir. Yanlış algılamalarda saldırı başlatmaz.
4. **Sınırlı PvE denemesi:** Yalnızca oyunun normal arayüzü üzerinden, kullanıcının açıkça başlattığı ve durdurabildiği kısa bir test değerlendirilir.
5. **Karakter profili:** Python projesindeki JSON profil şeması ile Android uygulaması arasında ortak veri formatı kullanılır.

## Android kısıtları
- Uygulama, oyun açık ve ekranda değilken güvenilir biçimde oynayacağını garanti edemez.
- Ekran kilitliyken, oyun arka plandayken veya Android izinleri kaldırıldığında kontrol çalışmayabilir.
- MediaProjection ve erişilebilirlik izinleri kullanıcı tarafından açıkça verilmelidir; Android bunları güvenlik nedeniyle sınırlar.
- Samsung pil optimizasyonu, ısınma ve ekran kapanma ayarları çalışmayı etkileyebilir.
- Diablo Immortal'ın kullanım şartları otomatik oyun davranışını yasaklayabilir. Böyle bir kullanım hesap yaptırımı riski taşır. Anti-cheat atlatma, oyun belleğine müdahale veya korumaları devre dışı bırakma yapılmayacaktır.

## Geliştirme sırası
- [ ] Android proje iskeleti ve uygulama ekranı
- [ ] İzinlerin ve servis durumunun kullanıcıya açık gösterilmesi
- [ ] Yalnızca ekran yakalayan, dokunma yapmayan prototip
- [ ] Ekran algılama doğruluğu için testler
- [ ] Android'in izin verdiği ve oyunun kurallarıyla uyumlu olduğu doğrulanırsa kontrollü PvE etkileşim denemesi
- [ ] Pil, ısı, bağlantı ve durdurma davranışı testleri

## Güvenlik ve kontrol
- Uygulamada her zaman görünür bir Durdur seçeneği bulunmalıdır.
- Kullanıcı başlatmadan hiçbir işlem yapılmamalıdır.
- Oturum açma bilgileri, şifreler veya oyun hesabı belirteçleri istenmemeli ve saklanmamalıdır.
- İlk prototip saldırı veya dokunma gerçekleştirmemelidir.
