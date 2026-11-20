# -*- coding: utf-8 -*-
"""Episode 58 in the pilot languages: tr, uk, uz, ka, hy, fa, ur.

One entry per beat of series_u.EP58, in the same order. A string is the subtitle and the narration; a dict
adds 'say' (what the voice reads, when the subtitle has digits the voice should say as words) and 'label'
(the caption of a beat that names its own in English). Button and menu names are the portal's own, taken
from aegis-owner-web origin/main src/locales/<lang>/common.json (liabilityTransfer.*,
ownerViolations.transferToRenter / transferredToRenter, violationNotice.addButton / batch.addButton,
nav.sections.tollProviders, nav.violations).
"""

LANGS = {}

# ----------------------------------------------------------------------------------------------- tr
LANGS['tr'] = dict(
    title='Bir geçiş bildirimini veya cezayı kiracıya devredin',
    sub='Portal kuruma mektubu yazar — siz imzalayıp gönderirsiniz, kiracının kartından tahsil edilmez',
    lines=[
        dict(text='ABD\'nin birçok eyaletinde geçiş ücreti bildirimi veya ceza kiracıya devredilebilir. '
                  'Kuruma, kiracının bilgileriyle imzalı bir mektup gönderirsiniz.', label='Kiracıya devret'),
        'Portal bu mektubu sizin için hazırlar. 30 eyaletteki yaklaşık 60 kurumun kurallarını bilir.',
        'Geçiş ücretleri ve ihlaller, ardından İhlaller bölümünü açın. Satır menüsünü açın ya da satıra sağ '
        'tıklayın ve Kiracıya devret\'e basın. Bu seçenek yalnızca bildirim bir kiralamaya bağlıysa görünür.',
        dict(text='En üstte kiracı ve imzalı sözleşmesinin olup olmadığı yazar.', label='Kurum kuralı'),
        'Kurum kuralı alanında en uygun kural zaten seçilidir. Listeden başka birini seçebilirsiniz.',
        'Altında: devre izin veren yasa ve son gönderim tarihi.',
        'Sonra bu kurumun adımları ve noter huzurunda mı, yoksa sadece sizin imzanızla mı imzalanacağı.',
        'Ve nereye gönderileceği: posta adresi, faks ya da bir web sitesi.',
        dict(text='Kiracının adresi veya imzalı sözleşme gibi bir şey eksikse, burada kırmızıyla yazılır. '
                  'Önce onu ekleyin, sonra geri dönün.', label='Eksik bir şey mi var?'),
        dict(text='İmzalayanın adını ve unvanını yazın, sonra Paketi indir\'e basın.', label='Paketi indir'),
        dict(text='PDF olarak bir mektup alırsınız: şirketiniz, kurumun adresi, bildirim ve yasa.', label='Mektup'),
        'Sonra kiracının adı ve adresi, ve imzanız için bir yer. İmzalı kira sözleşmesi kayıtlıysa, sona eklenir.',
        dict(text='Mektubu imzalayın ve kuruma kendiniz gönderin.', label='İmzalayın ve gönderin'),
        'Göndermeden önce fikrinizi mi değiştirdiniz? Devri iptal et\'e basın.',
        dict(text='Gönderdikten sonra nasıl gönderdiğinizi seçin, takip numarasını ekleyin ve Gönderildi olarak '
                  'işaretle\'ye basın.', label='Gönderildi olarak işaretle'),
        'Bundan sonra bu bildirim kiracının kartından tahsil edilmez. Yeniden deneme, hatırlatma ve tahsilat '
        'ajansı yok.',
        dict(text='Listede bildirim artık Kiracıya devredildi olarak görünür.', label='Kiracıya devredildi'),
        dict(text='Kurum yanıt verdiğinde Kurum kabul etti ya da Kurum reddetti\'ye basın.', label='Kurumun yanıtı'),
        'Reddedildiyse, kiracıdan yine normal şekilde tahsilat yapılır.',
        dict(text='Bir yol daha var. Postayla gelen cezayı ekle bir cezayı bir kiralamaya kaydettiğinde, pencere '
                  'hemen Kiracıya devret\'i sunar.', label='Postayla gelen cezadan'),
        'Birden çok ceza ekle\'de, bir kiralamaya kaydedilen her satırda aynı bağlantı vardır.',
    ])

# ----------------------------------------------------------------------------------------------- uk
LANGS['uk'] = dict(
    title='Передайте повідомлення про проїзд або штраф орендарю',
    sub='Портал пише лист до органу — ви підписуєте й надсилаєте, а з картки орендаря не списують',
    lines=[
        dict(text='У багатьох штатах США повідомлення про оплату проїзду або штраф можна передати орендарю. '
                  'Ви надсилаєте органу підписаний лист із даними орендаря.', label='Передати орендарю'),
        'Портал готує цей лист за вас. Він знає правила приблизно 60 органів у 30 штатах.',
        'Відкрийте Плата за проїзд і порушення, потім Порушення. Відкрийте меню рядка або клацніть рядок правою '
        'кнопкою і натисніть Передати орендарю. Цей пункт є лише тоді, коли повідомлення прив’язане до оренди.',
        dict(text='Угорі: орендар і чи є його підписаний договір.', label='Правило органу'),
        'У полі Правило органу вже вибрано найкращий варіант. Можна вибрати інший зі списку.',
        'Нижче: закон, який це дозволяє, і дата, до якої треба надіслати.',
        'Далі кроки для цього органу і чи треба підписувати в нотаріуса, чи досить вашого підпису.',
        'І куди надіслати: поштова адреса, факс або вебсайт.',
        dict(text='Якщо чогось бракує, наприклад адреси орендаря чи підписаного договору, це видно тут червоним. '
                  'Спершу додайте це, потім поверніться.', label='Чогось бракує?'),
        dict(text='Впишіть, хто підписує, і його посаду, потім натисніть Завантажити пакет.', label='Завантажити пакет'),
        dict(text='Ви отримуєте лист у PDF: ваша компанія, адреса органу, повідомлення і закон.', label='Лист'),
        'Далі ім’я та адреса орендаря і місце для вашого підпису. Якщо підписаний договір оренди збережено, його '
        'додано в кінці.',
        dict(text='Підпишіть лист і самі надішліть його до органу.', label='Підпишіть і надішліть'),
        'Передумали до надсилання? Натисніть Скасувати передачу.',
        dict(text='Коли надіслали, виберіть, як саме, додайте номер відстеження і натисніть Позначити як надіслане.',
             label='Позначити як надіслане'),
        'Відтепер це повідомлення не списують з картки орендаря. Ні повторних спроб, ні нагадувань, ні колекторів.',
        dict(text='У списку повідомлення тепер має позначку Передано орендарю.', label='Передано орендарю'),
        dict(text='Коли орган відповість, натисніть Орган прийняв або Орган відмовив.', label='Відповідь органу'),
        'Якщо орган відмовив, орендар знову сплачує як зазвичай.',
        dict(text='Є ще один шлях. Коли Додати квитанцію зберігає штраф в оренду, вікно одразу пропонує Передати '
                  'орендарю.', label='З квитанції з листа'),
        'У Додати пачку квитанцій кожен збережений рядок з орендою має те саме посилання.',
    ])

# ----------------------------------------------------------------------------------------------- uz
LANGS['uz'] = dict(
    title="Yo'l to'lovi bildirishnomasi yoki jarimani ijarachiga o'tkazing",
    sub="Portal organga xat yozadi — siz imzolab yuborasiz, ijarachining kartasidan pul yechilmaydi",
    lines=[
        dict(text="AQShning ko'p shtatlarida yo'l to'lovi bildirishnomasi yoki jarimani ijarachiga o'tkazish "
                  "mumkin. Siz organga ijarachi ma'lumotlari yozilgan imzoli xat yuborasiz.",
             label="Ijarachiga o'tkazish"),
        "Portal bu xatni siz uchun tayyorlaydi. U 30 shtatdagi taxminan 60 organning qoidalarini biladi.",
        "Yo'l to'lovlari va qoidabuzarliklar, keyin Qoidabuzarliklar bo'limini oching. Qator menyusini oching yoki "
        "qatorni o'ng tugma bilan bosing va Ijarachiga o'tkazish tugmasini bosing. U faqat bildirishnoma ijaraga "
        "bog'langan bo'lsa chiqadi.",
        dict(text="Yuqorida: ijarachi va uning imzolangan shartnomasi bor-yo'qligi.", label="Organ qoidasi"),
        "Organ qoidasi maydonida eng mos qoida allaqachon tanlangan. Ro'yxatdan boshqasini tanlashingiz mumkin.",
        "Uning ostida: bunga ruxsat beruvchi qonun va yuborish muddati.",
        "Keyin shu organ uchun qadamlar, va notarius huzurida imzolash kerakmi yoki oddiy imzo yetarlimi.",
        "Va qayerga yuborish: pochta manzili, faks yoki veb-sayt.",
        dict(text="Agar biror narsa yetishmasa, masalan ijarachining manzili yoki imzolangan shartnoma, bu yerda "
                  "qizil rangda ko'rsatiladi. Avval uni qo'shing, keyin qayting.",
             label="Nimadir yetishmayaptimi?"),
        dict(text="Kim imzolashini va lavozimini yozing, keyin Paketni yuklab olish tugmasini bosing.",
             label="Paketni yuklab olish"),
        dict(text="Siz PDF xat olasiz: kompaniyangiz, organ manzili, bildirishnoma va qonun.", label="Xat"),
        "Keyin ijarachining ismi va manzili, hamda imzo uchun joy. Imzolangan ijara shartnomasi saqlangan bo'lsa, "
        "u oxiriga qo'shiladi.",
        dict(text="Xatni imzolang va organga o'zingiz yuboring.", label="Imzolang va yuboring"),
        "Yuborishdan oldin fikringiz o'zgardimi? O'tkazishni bekor qilish tugmasini bosing.",
        dict(text="Yuborganingizdan keyin qanday yuborganingizni tanlang, kuzatuv raqamini qo'shing va Yuborilgan "
                  "deb belgilash tugmasini bosing.", label="Yuborilgan deb belgilash"),
        "Endi bu bildirishnoma uchun ijarachining kartasidan pul yechilmaydi. Qayta urinish ham, eslatma ham, "
        "undiruv agentligi ham yo'q.",
        dict(text="Ro'yxatda bildirishnoma endi Ijarachiga o'tkazildi deb ko'rinadi.", label="Ijarachiga o'tkazildi"),
        dict(text="Organ javob berganda Organ qabul qildi yoki Organ rad etdi tugmasini bosing.", label="Organ javobi"),
        "Agar rad etilgan bo'lsa, ijarachidan odatdagidek undiriladi.",
        dict(text="Yana bir yo'l bor. Pochtadagi jarimani qo‘shish jarimani ijaraga saqlaganda, oyna darhol "
                  "Ijarachiga o'tkazish tugmasini taklif qiladi.", label="Pochtadagi jarimadan"),
        "Bir nechta jarima qo‘shish oynasida ijaraga saqlangan har bir qatorda xuddi shu havola bor.",
    ])

# ----------------------------------------------------------------------------------------------- ka
LANGS['ka'] = dict(
    title='გზის საფასურის შეტყობინების ან ჯარიმის მოიჯარეზე გადაცემა',
    sub='პორტალი წერს წერილს ორგანოსთვის — თქვენ ხელს აწერთ და აგზავნით, მოიჯარის ბარათიდან თანხა არ ჩამოიჭრება',
    lines=[
        dict(text='აშშ-ის ბევრ შტატში გზის საფასურის შეტყობინება ან ჯარიმა შეიძლება მოიჯარეს გადაეცეს. '
                  'თქვენ ორგანოს უგზავნით ხელმოწერილ წერილს მოიჯარის მონაცემებით.', label='მოიჯარეზე გადაცემა'),
        'პორტალი ამ წერილს თქვენთვის ამზადებს. მან იცის დაახლოებით 60 ორგანოს წესები 30 შტატში.',
        'გახსენით გზის საფასური და დარღვევები, შემდეგ დარღვევები. გახსენით სტრიქონის მენიუ ან სტრიქონზე '
        'დააჭირეთ მარჯვენა ღილაკს და აირჩიეთ მოიჯარეზე გადაცემა. ის მხოლოდ მაშინ ჩანს, როცა შეტყობინება '
        'ქირასთან არის მიბმული.',
        dict(text='ზემოთ: მოიჯარე და აქვს თუ არა მას ხელმოწერილი ხელშეკრულება.', label='ორგანოს წესი'),
        'ველში ორგანოს წესი უკვე არჩეულია ყველაზე შესაფერისი. სიიდან სხვაც შეგიძლიათ აირჩიოთ.',
        'ქვემოთ: კანონი, რომელიც ამის უფლებას იძლევა, და თარიღი, რომლამდეც უნდა გაგზავნოთ.',
        'შემდეგ ამ ორგანოს ნაბიჯები და ის, საჭიროა თუ არა ნოტარიუსთან ხელმოწერა, თუ თქვენი ხელმოწერა საკმარისია.',
        'და სად გაიგზავნოს: საფოსტო მისამართი, ფაქსი ან ვებსაიტი.',
        dict(text='თუ რამე აკლია, მაგალითად მოიჯარის მისამართი ან ხელმოწერილი ხელშეკრულება, აქ წითლად ჩანს. '
                  'ჯერ ის დაამატეთ, მერე დაბრუნდით.', label='რამე აკლია?'),
        dict(text='ჩაწერეთ, ვინ აწერს ხელს და მისი თანამდებობა, შემდეგ დააჭირეთ ღილაკს პაკეტის ჩამოტვირთვა.',
             label='პაკეტის ჩამოტვირთვა'),
        dict(text='მიიღებთ წერილს PDF-ად: თქვენი კომპანია, ორგანოს მისამართი, შეტყობინება და კანონი.', label='წერილი'),
        'შემდეგ მოიჯარის სახელი და მისამართი და ადგილი თქვენი ხელმოწერისთვის. თუ ხელმოწერილი ხელშეკრულება '
        'შენახულია, ის ბოლოში ემატება.',
        dict(text='მოაწერეთ ხელი და თავად გაუგზავნეთ ორგანოს.', label='ხელი მოაწერეთ და გაგზავნეთ'),
        'გაგზავნამდე გადაიფიქრეთ? დააჭირეთ ღილაკს გადაცემის გაუქმება.',
        dict(text='გაგზავნის შემდეგ აირჩიეთ, როგორ გაგზავნეთ, დაამატეთ თვალთვალის ნომერი და დააჭირეთ ღილაკს '
                  'გაგზავნილად მონიშვნა.', label='გაგზავნილად მონიშვნა'),
        'ამიერიდან ამ შეტყობინებისთვის მოიჯარის ბარათიდან თანხა არ ჩამოიჭრება. არც განმეორებითი ცდა, არც '
        'შეხსენება, არც ვალების ამოღების სააგენტო.',
        dict(text='სიაში შეტყობინებას ახლა აწერია: გადაეცა მოიჯარეს.', label='გადაეცა მოიჯარეს'),
        dict(text='როცა ორგანო გიპასუხებთ, დააჭირეთ ღილაკს ორგანომ მიიღო ან ორგანომ უარყო.', label='ორგანოს პასუხი'),
        'თუ ორგანომ უარყო, მოიჯარეს ჩვეულებრივ ჩამოეჭრება.',
        dict(text='კიდევ ერთი გზა. როცა ფოსტით მიღებული ჯარიმის დამატება ჯარიმას ქირაზე ინახავს, ფანჯარა '
                  'მაშინვე გთავაზობთ ღილაკს მოიჯარეზე გადაცემა.', label='ფოსტით მიღებული ჯარიმიდან'),
        'ფანჯარაში რამდენიმე ჯარიმის დამატება ქირაზე შენახულ ყოველ სტრიქონს იგივე ბმული აქვს.',
    ])

# ----------------------------------------------------------------------------------------------- hy
LANGS['hy'] = dict(
    title='Փոխանցեք ճանապարհավճարի ծանուցումը կամ տուգանքը վարձակալին',
    sub='Պորտալը գրում է նամակը մարմնին — դուք ստորագրում և ուղարկում եք, վարձակալի քարտից գումար չի գանձվում',
    lines=[
        dict(text='ԱՄՆ-ի շատ նահանգներում ճանապարհավճարի ծանուցումը կամ տուգանքը կարելի է փոխանցել վարձակալին։ '
                  'Դուք մարմնին ուղարկում եք ստորագրված նամակ՝ վարձակալի տվյալներով։', label='Փոխանցել վարձակալին'),
        'Պորտալը այդ նամակը պատրաստում է ձեր փոխարեն։ Այն գիտի մոտ 60 մարմինների կանոնները 30 նահանգում։',
        'Բացեք Ճանապարհավճարներ և խախտումներ, հետո՝ Խախտումներ։ Բացեք տողի ընտրացանկը կամ աջ սեղմեք տողի վրա '
        'և սեղմեք Փոխանցել վարձակալին։ Այն երևում է միայն, երբ ծանուցումը կապված է վարձույթի հետ։',
        dict(text='Վերևում՝ վարձակալը, և արդյոք ունեք նրա ստորագրված պայմանագիրը։', label='Մարմնի կանոն'),
        'Մարմնի կանոն դաշտում արդեն ընտրված է ամենահարմարը։ Կարող եք ցանկից ընտրել մեկ ուրիշը։',
        'Դրա տակ՝ այն օրենքը, որը դա թույլ է տալիս, և ամսաթիվը, մինչև որը պետք է ուղարկել։',
        'Հետո այս մարմնի քայլերը, և արդյոք պետք է ստորագրել նոտարի ներկայությամբ, թե բավական է ձեր ստորագրությունը։',
        'Եվ ուր ուղարկել՝ փոստային հասցե, ֆաքս կամ կայք։',
        dict(text='Եթե ինչ-որ բան պակասում է, օրինակ՝ վարձակալի հասցեն կամ ստորագրված պայմանագիրը, այն նշված է '
                  'այստեղ կարմիրով։ Նախ ավելացրեք այն, հետո վերադարձեք։', label='Ինչ-որ բան պակասո՞ւմ է'),
        dict(text='Գրեք, թե ով է ստորագրում և նրա պաշտոնը, հետո սեղմեք Ներբեռնել փաթեթը։', label='Ներբեռնել փաթեթը'),
        dict(text='Դուք ստանում եք PDF նամակ՝ ձեր ընկերությունը, մարմնի հասցեն, ծանուցումը և օրենքը։', label='Նամակը'),
        'Հետո՝ վարձակալի անունն ու հասցեն և տեղ ձեր ստորագրության համար։ Եթե ստորագրված պայմանագիրը պահված է, '
        'այն ավելացվում է վերջում։',
        dict(text='Ստորագրեք և ինքներդ ուղարկեք մարմնին։', label='Ստորագրեք և ուղարկեք'),
        'Մտափոխվեցի՞ք մինչև ուղարկելը։ Սեղմեք Չեղարկել փոխանցումը։',
        dict(text='Ուղարկելուց հետո ընտրեք, թե ինչպես եք ուղարկել, ավելացրեք հետևման համարը և սեղմեք Նշել որպես '
                  'ուղարկված։', label='Նշել որպես ուղարկված'),
        'Այսուհետ այս ծանուցման համար վարձակալի քարտից գումար չի գանձվի։ Ոչ կրկնակի փորձեր, ոչ հիշեցումներ, '
        'ոչ պարտքերի հավաքագրում։',
        dict(text='Ցանկում ծանուցումն այժմ ունի նշում՝ Փոխանցված է վարձակալին։', label='Փոխանցված է վարձակալին'),
        dict(text='Երբ մարմինը պատասխանի, սեղմեք Մարմինն ընդունեց կամ Մարմինը մերժեց։', label='Մարմնի պատասխանը'),
        'Եթե մարմինը մերժել է, վարձակալից կգանձվի սովորականի պես։',
        dict(text='Եվս մեկ ճանապարհ։ Երբ Ավելացնել փոստով ստացված տուգանք պատուհանը տուգանքը պահում է վարձույթի '
                  'վրա, այն անմիջապես առաջարկում է Փոխանցել վարձակալին։', label='Փոստով ստացված տուգանքից'),
        'Ավելացնել մի քանի տուգանք պատուհանում վարձույթի վրա պահված յուրաքանչյուր տող ունի նույն հղումը։',
    ])

# ----------------------------------------------------------------------------------------------- fa
LANGS['fa'] = dict(
    title='انتقال اخطار عوارض یا جریمه به مستأجر',
    sub='پورتال نامه را برای مرجع می‌نویسد؛ شما امضا می‌کنید و می‌فرستید و از کارت مستأجر برداشت نمی‌شود',
    lines=[
        dict(text='در بسیاری از ایالت‌های آمریکا می‌توان اخطار عوارض یا جریمه را به مستأجر منتقل کرد. شما نامه‌ای '
                  'امضاشده با مشخصات مستأجر برای مرجع می‌فرستید.', label='انتقال به مستأجر'),
        dict(text='پورتال این نامه را برای شما آماده می‌کند. قوانین حدود ۶۰ مرجع در ۳۰ ایالت را می‌شناسد.',
             say='پورتال این نامه را برای شما آماده می‌کند. قوانین حدود شصت مرجع در سی ایالت را می‌شناسد.'),
        'عوارض و تخلفات و سپس تخلفات را باز کنید. منوی ردیف را باز کنید یا روی ردیف راست‌کلیک کنید و انتقال به '
        'مستأجر را بزنید. این گزینه فقط وقتی هست که اخطار به یک اجاره وصل باشد.',
        dict(text='بالای پنجره: مستأجر، و اینکه قرارداد امضاشدهٔ او را دارید یا نه.', label='قانون مرجع'),
        'در قانون مرجع، مناسب‌ترین گزینه از قبل انتخاب شده است. می‌توانید گزینهٔ دیگری را از فهرست انتخاب کنید.',
        'زیر آن: قانونی که این کار را مجاز می‌کند، و مهلت ارسال.',
        'سپس مراحل این مرجع، و اینکه باید نزد دفتر اسناد رسمی امضا کنید یا امضای خودتان کافی است.',
        'و محل ارسال: نشانی پستی، فکس یا یک وب‌سایت.',
        dict(text='اگر چیزی کم باشد، مثلاً نشانی مستأجر یا قرارداد امضاشده، اینجا با رنگ قرمز نوشته می‌شود. اول آن '
                  'را اضافه کنید و بعد برگردید.', label='چیزی کم است؟'),
        dict(text='نام امضاکننده و سمت او را بنویسید و سپس دانلود بسته را بزنید.', label='دانلود بسته'),
        dict(text='یک نامهٔ PDF می‌گیرید: شرکت شما، نشانی مرجع، اخطار و قانون.', label='نامه'),
        'بعد نام و نشانی مستأجر و جایی برای امضای شما. اگر قرارداد اجارهٔ امضاشده ذخیره شده باشد، به انتهای آن '
        'اضافه می‌شود.',
        dict(text='نامه را امضا کنید و خودتان برای مرجع بفرستید.', label='امضا و ارسال'),
        'پیش از ارسال پشیمان شدید؟ لغو انتقال را بزنید.',
        dict(text='بعد از ارسال، روش ارسال را انتخاب کنید، شمارهٔ پیگیری را وارد کنید و علامت‌گذاری به‌عنوان '
                  'ارسال‌شده را بزنید.', label='علامت‌گذاری به‌عنوان ارسال‌شده'),
        'از این پس بابت این اخطار از کارت مستأجر برداشت نمی‌شود. نه تلاش دوباره، نه یادآوری، نه وصول مطالبات.',
        dict(text='در فهرست، کنار اخطار اکنون نوشته شده: به مستأجر منتقل شد.', label='به مستأجر منتقل شد'),
        dict(text='وقتی مرجع پاسخ داد، مرجع پذیرفت یا مرجع رد کرد را بزنید.', label='پاسخ مرجع'),
        'اگر مرجع رد کرد، از مستأجر مانند قبل برداشت می‌شود.',
        dict(text='یک راه دیگر هم هست. وقتی افزودن جریمهٔ پستی جریمه را روی یک اجاره ذخیره می‌کند، پنجره همان لحظه '
                  'انتقال به مستأجر را پیشنهاد می‌دهد.', label='از جریمهٔ پستی'),
        'در افزودن چند جریمه، هر ردیف ذخیره‌شده روی یک اجاره همین پیوند را دارد.',
    ])

# ----------------------------------------------------------------------------------------------- ur
LANGS['ur'] = dict(
    title='ٹول نوٹس یا چالان کرایہ دار کو منتقل کریں',
    sub='پورٹل ادارے کے لیے خط لکھتا ہے — آپ دستخط کر کے بھیجتے ہیں، اور کرایہ دار کے کارڈ سے رقم نہیں کٹتی',
    lines=[
        dict(text='امریکہ کی کئی ریاستوں میں ٹول نوٹس یا چالان کرایہ دار کو منتقل کیا جا سکتا ہے۔ آپ ادارے کو '
                  'کرایہ دار کی تفصیلات کے ساتھ دستخط شدہ خط بھیجتے ہیں۔', label='کرایہ دار کو منتقل کریں'),
        dict(text='پورٹل یہ خط آپ کے لیے تیار کرتا ہے۔ اسے 30 ریاستوں کے تقریباً 60 اداروں کے اصول معلوم ہیں۔',
             say='پورٹل یہ خط آپ کے لیے تیار کرتا ہے۔ اسے تیس ریاستوں کے تقریباً ساٹھ اداروں کے اصول معلوم ہیں۔'),
        'ٹول اور خلاف ورزیاں، پھر خلاف ورزیاں کھولیں۔ قطار کا مینو کھولیں یا قطار پر رائٹ کلک کریں، اور کرایہ '
        'دار کو منتقل کریں دبائیں۔ یہ صرف تب نظر آتا ہے جب نوٹس کسی کرائے سے جڑا ہو۔',
        dict(text='سب سے اوپر: کرایہ دار، اور یہ کہ اس کا دستخط شدہ معاہدہ آپ کے پاس ہے یا نہیں۔', label='ادارے کا اصول'),
        'ادارے کا اصول میں سب سے موزوں اصول پہلے سے چنا ہوا ہے۔ آپ فہرست سے کوئی اور بھی چن سکتے ہیں۔',
        'اس کے نیچے: وہ قانون جو اس کی اجازت دیتا ہے، اور بھیجنے کی آخری تاریخ۔',
        'پھر اس ادارے کے مراحل، اور یہ کہ نوٹری کے سامنے دستخط کرنے ہیں یا صرف آپ کا دستخط کافی ہے۔',
        'اور کہاں بھیجیں: ڈاک کا پتہ، فیکس یا کوئی ویب سائٹ۔',
        dict(text='اگر کچھ کمی ہو، جیسے کرایہ دار کا پتہ یا دستخط شدہ معاہدہ، تو یہاں سرخ رنگ میں لکھا ہوتا ہے۔ '
                  'پہلے وہ شامل کریں، پھر واپس آئیں۔', label='کچھ کمی ہے؟'),
        dict(text='دستخط کرنے والے کا نام اور عہدہ لکھیں، پھر پیکج ڈاؤن لوڈ کریں دبائیں۔', label='پیکج ڈاؤن لوڈ کریں'),
        dict(text='آپ کو PDF میں ایک خط ملتا ہے: آپ کی کمپنی، ادارے کا پتہ، نوٹس اور قانون۔', label='خط'),
        'پھر کرایہ دار کا نام اور پتہ، اور آپ کے دستخط کی جگہ۔ اگر دستخط شدہ کرایہ نامہ محفوظ ہو تو وہ آخر میں '
        'لگ جاتا ہے۔',
        dict(text='خط پر دستخط کریں اور خود ادارے کو بھیجیں۔', label='دستخط کریں اور بھیجیں'),
        'بھیجنے سے پہلے ارادہ بدل گیا؟ منتقلی منسوخ کریں دبائیں۔',
        dict(text='بھیجنے کے بعد چنیں کہ کیسے بھیجا، ٹریکنگ نمبر لکھیں، اور بھیجا ہوا نشان زد کریں دبائیں۔',
             label='بھیجا ہوا نشان زد کریں'),
        'اب سے اس نوٹس کی رقم کرایہ دار کے کارڈ سے نہیں کٹے گی۔ نہ دوبارہ کوشش، نہ یاد دہانی، نہ وصولی ایجنسی۔',
        dict(text='فہرست میں نوٹس پر اب لکھا ہے: کرایہ دار کو منتقل ہو گیا۔', label='کرایہ دار کو منتقل ہو گیا'),
        dict(text='جب ادارہ جواب دے تو ادارے نے قبول کیا یا ادارے نے انکار کیا دبائیں۔', label='ادارے کا جواب'),
        'اگر ادارے نے انکار کیا تو کرایہ دار سے پہلے کی طرح وصولی ہوگی۔',
        dict(text='ایک اور راستہ بھی ہے۔ جب ڈاک سے آیا چالان شامل کریں کسی چالان کو کرائے پر محفوظ کرتا ہے، تو '
                  'کھڑکی فوراً کرایہ دار کو منتقل کریں پیش کرتی ہے۔', label='ڈاک سے آئے چالان سے'),
        'کئی چالان شامل کریں میں، کرائے پر محفوظ ہر قطار میں یہی لنک ہوتا ہے۔',
    ])
