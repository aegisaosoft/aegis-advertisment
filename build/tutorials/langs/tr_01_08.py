# -*- coding: utf-8 -*-
"""Episodes 1-8 in Turkish (tr), one entry per beat, loaded through E.translate.

UI names are the portal's own, taken from aegis-owner-web src/locales/tr/common.json.
"""

EPISODES = {
    # ------------------------------------------------------------------------------------------- 1
    1: dict(
        title='Portalda bir tur',
        sub='Her şey nerede, ve verilerinizi gizleyen tek ayar',
        lines=[
            dict(text='owner.myeztoll.com adresinde oturum açın; ilk gördüğünüz ekran Kontrol Paneli.',
                 say='owner nokta my e z toll nokta com adresinde oturum açın; ilk gördüğünüz ekran Kontrol Paneli.',
                 label='Kontrol Paneli'),
            'On iki kart, burada yapacağınız her iş için bir tane. Her birinde canlı bir sayı var: kaç aracınız '
            'olduğu, kaç ödemenin ilgi beklediği.',
            dict(text='Asıl gezinme soldaki kenar çubuğunda. Ekranlara göre değil, işlere göre gruplanmıştır.',
                 label='Kenar çubuğu'),
            'Şirket, Faturalandırma, Rezervasyonlar, Araçlar, Sürücüler, Ortaklık, Ödemeler, Geçiş ücretleri ve '
            'ihlaller, Raporlar, SMS ve E-posta, Yönetim. Açmak için bir gruba tıklayın.',
            'Grup olduğu yerde açılır. Baktığınız hiçbir şey kaybolmaz.',
            dict(text='Sağ üstte dil seçici. Bu serideki her şey, orada listelenen tüm dillerde aynen çalışır.',
                 label='Dil'),
            dict(text='Yanında Yardım. Hangi sayfada olduğunuzu bilir ve ürün hakkında genel değil, o sayfa '
                      'hakkında yanıt verir.', label='Yardım'),
            dict(text='Sol üstte de şirketinizin adı. Bu, göründüğünden daha önemlidir.',
                 label='Kimin adına çalışıyorsunuz'),
            'Yöneticiyseniz ya da ortaksanız, erişiminiz olan herhangi bir sahip adına çalışabilirsiniz. O zaman '
            'her sayfa yalnızca o sahibi gösterir.',
            'Bir sayfa boş görünüyorsa ve boş olmaması gerektiğinden eminseniz, önce buraya bakın. Yanlış sahip '
            'adına çalışmak, ekranın boş gelmesinin en yaygın nedenidir.',
            dict(text='Haritanın tamamı bu. Sonraki bölümde, daha tek bir rezervasyon yokken işinizin kurallarını '
                      'belirliyoruz.', label=' '),
        ]),

    # ------------------------------------------------------------------------------------------- 2
    2: dict(
        title='Her şeyi belirleyen ayarlar',
        sub='Şirket → Ayarlar, daha tek bir rezervasyon yokken',
        lines=[
            dict(text='Şirket, sonra Ayarlar. Bu sayfa işinizin nasıl çalışacağını belirler. İlk rezervasyondan '
                      'önce ona on dakika ayırmaya değer.', label='Şirket → Ayarlar'),
            'Üstteki sekmeler ayrı ayar sayfalarıdır, sadece tek bir Kaydet düğmesini paylaşırlar. Geçiş Ücreti '
            'Hesapları, GPS sistemleri ve Hizmetler ileride kendi bölümlerinde anlatılacak.',
            'Bu satır kimin ayarlarını düzenlediğinizi söyler. Birkaç sahibin olduğu bir platformda, bir şeyi '
            'değiştirmeden önce bu satırı okuyun.',
            dict(text='Şirket ve Alan Adı. Buradaki ad, kiracılarınızın vitrininizde gördüğü addır. Alan adı da '
                      'vitrininizin açıldığı web adresidir.', label='Şirket ve Alan Adı'),
            dict(text='.myezwheels.com\'un önüne gelecek kısmı yazın ve Alan adı oluştur\'a basın. Alan adı '
                      'olmadan araçlarınız hiçbir yerde listelenemez.',
                 say='nokta my e z wheels nokta com\'un önüne gelecek kısmı yazın ve Alan adı oluştur\'a basın. '
                     'Alan adı olmadan araçlarınız hiçbir yerde listelenemez.'),
            dict(text='Altında Yapılandırma. Minimum güvenlik depozitosu: depozitosu bundan düşük olan her araç '
                      'otomatik olarak bu tutara yükseltilir.', label='Yapılandırma'),
            'Belirsiz GPS geçişlerini tahsil et. Varsayılan olarak kapalıdır ve kapalı kalması iyidir: yanında '
            'ücretsiz şerit olan, yanlış eşleşebilen gişelerdeki düşük güvenli, yalnızca GPS geçişlerini '
            'faturalayıp faturalamayacağını belirler.',
            'Reddedilen geçiş tahsilatlarını yeniden dene. Bu da varsayılan olarak kapalı. Açıksa, geçici bir '
            'nedenle reddedilen kart sonraki günlerde yeniden denenir. Kapalıysa, geçiş ücreti başarısız olarak '
            'size kalır. Her iki durumda da kiracı kartını düzeltmesi için bir bağlantı alır.',
            'Temizlik Ücreti ve Sigara Ücreti yanlarında, Minimum Rezervasyon Günü de sağda. Üçü de kural değil, '
            'varsayılandır: bir aracın kendi değeri olabilir.',
            dict(text='En çok zaman kazandıran blok bu. Fiyatlandırma dönemi, sigorta, haftalık fiyat, renkler: '
                      'eklediğiniz her yeni araç bunlar zaten doldurulmuş olarak başlar.',
                 label='Yeni araçlar için varsayılanlar'),
            dict(text='Daha aşağıda E-posta Aktarımı. mail.myeztoll.com\'da herkese açık bir takma ad kaydedersiniz; '
                      'ona gönderilen her şey gerçek adresinize iletilir.',
                 say='Daha aşağıda E-posta Aktarımı. mail nokta my e z toll nokta com\'da herkese açık bir takma ad '
                     'kaydedersiniz; ona gönderilen her şey gerçek adresinize iletilir.',
                 label='E-posta Aktarımı'),
            'Gönderdiğiniz yanıtlar takma ad üzerinden çıkar, böylece sürücü gerçek e-posta adresinizi asla öğrenmez.',
            'Tek bir anahtar tüm aktarımı kapatır; o zaman gelen e-postalar iletilmez, geri çevrilir.',
            dict(text='Sonra sağ üstteki Kaydet. Kaydedilmemiş değişikliklerle sayfadan çıkarken önce size sorulur, '
                      'ama Kaydet\'e basmak daha kolay.', label='Kaydet'),
        ]),

    # ------------------------------------------------------------------------------------------- 3
    3: dict(
        title='Geçiş ücreti kurumlarınızı bağlamak',
        sub='Sistemin geçiş ücretlerini sizin yerinize toplamasını sağlayan giriş bilgileri',
        lines=[
            dict(text='Şirket, Ayarlar ve Geçiş Ücreti Hesapları sekmesi. Sistemin geçiş ücretlerinizi toplamak '
                      'için kullandığı girişleri burada verirsiniz.', label='Ayarlar → Geçiş Ücreti Hesapları'),
            'Önce ne yaptığını anlayın. Sizin adınıza, bir programa göre her kurumun portalına girer ve '
            'araçlarınızın biriktirdiği geçiş ücretlerini indirir. Bir veri akışı ya da API yok; kendiniz '
            'açacağınız web sitesinin aynısı.',
            dict(text='En üstteki Geçiş ağı kapsamı her ağ için bir etiket gösterir; giriş bilgileriniz varsa '
                      'üzerinde onay işareti olur. Tek bir E-ZPass hesabı on sekizden fazla E-ZPass kurumunun '
                      'hepsini kapsar; her eyalet için ayrı hesap açmayın.', label='Geçiş ağı kapsamı'),
            'Bir hesap eklemek için Hesap ekle\'ye basın.',
            dict(text='Sağlayıcıyı seçin. Aynı kurumda birden fazla hesabınız varsa bir takma ad verin. Takma ad '
                      'yalnızca sizin içindir.', label='Geçiş hesabı ekle'),
            'Hesap numarası, kullanıcı adı, şifre: tam olarak kurumun sitesinde kullandıklarınız. Hesap numarası '
            'isteğe bağlıdır; bazı kurumlar kullanmaz.',
            'Şifre şifrelenmiş olarak saklanır ve ne size ne de desteğe asla açık metin olarak gösterilmez.',
            'Kaydedin, hesap bir kart olarak görünür.',
            dict(text='Her kartın sağında bir sıra küçük simge vardır; gerçekten kullanacağınız ikisi şunlar.',
                 label='Her hesap için bir kart'),
            dict(text='Şimşek, Bağlantıyı test et. Üç hafta sonra hiçbir şeyin toplanmadığını öğrenmek yerine, '
                      'şimdi buradayken basın.', label='Bağlantıyı test et'),
            dict(text='Kalkan, Cihazı doğrula. Sistem yeni bir makineden ilk kez girdiğinde çoğu kurum bir kod '
                      'e-postalar. Kalkana basıp kodu girin; toplama sizsiz devam edebilir.', label='Cihazı doğrula'),
            'Her kartın solundaki küçük fiş, o kurumu çalıştıran yazılımın sunucuda kurulu olup olmadığını söyler. '
            'Yeşil yüklü demektir. Kırmızı eksik demektir; bu sizin değil, desteğin işidir.',
            dict(text='Hesaplar bağlanınca geçiş ücretleri kendiliğinden gelmeye başlar. Sırada: bu ücretlerin '
                      'bağlanacağı bir şey olsun diye araçlarınızı sisteme almak.', label=' '),
        ]),

    # ------------------------------------------------------------------------------------------- 4
    4: dict(
        title='Araç listesi',
        sub='Okumak, filtrelemek ve her satırda gizli menü',
        lines=[
            dict(text='Araçlar, sonra Tüm Araçlar. Sahip olduğunuz her araç, buraya nasıl gelmiş olursa olsun, bu '
                      'sayfadadır.', label='Araçlar → Tüm Araçlar'),
            'Üstte beş düğme. İçe Aktar bir tablo dosyası alır, Araç Ekle tek bir aracı elle ekler, Detayları '
            'göster tabloyu genişletir, Yeniden Yükle tabloyu yeniden okur, Sağlayıcıları ata da birkaç araca '
            'aynı anda geçiş kurumu bağlar.',
            dict(text='Altında filtreler. Tür, durum, geçiş ayarı ve plaka, ad, e-posta ya da türle eşleşen bir '
                      'arama kutusu; hangisi olduğunu söylemeniz gerekmez. Geçiş ayarını aklınızda tutun: listeyi '
                      'bir kuruma bağlı araçlara ya da bağlı olmayanlara daraltır.', label='Filtreler'),
            dict(text='Tablonun kendisi. Plaka ve Başlık kırmızı bir yıldız taşır; bu, sistemin zorunlu olduklarını '
                      'söylemesidir. Plaka, ürünün her yerinde aracı tanımlar.', label='Sütunlar'),
            dict(text='Rezervasyon Durumu, aracın aktif bir rezervasyonda olup olmadığını söyler. Göz gezdirmeniz '
                      'gereken Ödeme Durumu: "Geçiş ücreti yok" sorun değil, "Başarısız" geçmeyen bir kart, '
                      '"Rezervasyon ödemesi takıldı" ise bugün bakılmalı.', label='Ödeme Durumu'),
            'Her satırın solunda bir sıra simge var: harita, tanılama, takvim ve bilgi. Takip cihazı olmayan bir '
            'araçta bunlardan daha azı görünür.',
            'Üç nokta da asıl işi yapan menüyü açar.',
            dict(text='Rezervasyon Yap bu araçla bir rezervasyon başlatır. Rezervasyonları Görüntüle mevcut olanları '
                      'gösterir. Tüm EZ Geçiş Ücretleri aracın şimdiye kadarki her geçişini listeler.',
                 label='Satır menüsü'),
            'Yolculuk aracın nerede olduğunu çizer, Tanılama takip cihazını okur, Düzenle de tam araç formunu açar. '
            'Altı işlem, her satırdan tek tıkla.',
            dict(text='En altta sayı ve sayfalama. Varsayılan olarak sayfa başına on satır. Bunu buradan değiştirin, '
                      'yoksa kırk araçlık bir filo dört sayfa kaydırma demektir.', label='Sayfalama'),
        ]),

    # ------------------------------------------------------------------------------------------- 5
    5: dict(
        title='Filonuzu sisteme almak',
        sub='Bir tablo dosyası, elle tek bir araç ya da doğrudan bir kurumdan',
        lines=[
            dict(text='Araçları sisteme almanın birden fazla yolu var. En hızlısı, listenizin şu an nerede '
                      'durduğuna bağlıdır.', label='Beş giriş yolu'),
            'Zaten bir rezervasyon platformu kullanıyorsanız (HQ Rental, Renteon, RENTALL, TSD), filoyu oradan '
            'çekin; rezervasyonlarıyla birlikte gelir. Bir geçiş kurumu araçlarınızı zaten biliyorsa, araçları '
            'kurumdan oluşturun; transponder bağlantısı da hazır gelir.',
            'Elinizde bir tablo dosyası varsa, İçe Aktar\'a basın.',
            dict(text='Dosyayı bırakın. CSV, xlsx ve xls çalışır, sütunlar sizin için eşleştirilir; elle hiçbir '
                      'şey eşlemeniz istenmez.', label='Araç İçe Aktar'),
            'İki sütun zorunludur: plaka numarası ve plaka ili. Bu ikisi birlikte aracı geçiş kurumuna tanıtır. '
            'İl bilgisi olmayan bir dosya sonradan tek işlemle tamamlanabilir.',
            'Bir iki araç için elle eklemek daha hızlı. Araç Ekle.',
            dict(text='Üç sekme: Temel Bilgiler, Fiyatlandırma, Konum. Herhangi birinden kaydedebilirsiniz; diğer '
                      'ikisi sonra doldurulabilir.', label='Yeni Araç Ekle'),
            'Başlık ve açıklama kiracının okuduğu kısımdır. Başlık zorunludur ve bu aracın diğer tüm ekranlarda '
            'taşıyacağı addır.',
            dict(text='İki onay kutusu aracın görünüp görünmeyeceğini belirler. İlanı yayınla onu vitrininize koyar; '
                      'My E-Z Wheels’ta göster ortak pazar yerine ekler.', label='Nerede listelenir'),
            dict(text='Geçiş Ücreti Sistemleri, bu aracın faturalanıp faturalanamayacağını belirleyen satırdır. '
                      'Ekle ona bir kurum bağlar. Buradaki boş liste, bir geçiş ücretinin tahsil edilecek kimse '
                      'olmadan gelmesinin en yaygın nedenidir.', label='Geçiş Ücreti Sistemleri'),
            dict(text='Sonra Araç Bilgileri. Tür, ülke, marka, model, yıl, renkler: çoğu, ikinci bölümde '
                      'belirlediğiniz varsayılanlardan zaten doldurulmuştur.', label='Araç Bilgileri'),
            'Plaka Numarası ve Plaka İli. Formdaki her şeyden önemli bu ikisi: ili yanlış girerseniz kurum bu '
            'aracı asla eşleştiremez.',
            'VIN ve GPS Takip Cihazı IMEI isteğe bağlıdır. Ama IMEI takip cihazını bu araca bağlar; takip cihazı '
            'da sistemin, kurumun size hiç faturalamadığı bir geçişi bulmasını sağlar.',
            dict(text='Aracı Kaydet. Bir araç tamam. Sırada: insanların atladığı ve sonra paralarının nereye '
                      'gittiğini bir ay merak ettiği adım.', label='Aracı Kaydet'),
        ]),

    # ------------------------------------------------------------------------------------------- 6
    6: dict(
        title='Transponderlar: kimsenin atlamaması gereken adım',
        sub='Arkasında araç olmayan bir etiket kimseye faturalanamaz',
        lines=[
            dict(text='Geçiş ücretleri ve ihlaller\'den bir geçiş hesabı açın; kendi sayfası gelir: kurumun sizin '
                      'için tuttuğu her araç ve her transponder.', label='Bir geçiş sağlayıcısı hesabı'),
            'İki sekme. Araçlar, kurumun sizin sahip olduğunuzu düşündüğü araçlardır. Transponderlar, kurumun '
            'verdiği etiketlerdir. Sayılar nadiren tutar; bu bölüm aradaki farkla ilgili.',
            'Neden önemli: geçiş ücreti, aracı kim sürüyorsa ona faturalanır. Kurum size bir etiketin gişeden '
            'geçtiğini söyler. Bunu bir araca ancak etiket-araç bağlantısı çevirir. Rezervasyonu olan yalnızca '
            'araçtır, kartlı sürücüsü olan da yalnızca rezervasyon.',
            dict(text='Bu yüzden sayfanın en yararlı satırı bu açıklama. Bağlı, tamam demektir. DB\'de transponder '
                      'yok: kurum aracı biliyor ama bizde etiketi yok. Transponder DB\'den farklı: ikisi uyuşmuyor '
                      've biri eski.', label='Beş durum'),
            'Sağlayıcı atanmamış: araç burada var ama ona bağlı bir geçiş kurumu yok; bu, beşinci bölümdeki Geçiş '
            'Ücreti Sistemleri satırıdır. DB\'de yok: kurumda bizim hiç duymadığımız bir araç var.',
            dict(text='Durum sütunu bunu her satırda tekrarlar; listede aşağı inip hangi araçların size hiçbir şey '
                      'kazandırmadığını tam olarak görebilirsiniz.', label='Araç başına durum'),
            dict(text='Sağdaki Transponder sütunu da cevabı verir: doluysa o araç faturalanabilir. Boşsa, ondan '
                      'gelen geçiş ücreti tahsil edilecek kimse bulamaz ve size kalır.', label='Transponder'),
            dict(text='Şimdi tuzak. Bu uyarı, transponder listesinin önbellekten geldiğini söyler ve kurumdan en '
                      'son ne zaman okunduğunu belirtir.', label='Liste önbellekten'),
            'Kurumun o andan sonra verdiği hiçbir etiket bu listede yoktur. Yani bir transponderın var olduğundan '
            'eminseniz ve burada bulamıyorsanız, liste eskidir; transponder kayıp değildir.',
            dict(text='Araç ve transponder listesini yenile, kuruma geri gidip listeyi yeniden okur. Bir sorun '
                      'olduğuna karar vermeden önce buna basın.', label='Yenile'),
            'Biraz sürer ve bunu söyler: önce araçları yükler, sonra arkalarındaki tüm transponder envanterini '
            'tarar.',
            dict(text='Bunu ilk gününüzde her geçiş hesabı için bir kez yapın, kurum size her yeni etiket '
                      'gönderdiğinde de tekrarlayın. Atlarsanız geçiş ücretleri yine gelir, ama sürücüye değil, '
                      'size gelir.', label=' '),
        ]),

    # ------------------------------------------------------------------------------------------- 7
    7: dict(
        title='Tarifeler ve fiyat sezonları',
        sub='Bütün bir kategoriyi tek seferde fiyatlayın, yoğun haftaları farklı fiyatlayın',
        lines=[
            dict(text='Araçlar, sonra Tarifeler. Bu sayfa tek bir aracı açmadan filonuzu fiyatlar.',
                 label='Araçlar → Tarifeler'),
            dict(text='Önce hangi tarifeyi belirlediğinizi seçin: günlük, haftalık ya da aylık. Bunlar üç ayrı '
                      'fiyattır ve bu seçim sayfadaki her rakamı değiştirir.', label='Günlük · Haftalık · Aylık'),
            'Altındaki liste, kategoriye göre gruplanmış filonuzdur: Ekonomik, Lüks, Premium, Spor, SUV. Her grup '
            'markalara, modellere ve en sonunda tek tek araçlara açılır.',
            dict(text='Kutudan önce rakamı okuyun. Bir sayı, o gruptaki her aracın zaten o fiyatta olduğunu '
                      'gösterir. "farklı" kelimesi öyle olmadığını gösterir; buraya değer girerseniz hepsinin '
                      'üzerine yazılır.', label='"farklı" bir uyarıdır'),
            'Yeni tarifeyi yazıp Uygula\'ya basın; o başlık altındaki her araca tek seferde yazılır.',
            'Sadece bir modeli kastettiyseniz önce grubu açın. Kategorinin en üstünde uygulamak hızlıdır; '
            'dokunmak istemediğiniz bir aracı yeniden fiyatlamanın da en hızlı yoludur.',
            dict(text='Sonra Fiyat sezonları; aynı fikir, bir tarih aralığı için.', label='Fiyat sezonları'),
            'Bir sezonun adı, başlangıcı, bitişi ve önceliği vardır. İki sezon çakıştığında yüksek öncelikli '
            'kazanır; tatil haftası yaz sezonunun içinde böyle durur ve daha pahalıya gelir.',
            'Sezon ekle\'ye basın; sezon bu tabloda görünür.',
            dict(text='Sonra sezonu buradan seçin ve temel tarifeleri nasıl fiyatladıysanız öyle fiyatlayın: '
                      'kategoriye, markaya, modele göre ya da tek bir araç.', label='Araç sezon fiyatları'),
            'En alttaki kuralı iki kez okumaya değer: bir kademeyi boş bırakırsanız o dönem aracın temel fiyatına '
            'döner. Boş, sıfır demek değildir.',
            dict(text='Hangi sezonun geçerli olduğunu rezervasyonun yapıldığı gün değil, kiralamanın başlangıç '
                      'tarihi belirler. Nisan\'da ağustos için alınan rezervasyon, ağustos fiyatıyla fiyatlanır.',
                 label=' '),
        ]),

    # ------------------------------------------------------------------------------------------- 8
    8: dict(
        title='Rezervasyon ekranı',
        sub='Aynı rezervasyonlara iki bakış, ve her satırda on işlem',
        lines=[
            dict(text='Rezervasyonlar. Sahip olduğunuz her rezervasyon, bir listede.', label='Rezervasyonlar'),
            dict(text='Durum filtresi tümüyle değil, seçili sekiz durumla başlar. Var olduğunu bildiğiniz bir '
                      'rezervasyon bu sayfada yoksa, bir sonuca varmadan önce o filtreyi açın.',
                 label='Durumlardan sekizi'),
            'İki sekme: Liste ve Planlayıcı. Aynı rezervasyonlar, onlara iki bakış.',
            dict(text='Listede üç sütun bütün hikâyeyi anlatır. Kiralama Sözleşmesi, sözleşmenin imzalandığını, '
                      'gönderildiğini ya da gerekmediğini gösterir.', label='Kiralama Sözleşmesi'),
            dict(text='Durum, rezervasyonun kendi durumudur: Onaylandı, Tamamlandı, Erken Tamamlandı, Kart bekleniyor.',
                 label='Durum'),
            dict(text='Geçiş Ücreti Ödemeleri de paradır: Başarılı, Başarısız, Tahsil edilmedi, Ödeme takıldı. Her '
                      'sabah göz gezdirmeniz gereken sütun bu.', label='Geçiş Ücreti Ödemeleri'),
            'Bunun gibi bir satır durumu açıkça söyler: kart bekleniyor, hiçbir şey tahsil edilmedi ve bir koşul '
            'hâlâ karşılanmadı. Bu düzelene kadar o rezervasyondan hiç para tahsil edilmez.',
            'Bir satırdaki üç nokta, o rezervasyonla yapabileceğiniz her şeyi açar.',
            dict(text='Menü, en üstte rezervasyonun kendisiyle açılır: kim, hangi araç, tarihler, durum. Böylece asla '
                      'yanlış satırda işlem yapmazsınız.', label='Satır menüsü'),
            'Aracı Değiştir bu rezervasyonu başka bir araca taşır. Rezervasyonu yeniden aç biten bir rezervasyonu '
            'geri getirir. İkisi de geçiş ücretlerini de taşır; bilerek kullanın.',
            'Tahsilatlar, Rezervasyon bilgisi, Geçiş Ücretlerini Görüntüle ve İhlalleri Görüntüle salt okunur '
            'olanlardır: bu rezervasyona ne faturalandığı ve neden.',
            dict(text='Fatura oluştur, bu rezervasyondaki ödenmemiş geçiş ücretlerini sürücü için tek bir faturaya '
                      'çevirir. Kart gittiğinde ama geçiş ücretleri kaldığında kullanılacak araç bu.',
                 label='Fatura oluştur'),
            'Rezervasyonu tahsil et şimdi faturalar. Kiralama Sözleşmesi sözleşmeyi gönderir ya da yeniden gönderir. '
            'On işlem, hiçbiri başka bir ekran gerektirmez.',
            dict(text='Planlayıcı, aynı rezervasyonların zamana karşı çizilmiş hâlidir: her araç için bir satır, her '
                      'rezervasyon için bir çubuk.', label='Planlayıcı'),
            'Kırmızı çizgi bugündür. Bir satırdaki boşluk, boşta duran bir araçtır. Sağ kenarı aşan çubuk da henüz '
            'bitmemiş bir rezervasyondur.',
            'Alttaki renkler de listedeki durumların aynısıdır. Hangi görünümü seçerseniz seçin, aynı dört kelimeyi '
            'okuyorsunuz.',
        ]),
}
