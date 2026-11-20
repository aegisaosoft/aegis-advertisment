# -*- coding: utf-8 -*-
"""Uzbek (Latin) narration for tutorial episodes 1-8. Loaded via E.translate('uz', ...)."""

EPISODES = {
    # ------------------------------------------------------------------------------------------ 1
    1: dict(
        title="Portal bo'ylab sayohat",
        sub="Hamma narsa qayerda turadi va ma'lumotlaringizni yashiradigan bitta sozlama",
        lines=[
            dict(text="owner.myeztoll.com saytiga kiring, birinchi ko'radiganingiz — Boshqaruv paneli.",
                 say="owner nuqta my e z toll nuqta com saytiga kiring, birinchi ko'radiganingiz — Boshqaruv paneli.",
                 label="Boshqaruv paneli"),
            "O'n ikkita karta, bu yerda qiladigan har bir ishingiz uchun bittadan. Har birida jonli raqam bor: "
            "nechta avtomobilingiz bor, nechta to'lov e'tibor talab qiladi.",
            dict(text="Asosiy navigatsiya chapdagi yon panelda. U ekranlar bo'yicha emas, ishlar bo'yicha guruhlangan.",
                 label="Yon panel"),
            "Kompaniya, Hisob-kitob, Bronlar, Transport vositalari, Haydovchilar, Hamkorlik, To'lovlar, Yo'l to'lovlari "
            "va qoidabuzarliklar, Hisobotlar, SMS va Mail, Boshqarish. Guruhni ochish uchun ustiga bosing.",
            "Guruh shu joyning o'zida ochiladi. Ko'rib turganingiz yo'qolmaydi.",
            dict(text="Yuqori o'ngda til tanlash. Bu turkumdagi hamma narsa u yerdagi istalgan tilda xuddi shunday ishlaydi.",
                 label="Til"),
            dict(text="Uning yonida Yordam. U qaysi sahifadaligingizni biladi va umuman mahsulot haqida emas, "
                      "aynan shu sahifa haqida javob beradi.",
                 label="Yordam"),
            dict(text="Yuqori chapda esa kompaniyangiz nomi. Bu ko'rinishidan ko'ra muhimroq.",
                 label="Kim sifatida ishlayapsiz"),
            "Agar siz administrator yoki hamkor bo'lsangiz, ruxsatingiz bor istalgan ega sifatida ishlay olasiz. "
            "Shunda har bir sahifa faqat o'sha egani ko'rsatadi.",
            "Sahifa bo'sh ko'rinsa-yu, bo'sh bo'lmasligiga ishonchingiz komil bo'lsa, avval shu yerga qarang. "
            "Noto'g'ri ega sifatida ishlash — ekran bo'sh chiqishining eng ko'p uchraydigan sababi.",
            dict(text="Butun xarita shu. Keyingi qismda birorta bron bo'lmasidan oldin biznesingiz ishlaydigan "
                      "qoidalarni o'rnatamiz.",
                 label=" "),
        ]),

    # ------------------------------------------------------------------------------------------ 2
    2: dict(
        title="Hamma narsani hal qiladigan sozlamalar",
        sub="Kompaniya → Sozlamalar, birorta bron bo'lmasidan oldin",
        lines=[
            dict(text="Kompaniya, keyin Sozlamalar. Bu sahifa biznesingiz qanday ishlashini belgilaydi. "
                      "Birinchi bronni olishdan oldin unga o'n daqiqa ajrating.",
                 label="Kompaniya → Sozlamalar"),
            "Yuqoridagi yorliqlar alohida sozlama sahifalari, ular faqat bitta Saqlash tugmasini bo'lishadi. "
            "Yo'l to'lovi hisoblari, GPS tizimlari va Xizmatlar keyinroq alohida qismlarda ko'riladi.",
            "Bu qator kimning sozlamalarini tahrirlayotganingizni ko'rsatadi. Bir nechta egasi bor platformada "
            "biror narsani o'zgartirishdan oldin shu qatorni o'qing.",
            dict(text="Kompaniya va domen. Bu yerdagi nomni ijarachilar do'koningizda ko'radi, domen esa do'kon "
                      "ochiladigan veb-manzil.",
                 label="Kompaniya va domen"),
            dict(text=".myezwheels.com oldida turadigan qismni yozing va Domen yaratish tugmasini bosing. "
                      "Domensiz avtomobillaringizni joylashtiradigan joy bo'lmaydi.",
                 say="nuqta my e z wheels nuqta com oldida turadigan qismni yozing va Domen yaratish tugmasini bosing. "
                     "Domensiz avtomobillaringizni joylashtiradigan joy bo'lmaydi."),
            dict(text="Uning ostida Konfiguratsiya. Minimal xavfsizlik depoziti: depoziti bundan past qo'yilgan "
                      "har qanday avtomobilniki avtomatik shu miqdorga ko'tariladi.",
                 label="Konfiguratsiya"),
            "Shubhali GPS yo‘l haqlarini yechish. Standart bo'yicha o'chiq, shunday qoldirgan ma'qul: u ishonchliligi "
            "past, faqat GPS bo'yicha topilgan yo'l to'lovlarini yechish yoki yechmaslikni hal qiladi. Bular yonida "
            "bepul yo'lak bor gantrilar, ular xato mos kelishi mumkin.",
            "Rad etilgan yo‘l haqi to‘lovlarini qayta urinish. Bu ham standart bo'yicha o'chiq. Yoqilsa, vaqtinchalik "
            "sabab bilan rad etilgan karta keyingi kunlarda qayta uriniladi. O'chiq bo'lsa, yo'l to'lovi muvaffaqiyatsiz "
            "bo'lib qoladi va uni o'zingiz hal qilasiz. Har holda ijarachi kartani tuzatish uchun havola oladi.",
            "Tozalash to'lovi va Chekish to'lovi ularning yonida, o'ngda esa Minimal band qilish kunlari. Uchalasi ham "
            "qoida emas, standart qiymat: avtomobilning o'z qiymati bo'lishi mumkin.",
            dict(text="Eng ko'p vaqt tejaydigan blok mana shu. Narxlash davri, sug'urta, haftalik narx, ranglar — "
                      "qo'shgan har bir yangi avtomobilingizda bular allaqachon to'ldirilgan bo'ladi.",
                 label="Yangi avtomobillar uchun standartlar"),
            dict(text="Pastroqda Email yo'naltirish. Siz mail.myeztoll.com da ommaviy taxallus ro'yxatdan o'tkazasiz, "
                      "unga yuborilgan hamma narsa haqiqiy manzilingizga yo'naltiriladi.",
                 say="Pastroqda Email yo'naltirish. Siz mail nuqta my e z toll nuqta com da ommaviy taxallus ro'yxatdan "
                     "o'tkazasiz, unga yuborilgan hamma narsa haqiqiy manzilingizga yo'naltiriladi.",
                 label="Email yo'naltirish"),
            "Siz yuborgan javoblar taxallus orqali chiqadi, shuning uchun haydovchi haqiqiy email manzilingizni "
            "hech qachon bilmaydi.",
            "Bitta kalit butun yo'naltirishni o'chiradi. Shunda kiruvchi xatlar yo'naltirilmay, qaytarib yuboriladi.",
            dict(text="Keyin yuqori o'ngdagi Saqlash. Saqlanmagan o'zgarishlar bilan sahifadan chiqsangiz, avval "
                      "so'raladi — lekin Saqlash tugmasini bosish osonroq.",
                 label="Saqlash"),
        ]),

    # ------------------------------------------------------------------------------------------ 3
    3: dict(
        title="Yo'l to'lovi agentliklarini ulash",
        sub="Tizim yo'l to'lovlarini sizsiz yig'ishi uchun kerak bo'lgan kirish ma'lumotlari",
        lines=[
            dict(text="Kompaniya, Sozlamalar va Yo'l to'lovi hisoblari yorlig'i. Bu yerda tizimga yo'l to'lovlaringizni "
                      "yig'ish uchun kerakli loginlarni berasiz.",
                 label="Sozlamalar → Yo'l to'lovi hisoblari"),
            "Avval u nima qilishini tushunib oling. U har bir agentlik portaliga siz nomingizdan, jadval bo'yicha kiradi "
            "va avtomobillaringiz yig'gan yo'l to'lovlarini yuklab oladi. Hech qanday ma'lumot oqimi yoki API yo'q — "
            "bu siz o'zingiz ochadigan o'sha sayt.",
            dict(text="Yuqoridagi Yo‘l haqi tarmoqlari qamrovi har bir tarmoq uchun bitta nishon ko'rsatadi, kirish "
                      "ma'lumotlari bor bo'lsa, unda belgi qo'yilgan. Bitta E-ZPass hisobi o'n sakkizdan ortiq E-ZPass "
                      "agentligining hammasini qamraydi — har bir shtat uchun alohida ochmang.",
                 label="Yo‘l haqi tarmoqlari qamrovi"),
            "Qo'shish uchun Hisob qo‘shish tugmasini bosing.",
            dict(text="Provayderni tanlang. Bitta agentlikda bir nechta hisobingiz bo'lsa, unga nom bering. "
                      "Nom faqat siz uchun.",
                 label="Yo‘l haqi hisobini qo‘shish"),
            "Hisob raqami, login, parol — aynan agentlik saytida ishlatadiganlaringiz. Hisob raqami ixtiyoriy, "
            "ba'zi agentliklar uni ishlatmaydi.",
            "Parol shifrlangan holda saqlanadi va hech qachon sizga ham, qo'llab-quvvatlash xizmatiga ham ochiq "
            "matnda ko'rsatilmaydi.",
            "Saqlang, hisob karta bo'lib paydo bo'ladi.",
            dict(text="Har bir kartaning o'ng tomonida kichik belgilar qatori bor. Ulardan ikkitasini siz haqiqatan "
                      "ishlatasiz.",
                 label="Har bir hisobga bitta karta"),
            dict(text="Chaqmoq — bu Ulanishni tekshirish. Uni hozir, shu yerda o'tirganingizda bosing. Uch haftadan "
                      "keyin hech narsa yig'ilmaganini bilib qolmang.",
                 label="Ulanishni tekshirish"),
            dict(text="Qalqon — bu Qurilmani tasdiqlash. Tizim yangi kompyuterdan birinchi marta kirganda, ko'p "
                      "agentliklar email orqali kod yuboradi. Qalqonni bosib kodni kiriting, shunda yig'ish sizsiz "
                      "davom etadi.",
                 label="Qurilmani tasdiqlash"),
            "Har bir kartaning chap tomonidagi kichik vilka shu agentlik bilan ishlaydigan dastur serverda "
            "o'rnatilganmi, shuni ko'rsatadi. Yashil — yuklangan. Qizil — yo'q, bu sizning emas, qo'llab-quvvatlash "
            "xizmatining ishi.",
            dict(text="Hisoblar ulangach, yo'l to'lovlari o'zi kela boshlaydi. Keyingi qism: avtomobillaringizni "
                      "tizimga kiritish, shunda bu to'lovlar biror narsaga bog'lanadi.",
                 label=" "),
        ]),

    # ------------------------------------------------------------------------------------------ 4
    4: dict(
        title="Avtomobillar ro'yxati",
        sub="Uni o'qish, filtrlash va har bir qatordagi yashirin menyu",
        lines=[
            dict(text="Transport vositalari, keyin Barcha avtomobillar. Qaysi yo'l bilan kelgan bo'lmasin, har bir "
                      "avtomobilingiz shu sahifada.",
                 label="Transport vositalari → Barcha avtomobillar"),
            "Yuqorida beshta tugma. Import qilish jadval faylni oladi, Avtomobil qo'shish bitta mashinani qo'lda "
            "qo'shadi, Tafsilotlarni ko'rsatish jadvalni kengaytiradi, Yangilash uni qayta o'qiydi, Provayderlarni "
            "biriktirish esa bir nechta avtomobilga yo'l to'lovi agentliklarini birdaniga biriktiradi.",
            dict(text="Ularning ostida filtrlar. Tur, holat, yo'l to'lovi sozlamasi va qidiruv maydoni. U davlat raqami, "
                      "ism, email yoki tur bo'yicha topadi — qaysi ekanini aytish shart emas. Yo'l to'lovi sozlamasini "
                      "eslab qoling: u ro'yxatni agentlikka ulangan yoki ulanmagan mashinalarga toraytiradi.",
                 label="Filtrlar"),
            dict(text="Endi jadvalning o'zi. Davlat raqami va Sarlavha yonida qizil yulduzcha bor, demak ular majburiy: "
                      "davlat raqami avtomobilni mahsulotning boshqa hamma joyida aniqlaydi.",
                 label="Ustunlar"),
            dict(text="Band qilish holati mashina faol bronda ekanini ko'rsatadi. To'lov holatini ko'zdan kechiring: "
                      "«Yoʻl haqi yoʻq» — yaxshi, «Muvaffaqiyatsiz» — karta o'tmagan, «Bron to'lovi qotib qoldi» esa "
                      "bugunoq ko'rib chiqishni talab qiladi.",
                 label="To'lov holati"),
            "Har bir qatorning chap tomonida belgilar qatori: xarita, diagnostika, kalendar va ma'lumot. "
            "Trekeri yo'q avtomobilda ular kamroq bo'ladi.",
            "Uch nuqta esa asosiy ishni bajaradigan menyuni ochadi.",
            dict(text="Band qilish shu mashinaga bron boshlaydi. Band qilishlarni ko'rish uning mavjud bronlarini "
                      "ko'rsatadi. Barcha EZ yo'l to'lovlari u yig'gan har bir yo'l to'lovini sanab beradi.",
                 label="Qator menyusi"),
            "Sayohat u qayerda bo'lganini chizadi, Diagnostika trekerni o'qiydi, Tahrirlash esa to'liq avtomobil "
            "formasini ochadi. Olti amal, istalgan qatordan bir bosishda.",
            dict(text="Pastda soni va sahifalash. Standart bo'yicha sahifada o'nta qator — buni shu yerda o'zgartiring, "
                      "aks holda qirqta mashina to'rt sahifa aylantirish degani.",
                 label="Sahifalash"),
        ]),

    # ------------------------------------------------------------------------------------------ 5
    5: dict(
        title="Avtoparkingizni kiritish",
        sub="Jadval fayl, qo'lda bitta mashina yoki to'g'ridan-to'g'ri agentlikdan",
        lines=[
            dict(text="Avtomobillarni tizimga kiritishning bir necha yo'li bor. Eng tezi ro'yxatingiz hozir qayerda "
                      "turganiga bog'liq.",
                 label="Kiritishning besh yo'li"),
            "HQ Rental, Renteon, RENTALL yoki TSD kabi bron platformasidan foydalansangiz, avtoparkni o'sha yerdan "
            "torting — u bronlari bilan keladi. Yo'l to'lovi agentligi mashinalaringizni allaqachon bilsa, ularni "
            "agentlikdan yarating, transponder bog'lanishi o'zi keladi.",
            "Agar sizda jadval fayl bo'lsa, Import qilish tugmasini bosing.",
            dict(text="Faylni tashlang. CSV, xlsx va xls ishlaydi, ustunlar siz uchun moslanadi — hech narsani qo'lda "
                      "bog'lash so'ralmaydi.",
                 label="Avtomobillarni import qilish"),
            "Ikki ustun majburiy: davlat raqami va raqam shtati. Ikkalasi birga avtomobilni agentlikka tanitadi. "
            "Shtati yo'q faylni keyin bitta amal bilan to'ldirish mumkin.",
            "Bir-ikkita mashina uchun qo'lda tezroq. Avtomobil qo'shish.",
            dict(text="Uchta yorliq: Asosiy ma'lumot, Narxlash, Joylashuv. Istalganidan saqlashingiz mumkin, qolgan "
                      "ikkitasini keyin to'ldirasiz.",
                 label="Yangi transport vositasini qo'shish"),
            "Sarlavha va Tavsifni ijarachi o'qiydi. Sarlavha majburiy, bu mashina boshqa har bir ekranda shu nom "
            "bilan ko'rinadi.",
            dict(text="Ikki belgilash katagi u umuman ko'rinadimi, shuni hal qiladi. E'lonni nashr etish uni "
                      "do'koningizga qo'yadi, My E-Z Wheels’da ko‘rsatish esa umumiy bozorga qo'shadi.",
                 label="Qayerda e'lon qilinadi"),
            dict(text="Yo'l to'lovi tizimlari qatori bu mashinaga umuman hisob qo'yish mumkinmi, shuni hal qiladi. "
                      "Qo'shish unga agentlik biriktiradi. Bu yerdagi bo'sh ro'yxat — yo'l to'lovi undiradigan odamsiz "
                      "kelishining eng ko'p sababi.",
                 label="Yo'l to'lovi tizimlari"),
            dict(text="Keyin Transport ma'lumotlari. Tur, mamlakat, marka, model, yil, ranglar — ularning ko'pi ikkinchi "
                      "qismda o'rnatgan standartlaringizdan allaqachon to'ldirilgan.",
                 label="Transport ma'lumotlari"),
            "Davlat raqami va Raqam shtati. Bu ikkisi formadagi hamma narsadan muhimroq: shtat noto'g'ri bo'lsa, "
            "agentlik bu mashinani hech qachon topa olmaydi.",
            "VIN va GPS treker IMEI ixtiyoriy. Lekin IMEI trekerni shu mashinaga bog'laydi, treker esa tizimga "
            "agentlik sizga hisoblamagan yo'l to'lovini topish imkonini beradi.",
            dict(text="Transportni saqlash. Bitta mashina kiritildi. Keyingi qism: odamlar o'tkazib yuboradigan, keyin "
                      "pulim qayerga ketdi deb bir oy o'ylab yuradigan qadam.",
                 label="Transportni saqlash"),
        ]),

    # ------------------------------------------------------------------------------------------ 6
    6: dict(
        title="Transponderlar — o'tkazib yuborib bo'lmaydigan qadam",
        sub="Orqasida avtomobil bo'lmagan tegni hech kimga hisoblab bo'lmaydi",
        lines=[
            dict(text="Yo'l to'lovlari va qoidabuzarliklardan yo'l to'lovi hisobini oching, uning alohida sahifasi "
                      "ochiladi: agentlikda siz uchun turgan har bir avtomobil va har bir transponder.",
                 label="Yo'l to'lovi provayderi hisobi"),
            "Ikki yorliq. Transport vositalari — agentlik fikricha sizniki bo'lgan mashinalar. Transponderlar — u bergan "
            "teglar. Sonlari kamdan-kam mos keladi, bu qism ana shu farq haqida.",
            "Nega bu muhim: yo'l to'lovi kim haydagan bo'lsa, o'shanga hisoblanadi. Agentlik teg gantridan o'tganini "
            "aytadi. Faqat teg va avtomobil bog'lanishi buni mashinaga aylantiradi, faqat mashinada bron bor, "
            "faqat bronda kartasi bor haydovchi bor.",
            dict(text="Shuning uchun bu izoh sahifadagi eng foydali qator. Ulangan — tayyor. DB da transponder yo'q — "
                      "agentlik mashinani biladi, lekin bizda uning tegi yo'q. Transponder DB dan farq qiladi — ikkisi "
                      "mos emas, biri eskirgan.",
                 label="Beshta holat"),
            "Provayder tayinlanmagan — mashina bu yerda bor, lekin unga agentlik biriktirilmagan. Bu beshinchi qismdagi "
            "Yo'l to'lovi tizimlari qatori. DB da yo'q — agentlikda biz hech eshitmagan avtomobil bor.",
            dict(text="Holat ustuni buni har bir qatorda takrorlaydi. Ro'yxat bo'ylab pastga tushib, aynan qaysi "
                      "mashinalar sizga hech narsa keltirmayotganini ko'rasiz.",
                 label="Holat, har bir avtomobil uchun"),
            dict(text="O'ngdagi Transponder ustuni esa javob: to'ldirilgan bo'lsa, mashinaga hisob qo'yish mumkin. "
                      "Bo'sh bo'lsa, undan kelgan yo'l to'lovini undiradigan odam yo'q va u sizga tushadi.",
                 label="Transponder"),
            dict(text="Endi tuzoq. Bu banner transponderlar ro'yxati keshdan olinganini aytadi va agentlikdan oxirgi "
                      "marta qachon o'qilganini ko'rsatadi.",
                 label="Ro'yxat keshdan olingan"),
            "Agentlik o'sha vaqtdan keyin bergan teg bu ro'yxatda shunchaki yo'q. Transponder borligiga amin "
            "bo'lsangiz-u, bu yerda topolmasangiz, ro'yxat eski — teg yo'qolmagan.",
            dict(text="Avtomobillar va transponderlar ro‘yxatini yangilash agentlikka qaytib, uni qayta o'qiydi. "
                      "Biror narsa noto'g'ri deb xulosa qilishdan oldin uni bosing.",
                 label="Yangilash"),
            "Bu biroz vaqt oladi va u buni aytadi — avval avtomobillarni yuklaydi, keyin ularning ortidan "
            "transponderlarning butun ro'yxatini ko'rib chiqadi.",
            dict(text="Buni har bir yo'l to'lovi hisobi uchun birinchi kuningizda bir marta qiling, agentlik yangi teg "
                      "yuborganda yana qiling. O'tkazib yuborsangiz, yo'l to'lovlari baribir keladi — faqat haydovchiga "
                      "emas, sizga yozilib keladi.",
                 label=" "),
        ]),

    # ------------------------------------------------------------------------------------------ 7
    7: dict(
        title="Tariflar va narx mavsumlari",
        sub="Butun toifaga birdaniga narx qo'ying, keyin gavjum haftalarga boshqacha narx",
        lines=[
            dict(text="Transport vositalari, keyin Tariflar. Bu sahifa birorta avtomobilni ochmasdan avtoparkingizga "
                      "narx qo'yadi.",
                 label="Transport vositalari → Tariflar"),
            dict(text="Avval qaysi tarifni o'rnatayotganingizni tanlang: Kunlik, Haftalik yoki Oylik. Bular uchta alohida "
                      "narx, almashtirgich sahifadagi har bir raqamni o'zgartiradi.",
                 label="Kunlik · Haftalik · Oylik"),
            "Ostidagi ro'yxat — toifalar bo'yicha guruhlangan avtoparkingiz: Economic, Luxury, Premium, Sports, SUV. "
            "Har bir guruh markalar, modellar va oxirida alohida mashinalarga ochiladi.",
            dict(text="Maydondan oldin raqamni o'qing. Raqam bo'lsa, guruhdagi har bir mashina allaqachon shu narxda. "
                      "«har xil» so'zi esa narxlar turlicha degani, bu yerga qiymat kiritsangiz, hammasi ustidan yoziladi.",
                 label="«har xil» — ogohlantirish"),
            "Yangi tarifni yozing va Qo‘llash tugmasini bosing — u shu sarlavha ostidagi har bir mashinaga "
            "birdaniga yoziladi.",
            "Faqat bitta modelni nazarda tutgan bo'lsangiz, avval guruhni oching. Toifa tepasida qo'llash tez, "
            "lekin u tegmoqchi bo'lmagan mashinangiz narxini o'zgartirishning ham eng tez yo'li.",
            dict(text="Keyin Narx mavsumlari. Bu o'sha g'oya, faqat sanalar oralig'ida.",
                 label="Narx mavsumlari"),
            "Mavsum — bu nom, boshlanish, tugash va ustuvorlik. Ikki mavsum ustma-ust tushsa, ustuvorligi yuqorisi "
            "yutadi. Bayram haftasi shunday qilib yozgi mavsum ichida turib, qimmatroq narx oladi.",
            "Mavsum qoʻshish — va u shu jadvalda paydo bo'ladi.",
            dict(text="Keyin bu yerda mavsumni tanlang va unga asosiy tariflar kabi narx qo'ying: toifa, marka, "
                      "model bo'yicha yoki bitta mashinaga.",
                 label="Mashina mavsumiy narxlari"),
            "Pastdagi qoidani ikki marta o'qing: darajani bo'sh qoldirsangiz, o'sha davr uchun mashinaning asosiy "
            "narxi olinadi. Bo'sh — nol degani emas.",
            dict(text="Qaysi mavsum qo'llanishini bron qilingan kun emas, ijara boshlanish sanasi hal qiladi. "
                      "Aprelda avgust uchun olingan bron avgust narxida hisoblanadi.",
                 label=" "),
        ]),

    # ------------------------------------------------------------------------------------------ 8
    8: dict(
        title="Bronlar ekrani",
        sub="Bir xil bronlarning ikki ko'rinishi va har bir qatorda o'nta amal",
        lines=[
            dict(text="Bronlar. Barcha bronlaringiz, bitta ro'yxatda.", label="Bronlar"),
            dict(text="Holat filtrida hammasi emas, sakkizta holat tanlangan. Bor ekanini bilgan broningiz bu sahifada "
                      "bo'lmasa, biror xulosaga kelishdan oldin shu filtrni oching.",
                 label="Holatlarning sakkiztasi"),
            "Ikki yorliq: Roʻyxat va Rejalashtirgich. Bir xil bronlar, ikki xil ko'rinishda.",
            dict(text="Ro'yxatda butun voqeani uchta ustun aytadi. Ijara shartnomasi shartnoma imzolangan, yuborilgan "
                      "yoki kerak emasligini ko'rsatadi.",
                 label="Ijara shartnomasi"),
            dict(text="Holat — bronning o'z holati: Tasdiqlangan, Bajarildi, Muddatidan oldin yakunlangan, "
                      "Karta kutilmoqda.",
                 label="Holat"),
            dict(text="Yoʻl haqi toʻlovlari esa pul: Muvaffaqiyatli, Muvaffaqiyatsiz, Yechib olinmagan, To‘lov qotib "
                      "qoldi. Har kuni ertalab shu ustunni ko'zdan kechiring.",
                 label="Yoʻl haqi toʻlovlari"),
            "Mana bunday qator buni ochiq aytadi: karta kutilmoqda, hech narsa yechilmagan va bitta shart hali "
            "bajarilmagan. U tuzatilmaguncha bu bron bo'yicha hech qanday pul yig'ilmaydi.",
            "Qatordagi uch nuqta shu bron bilan qila oladigan hamma narsani ochadi.",
            dict(text="Menyu tepasida bronning o'zi yozilgan — kim, qaysi mashina, sanalar, holat — shuning uchun "
                      "hech qachon noto'g'ri qatorda amal bajarmaysiz.",
                 label="Qator menyusi"),
            "Avtomobilni almashtirish bronni boshqa mashinaga o'tkazadi. Bronni qayta ochish tugagan bronni qaytaradi. "
            "Ikkalasi ham yo'l to'lovlarini o'zi bilan ko'chiradi, shuning uchun ehtiyot bo'lib ishlating.",
            "Hisob-kitoblar, Bron ma'lumotlari, Yo'l to'lovlarini ko'rish va Jarimalarni ko'rish faqat o'qish uchun — "
            "bu bronga nima hisoblangan va nima uchun.",
            dict(text="Hisob-faktura yaratish bu brondagi to'lanmagan yo'l to'lovlarini haydovchi uchun bitta "
                      "hisob-fakturaga aylantiradi. Karta yo'q, lekin yo'l to'lovlari bor bo'lganda shu vosita kerak.",
                 label="Hisob-faktura yaratish"),
            "Bron uchun to‘lov hozir pul yechadi. Ijara shartnomasi shartnomani yuboradi yoki qayta yuboradi. "
            "O'nta amal, hech biri boshqa ekranni talab qilmaydi.",
            dict(text="Rejalashtirgich — o'sha bronlar vaqt bo'yicha chizilgan: har bir avtomobilga bitta qator, "
                      "har bir bronga bitta chiziq.",
                 label="Rejalashtirgich"),
            "Qizil chiziq — bugun. Qatordagi bo'sh joy — turib qolgan mashina, o'ng chetdan chiqib ketgan chiziq esa "
            "hali tugamagan bron.",
            "Pastdagi ranglar ro'yxatdagi o'sha holatlar. Qaysi ko'rinishni tanlamang, o'sha to'rt so'zni o'qiysiz.",
        ]),
}
