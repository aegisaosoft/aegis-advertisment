# -*- coding: utf-8 -*-
"""The fourteen lines of the ToonBee cut, in every language it is narrated in.

EN is transcribed from the ToonBee project itself — the Scene Text of each of the
fourteen scenes, word for word, including the wording ToonBee rewrote when the scenes
were regenerated. Captions built from anything else drift: ToonBee's own caption
option is transcription-based and has already produced "cantry" for "gantry".

The other languages are not translations of that text so much as the same film written
again, because the picture cannot move. Every scene is a fixed number of seconds of
animation that was exported once, so a line that runs long has nowhere to go: it would
either be cut off by the next scene or push the narration out of step with the picture
for the rest of the film. `room()` is what each line has to fit inside, and the writing
was done against it — the German and Russian scenes 7, 8 and 13 are all shorter than a
literal translation of the English would be.

ES is US/Latin-American Spanish — carro, renta, manejar, costo — because the audience is
United States fleet owners and half of them are Latino. PT is Brazilian. Never
peninsular Spanish.

The figures stay the English cut's figures in every language because the picture shows
them: $412.68 over 39 crossings. "Four-twelve" in line one and "four hundred twelve" in
line eight are the same number returning as a bill, and every language keeps that echo —
cuatro y doce, четыре двенадцать, vier Uhr zwölf, quatre heures douze, quatro e doze.

SCENES are the fourteen scene lengths read off the ToonBee timeline, confirmed frame by
frame against the export: the letter lands at 10.4s, the $412.68 board at 51.0s, the
price discs at 64.2s, the fleet at 88.2s.
"""

SCENES = [10.4, 6.0, 6.0, 6.0, 6.0, 8.4, 8.2, 7.2, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0]

# A beat after the cut before the narrator speaks, and a beat of air before the next
# scene arrives. Measured off the English cut, where Scribe put every line between
# 0.08s and 0.26s after its scene begins.
LEAD = 0.16
TAIL = 0.35

EN = [
    "Tuesday. Four-twelve in the afternoon. One of your cars goes through a toll. Nobody pays. Not yet.",
    "Three weeks later, the bill arrives with your name attached.",
    "By then, the renter is gone, refunded, and the rental is closed.",
    "So you pay it, calling it the cost of doing business.",
    "The same thing happens with tickets, fuel, and vehicle damage.",
    "But the toll agencies knew. E-ZPass, SunPass, thirty-one networks in all, coast to coast.",
    "And the booking knew who was driving. MyEZToll puts those two together and collects, "
    "from the renter's card.",
    "One small fleet. One week. Four hundred twelve dollars — and it was going to be yours to swallow.",
    "So what does the platform actually cost your fleet?",
    "Nothing: no subscription, setup fee, or charge for each vehicle.",
    "Connecting the GPS you already use is free as well.",
    "The only paid option is our own telematics hardware.",
    "You pay nothing. The toll comes back to you in full — plus a share of our fee.",
    "Stop losing. Start earning.",
]

ES = [
    "Martes. Cuatro y doce de la tarde. Uno de sus carros cruza un peaje. Nadie lo paga. Todavía no.",
    "Tres semanas después llega la factura, con su nombre.",
    "Para entonces el cliente ya se fue, le devolvieron el depósito y la renta está cerrada.",
    "Así que la paga usted, y lo llama el costo de hacer negocio.",
    "Lo mismo pasa con las multas, la gasolina y los daños al vehículo.",
    "Pero las agencias de peaje sí lo sabían. E-ZPass, SunPass, treinta y una redes, "
    "de costa a costa.",
    "Y la reserva sabía quién manejaba. MyEZToll junta las dos cosas y cobra, "
    "a la tarjeta del cliente.",
    "Una flota pequeña. Una semana. Cuatrocientos doce dólares — y los iba a pagar usted.",
    "¿Y cuánto le cuesta en realidad la plataforma a su flota?",
    "Nada: sin suscripción, sin costo de instalación, sin cargo por vehículo.",
    "Conectar el GPS que ya usa también es gratis.",
    "Lo único de pago es nuestro propio equipo de telemática.",
    "Usted no paga nada. Recibe el peaje completo y parte de nuestra comisión.",
    "Deje de perder. Empiece a ganar.",
]

RU = [
    "Вторник. Четыре двенадцать дня. Одна из ваших машин проезжает платный участок. Никто не платит. Пока.",
    "Через три недели приходит счёт — на ваше имя.",
    "Арендатор давно уехал, залог возвращён, аренда закрыта.",
    "И вы платите, называя это издержками бизнеса.",
    "То же самое со штрафами, топливом и повреждениями.",
    "Но толл-агентства знали. E-ZPass, SunPass — тридцать одна сеть по всей стране.",
    "А бронь знала, кто был за рулём. MyEZToll сводит их вместе и списывает с карты арендатора.",
    "Небольшой парк. Одна неделя. Четыреста двенадцать долларов — и заплатили бы вы.",
    "Так сколько платформа стоит вашему парку?",
    "Нисколько: ни подписки, ни платы за подключение, ни платы за машину.",
    "Подключить GPS, который у вас уже есть, тоже бесплатно.",
    "Платное только одно — наше собственное оборудование.",
    "Вы не платите ничего. Толл — весь ваш, плюс доля нашей комиссии.",
    "Хватит терять. Пора зарабатывать.",
]

DE = [
    "Dienstag. Vier Uhr zwölf nachmittags. Eines Ihrer Autos fährt durch eine Maut. Niemand zahlt. Noch nicht.",
    "Drei Wochen später kommt die Rechnung — auf Ihren Namen.",
    "Da ist der Mieter längst weg, die Kaution zurück, die Vermietung geschlossen.",
    "Also zahlen Sie und nennen es Betriebskosten.",
    "Dasselbe bei Bußgeldern, Kraftstoff und Schäden.",
    "Aber die Mautbetreiber wussten es. E-ZPass, SunPass — einunddreißig Netze, landesweit.",
    "Und die Buchung wusste, wer fuhr. MyEZToll führt beides zusammen und bucht von der Karte des Mieters ab.",
    "Eine kleine Flotte. Eine Woche. Vierhundertzwölf Dollar — und Sie hätten sie getragen.",
    "Was kostet die Plattform Ihre Flotte?",
    "Nichts: keine Gebühr, keine Einrichtung, nichts pro Fahrzeug.",
    "Ihr vorhandenes GPS anzubinden ist ebenfalls kostenlos.",
    "Bezahlt wird nur unsere eigene Telematik-Hardware.",
    "Sie zahlen nichts. Die Maut ganz, plus ein Anteil unserer Gebühr.",
    "Schluss mit Verlieren. Fangen Sie an zu verdienen.",
]

FR = [
    "Mardi. Quatre heures douze de l'après-midi. Une de vos voitures franchit un péage. Personne ne paie. Pas encore.",
    "Trois semaines plus tard, la facture arrive à votre nom.",
    "Le locataire est parti, la caution rendue, la location close.",
    "Alors vous payez, et vous appelez ça les frais du métier.",
    "Pareil pour les amendes, le carburant et les dégâts.",
    "Mais les sociétés de péage savaient. E-ZPass, SunPass — trente et un réseaux, d'une côte à l'autre.",
    "Et la réservation savait qui conduisait. MyEZToll relie les deux et débite la carte du locataire.",
    "Une petite flotte. Une semaine. Quatre cent douze dollars — et c'était pour votre poche.",
    "Alors, combien coûte la plateforme à votre flotte ?",
    "Rien : pas d'abonnement, pas de mise en service, rien par véhicule.",
    "Brancher le GPS que vous avez déjà est gratuit aussi.",
    "Seul notre boîtier télématique est payant.",
    "Vous ne payez rien. Le péage entier, plus une part de notre commission.",
    "Arrêtez de perdre. Commencez à gagner.",
]

PT = [
    "Terça-feira. Quatro e doze da tarde. Um dos seus carros passa por um pedágio. Ninguém paga. Ainda não.",
    "Três semanas depois chega a fatura, com o seu nome.",
    "A essa altura o cliente já foi, a caução voltou, a locação está fechada.",
    "Então você paga e chama isso de custo do negócio.",
    "O mesmo com multas, combustível e danos no veículo.",
    "Mas as concessionárias sabiam. E-ZPass, SunPass — trinta e uma redes, de costa a costa.",
    "E a reserva sabia quem dirigia. O MyEZToll junta as duas coisas e cobra do cartão do cliente.",
    "Uma frota pequena. Uma semana. Quatrocentos e doze dólares — e quem pagaria era você.",
    "E quanto a plataforma custa para a sua frota?",
    "Nada: sem assinatura, sem taxa de instalação, sem cobrança por veículo.",
    "Conectar o GPS que você já usa também é grátis.",
    "O único item pago é o nosso próprio equipamento de telemetria.",
    "Você não paga nada. O pedágio volta inteiro, mais uma parte da nossa taxa.",
    "Pare de perder. Comece a ganhar.",
]

UK = [
    "Вівторок. Четверта дванадцять дня. Одна з ваших машин проїжджає платну ділянку. Ніхто не платить. Поки що.",
    "Через три тижні приходить рахунок — на ваше ім'я.",
    "Орендар давно поїхав, заставу повернено, оренду закрито.",
    "І ви платите, називаючи це витратами бізнесу.",
    "Те саме зі штрафами, пальним і пошкодженнями.",
    "Але толл-агенції знали. E-ZPass, SunPass — тридцять одна мережа по всій країні.",
    "А бронювання знало, хто був за кермом. MyEZToll зводить їх разом і списує з картки орендаря.",
    "Невеликий парк. Один тиждень. Чотириста дванадцять доларів — і заплатили б ви.",
    "То скільки платформа коштує вашому парку?",
    "Ніскільки: ні підписки, ні плати за підключення, ні плати за машину.",
    "Підключити GPS, який у вас уже є, теж безкоштовно.",
    "Платне лише одне — наше власне обладнання.",
    "Ви не платите нічого. Толл — увесь ваш, плюс частка нашої комісії.",
    "Досить втрачати. Час заробляти.",
]

TR = [
    "Salı. Öğleden sonra dört on iki. Araçlarınızdan biri gişeden geçiyor. Kimse ödemiyor. Henüz.",
    "Üç hafta sonra fatura sizin adınıza geliyor.",
    "Kiracı çoktan gitti, depozito iade edildi, kiralama kapandı.",
    "Siz ödüyorsunuz ve buna işin maliyeti diyorsunuz.",
    "Aynısı cezalarda, yakıtta ve hasarda oluyor.",
    "Ama gişe kurumları biliyordu. E-ZPass, SunPass — ülke genelinde otuz bir ağ.",
    "Rezervasyon da kimin sürdüğünü biliyordu. MyEZToll ikisini birleştirip kiracının kartından tahsil ediyor.",
    "Küçük bir filo. Bir hafta. Dört yüz on iki dolar — ve ödeyecek olan sizdiniz.",
    "Peki platform filonuza ne kadara mal oluyor?",
    "Hiç: abonelik yok, kurulum ücreti yok, araç başına ücret yok.",
    "Hâlihazırda kullandığınız GPS'i bağlamak da ücretsiz.",
    "Ücretli olan tek şey kendi telematik donanımımız.",
    "Siz hiç ödemiyorsunuz. Geçiş ücreti size tam döner, artı komisyonumuzdan bir pay.",
    "Kaybetmeyi bırakın. Kazanmaya başlayın.",
]

# One recording serves both written forms: Mandarin is one spoken language, and
# Simplified and Traditional differ on the page, not in the mouth. The captions ship
# Simplified, which is what the larger part of the audience reads.
ZH = [
    "星期二，下午四点十二分。您的一辆车驶过收费站。没有人付款。还没有。",
    "三周后，账单寄到了，上面是您的名字。",
    "那时租客早已离开，押金已退，租约已结。",
    "于是您付了钱，把它称作做生意的成本。",
    "罚单、油费和车辆损坏，也是一样。",
    "但收费机构知道。E-ZPass、SunPass——全美三十一个网络。",
    "而订单知道是谁在开车。MyEZToll 把两者对上，从租客的卡上扣款。",
    "一支小车队。一个星期。四百一十二美元——本来要由您承担。",
    "那么这个平台要花您车队多少钱？",
    "一分不要：没有订阅费、安装费，也不按车收费。",
    "接入您已经在用的 GPS，同样免费。",
    "唯一收费的，是我们自己的车联网硬件。",
    "您分文不付。过路费全归您，加上我们佣金的一部分。",
    "别再亏损。开始赚钱。",
]

HY = [
    "Երեքշաբթի։ Ցերեկվա չորսն անց տասներկու։ Ձեր մեքենաներից մեկն անցնում է վճարովի հատվածով։ Ոչ ոք չի վճարում։ Դեռ։",
    "Երեք շաբաթ անց հաշիվը գալիս է՝ ձեր անունով։",
    "Վարձակալը վաղուց գնացել է, գրավը վերադարձված է, վարձակալությունը՝ փակված։",
    "Եվ դուք վճարում եք՝ անվանելով դա բիզնեսի ծախս։",
    "Նույնը՝ տուգանքների, վառելիքի և վնասների դեպքում։",
    "Բայց վճարովի ճանապարհների գործակալությունները գիտեին։ E-ZPass, SunPass — երեսունմեկ ցանց ամբողջ երկրում։",
    "Իսկ ամրագրումը գիտեր, թե ով էր ղեկին։ MyEZToll-ը միացնում է դրանք և գանձում վարձակալի քարտից։",
    "Փոքր ավտոպարկ։ Մեկ շաբաթ։ Չորս հարյուր տասներկու դոլար — և վճարելու էիք դուք։",
    "Իսկ որքա՞ն է հարթակն արժենում ձեր ավտոպարկին։",
    "Ոչինչ՝ ոչ բաժանորդագրություն, ոչ միացման վճար, ոչ վճար մեքենայի համար։",
    "Ձեր արդեն օգտագործվող GPS-ը միացնելը նույնպես անվճար է։",
    "Վճարովի է միայն մեր սեփական սարքավորումը։",
    "Դուք ոչինչ չեք վճարում։ Վճարն ամբողջովին ձերն է, գումարած մեր միջնորդավճարի մասը։",
    "Բավական է կորցնել։ Ժամանակն է վաստակելու։",
]

KA = [
    "სამშაბათი. შუადღის ოთხი და თორმეტი. თქვენი ერთ-ერთი მანქანა ფასიან მონაკვეთს გადის. არავინ იხდის. ჯერჯერობით.",
    "სამი კვირის შემდეგ ანგარიში მოდის — თქვენს სახელზე.",
    "მოიჯარე დიდი ხნის წასულია, გირაო დაბრუნებული, ქირავნობა დახურული.",
    "და თქვენ იხდით, ამას ბიზნესის ხარჯს უწოდებთ.",
    "იგივე ხდება ჯარიმებთან, საწვავთან და დაზიანებებთან.",
    "მაგრამ საგზაო სააგენტოებმა იცოდნენ. E-ZPass, SunPass — ოცდათერთმეტი ქსელი მთელ ქვეყანაში.",
    "ჯავშანმა კი იცოდა, ვინ იჯდა საჭესთან. MyEZToll აკავშირებს მათ და ჩამოჭრის მოიჯარის ბარათიდან.",
    "პატარა ავტოპარკი. ერთი კვირა. ოთხასთორმეტი დოლარი — და გადაიხდიდით თქვენ.",
    "მაშ, რა ჯდება პლატფორმა თქვენს ავტოპარკს?",
    "არაფერი: არც გამოწერა, არც ჩართვის საფასური, არც გადასახადი მანქანაზე.",
    "თქვენი უკვე არსებული GPS-ის მიერთებაც უფასოა.",
    "ფასიანი მხოლოდ ჩვენი საკუთარი აღჭურვილობაა.",
    "თქვენ არაფერს იხდით. გადასახადი მთლიანად თქვენია, პლუს ჩვენი საკომისიოს წილი.",
    "საკმარისია დანაკარგები. დროა გამოიმუშაოთ.",
]

# Persian and Urdu are written right to left. The lines are stored in logical order —
# first word first — which is what a caption file, a browser and a player all expect;
# the rendering is the reader's side of the problem, not the file's.
FA = [
    "سه‌شنبه. چهار و دوازده عصر. یکی از خودروهایتان از عوارضی می‌گذرد. هیچ‌کس پرداخت نمی‌کند. هنوز نه.",
    "سه هفته بعد، صورت‌حساب به نام شما می‌رسد.",
    "مستأجر رفته، ودیعه برگشته، اجاره بسته شده.",
    "پس شما پرداخت می‌کنید و نامش را هزینه کسب‌وکار می‌گذارید.",
    "همین اتفاق برای جریمه، سوخت و خسارت خودرو می‌افتد.",
    "اما عوارضی‌ها می‌دانستند. E-ZPass، SunPass — سی و یک شبکه در کل کشور.",
    "و رزرو راننده را می‌شناخت. MyEZToll این دو را به هم می‌رساند و از کارت مستأجر می‌گیرد.",
    "ناوگان کوچک. یک هفته. چهارصد و دوازده دلار — پای شما.",
    "پس این پلتفرم برای ناوگان شما چقدر هزینه دارد؟",
    "هیچ: نه اشتراک، نه هزینه راه‌اندازی، نه هزینه هر خودرو.",
    "اتصال همان GPS که دارید هم رایگان است.",
    "تنها چیز پولی، سخت‌افزار تله‌متیک خودمان است.",
    "هیچ نمی‌پردازید. عوارض کامل، و سهمی از کارمزد ما.",
    "دیگر ضرر نکنید. درآمد را شروع کنید.",
]

UR = [
    "منگل۔ سہ پہر چار بج کر بارہ منٹ۔ آپ کی ایک گاڑی ٹول سے گزرتی ہے۔ کوئی ادائیگی نہیں کرتا۔ ابھی نہیں۔",
    "تین ہفتے بعد بل آپ کے نام پر آتا ہے۔",
    "تب تک کرایہ دار جا چکا، ضمانت واپس ہو چکی، کرایہ ختم ہو چکا۔",
    "تو آپ ادا کرتے ہیں اور اسے کاروبار کی لاگت کہتے ہیں۔",
    "یہی چالان، ایندھن اور گاڑی کے نقصان کے ساتھ ہوتا ہے۔",
    "لیکن ٹول ادارے جانتے تھے۔ E-ZPass، SunPass — پورے ملک میں اکتیس نیٹ ورک۔",
    "بکنگ کو ڈرائیور معلوم تھا۔ MyEZToll دونوں کو ملا کر کرایہ دار کے کارڈ سے لیتا ہے۔",
    "ایک چھوٹا بیڑا۔ ایک ہفتہ۔ چار سو بارہ ڈالر — اور ادا آپ کو کرنا تھا۔",
    "تو یہ پلیٹ فارم آپ کے بیڑے پر کتنا خرچ آتا ہے؟",
    "کچھ نہیں: نہ سبسکرپشن، نہ سیٹ اپ فیس، نہ فی گاڑی کوئی چارج۔",
    "جو GPS آپ پہلے سے استعمال کرتے ہیں، اسے جوڑنا بھی مفت ہے۔",
    "صرف ہمارا اپنا ٹیلی میٹکس ہارڈویئر پیسوں والا ہے۔",
    "آپ کچھ ادا نہیں کرتے۔ ٹول پورا آپ کا، ساتھ ہماری فیس کا حصہ۔",
    "نقصان اٹھانا بند کریں۔ کمانا شروع کریں۔",
]

# Uzbek is read by nobody: no ElevenLabs model speaks it, so this text is never
# recorded. It is a subtitle track over the English narration, and the lines are
# therefore written to be *read* inside the English line's own seconds rather than
# spoken inside the scene's. Latin script, which is what Uzbekistan writes today.
UZ = [
    "Seshanba. Kunduzi soat toʻrt oʻn ikki. Mashinangizdan biri toʻlov punktidan oʻtadi. Hech kim toʻlamaydi. Hali emas.",
    "Uch hafta oʻtib, hisob sizning nomingizga keladi.",
    "Ijarachi allaqachon ketgan, garov qaytarilgan, ijara yopilgan.",
    "Siz toʻlaysiz va buni biznes xarajati deb ataysiz.",
    "Jarimalar, yoqilgʻi va shikastlar bilan ham xuddi shunday.",
    "Ammo yoʻl toʻlovi agentliklari bilardi. E-ZPass, SunPass — butun mamlakat boʻylab oʻttiz bitta tarmoq.",
    "Bron esa kim rulda boʻlganini bilardi. MyEZToll ikkisini bogʻlaydi va ijarachining kartasidan yechadi.",
    "Kichik avtopark. Bir hafta. Toʻrt yuz oʻn ikki dollar — va toʻlaydigan siz edingiz.",
    "Xoʻsh, platforma avtoparkingizga qanchaga tushadi?",
    "Hech narsaga: obuna yoʻq, ulanish toʻlovi yoʻq, mashina uchun toʻlov yoʻq.",
    "Allaqachon foydalanayotgan GPS’ingizni ulash ham bepul.",
    "Faqat bitta narsa pullik — oʻzimizning uskunamiz.",
    "Siz hech narsa toʻlamaysiz. Toʻlov toʻliq sizga qaytadi, ustiga komissiyamizning bir qismi.",
    "Yoʻqotishni bas qiling. Daromad topishni boshlang.",
]

LANGS = {'en': EN, 'es': ES, 'ru': RU, 'de': DE, 'fr': FR, 'pt': PT,
         'uk': UK, 'tr': TR, 'zh': ZH,
         'hy': HY, 'ka': KA, 'fa': FA, 'ur': UR, 'uz': UZ}

# The one language nobody reads aloud. Its captions are timed off the English
# narration, so it needs no clips, no voice and no place in the recording tools.
SUBTITLED = {'uz': 'en'}

for _code, _lines in LANGS.items():
    assert len(_lines) == len(SCENES), '%s has %d lines, not %d' % (_code, len(_lines), len(SCENES))


def grid():
    """(start, end) of every scene, in seconds."""
    out, edge = [], 0.0
    for d in SCENES:
        out.append((edge, edge + d))
        edge += d
    return out


def room():
    """Seconds each line has to be spoken in, once the lead-in and the tail are taken."""
    return [d - LEAD - TAIL for d in SCENES]
