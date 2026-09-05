"""Build the localised two-minute cuts: es, fr, pt, de.

Each locale ships its own owner-web screenshots, its own on-screen copy, and
narration that quotes the figures actually visible on those screens - the
capture runs happened at different times, so the numbers genuinely differ.

    python localize.py            # all four
    python localize.py fr de
"""
import io
import json
import re
import sys

from voice_defaults import adult_narrator, pitch_markup

# Figures read off each locale's own screenshots.
#
# `spokenEn` / `spokenRu` are the same figures said aloud. Every localised cut
# carries the English subtitle track as well (and the Russian one, unless it is
# the Russian cut), and those tracks are lifted from the English film - which was
# captured on another day, off other screens. Left alone they narrate $412 over
# thirty-nine crossings while this locale's screenshot shows something else, so
# the one cue that quotes money is re-said here.
FIGURES = {
    'es': {'total': '$100.89', 'crossings': '15', 'driver': '$48.26',
           'spokenEn': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'spokenRu': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'fr': {'total': '$100.89', 'crossings': '15', 'driver': '$48.26',
           'spokenEn': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'spokenRu': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'pt': {'total': '$100.89', 'crossings': '15', 'driver': '$48.26',
           'spokenEn': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'spokenRu': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'de': {'total': '$182.41', 'crossings': '25', 'driver': '$32.03',
           'spokenEn': 'One hundred and eighty-two dollars and forty-one cents, across twenty-five crossings.',
           'spokenRu': 'Сто восемьдесят два доллара сорок один цент за двадцать пять проездов.'},
    'ru': {'total': '$182.41', 'crossings': '25', 'driver': '$32.03',
           'spokenEn': 'One hundred and eighty-two dollars and forty-one cents, across twenty-five crossings.',
           'spokenRu': 'Сто восемьдесят два доллара сорок один цент за двадцать пять проездов.'},
}

# The money cue as the English film says it, in both of the tracks that ride along.
# If the English cut is re-worded these stop matching and the build stops, rather
# than quietly shipping the English figures over a localised screen.
EN_MONEY_CUE = 'Four hundred and twelve dollars, across thirty-nine crossings.'
RU_MONEY_CUE = 'Четыреста двенадцать долларов за тридцать девять проездов.'

# Subtitle picker labels for the two tracks every cut carries besides its own.
SUB_LABELS = {'en': 'Subtitles · EN', 'ru': 'Субтитры · RU'}

# Highlight boxes that suit the localised layouts (the English cut has its own).
SPOTS = {
    'tolls':      ('style="left:0.4%;top:18.5%;width:15%;height:6.5%"',
                   'style="left:0.4%;top:24%;width:17%;height:5.4%"'),
    'violations': ('style="left:58%;top:38%;width:41%;height:50%"',
                   'style="left:39%;top:56%;width:29%;height:34%"'),
    'charges':    ('style="left:4%;top:12%;width:34%;height:46%"',
                   'style="left:55%;top:55%;width:42%;height:33%"'),
    'driver':     ('style="left:33%;top:19%;width:16%;height:8%"',
                   'style="left:30%;top:76%;width:26%;height:10%"'),
}

L = {}

# ----------------------------------------------------------------- Spanish ---
L['es'] = {
 'title': 'Dos Minutos con Su Flota', 'runtime': 'Película · ',
 'posterRuntime': 'Para propietarios de flotas · ',
 'chrome': ['transacciones de peaje', 'infracciones', 'cargos',
            'gps · mapa de viaje', 'registro de cargos', 'estado de cuenta'],
 'eyebrows': ['Una semana · una flota pequeña', 'Adónde va el dinero',
              'Cada cargo, emparejado', 'Lo que le cuesta a usted',
              'Y funciona al revés'],
 'callouts': ['{total} en una sola semana — <b>{crossings} pasos</b>',
              'Ni un solo cliente identificado en el extracto.<br>Lo acaba pagando el propietario.',
              'El coche en el pórtico, <b>al segundo</b> — y la reserva identifica al conductor.',
              'Se cobra <b>al cliente</b> — {driver}, no a usted.',
              '<b>Parte del propietario</b> — ingresos con la flota que ya tiene.'],
 'leaks': [('Peajes sin atribuir', 'Nadie pudo probar quién conducía'),
           ('Multas tardías', 'Publicadas tras cerrar el alquiler'),
           ('Cargos posteriores', 'Daños y combustible, hallados tarde'),
           ('Horas de administración', 'Hojas de cálculo contra extractos')],
 'free': ('Gratis', 'Sin contrato, sin flota mínima y sin comisión sobre sus ingresos de alquiler.'),
 'prices': [('Suscripción', 'GRATIS'), ('Alta y puesta en marcha', 'GRATIS'),
            ('Cargo por vehículo', 'GRATIS'), ('Conectar el GPS que ya utiliza', 'GRATIS'),
            ('Recuperación de peajes y multas', 'GRATIS'),
            ('Nuestro equipo de telemática', 'Opcional · de pago')],
 'slogan': 'Deje de perder.<br><em>Empiece a ganar.</em>',
 'freeline': 'Gratis para propietarios de flotas',
 'cta': 'MyEZToll — pida una demo y véalo en su propia flota.',
 'legal': 'Aegis AG Soft LLC · Nueva Jersey, EE. UU. · salvo el equipo de telemática opcional',
 'posterKicker': 'Para propietarios de flotas',
 'posterText': 'Dos minutos sobre dónde pierde dinero su flota, y por qué MyEZToll no le cuesta nada al propietario y además le paga una parte.',
 'play': 'Reproducir con narración', 'fineprint': 'Narración y subtítulos · ES · EN · RU',
 'subLabel': 'Subtítulos · ES',
 'footnote': 'Las pantallas son el producto real, capturadas de una cuenta de propietario; matrículas, nombres y datos de contacto están ocultos.',
 'chapters': ['La fuga', 'Cuatro fugas', 'Deje de perder', 'Es gratis', 'Le pagamos', 'Empiece gratis'],
 'lines': [
  ["Esto es una semana de peajes en una sola flota pequeña.",
   "Cien dólares con ochenta y nueve centavos, en quince pasos.",
   "La pregunta nunca es cuánto costó. Es quién lo paga.",
   "Si no puede identificar al cliente, lo paga usted."],
  ["Y los peajes son solo la primera fuga.",
   "Las multas de cámara se publican semanas después, con el alquiler ya cerrado.",
   "Los daños y el combustible aparecen cuando el conductor ya se fue.",
   "Y su personal quema horas cuadrando extractos con reservas."],
  ["MyEZToll cierra las cuatro.",
   "El GPS sitúa el coche en el pórtico; la reserva identifica al conductor.",
   "Las multas se rastrean noventa días atrás; ninguna caduca sin facturar.",
   "Y cada cargo llega automáticamente a la tarjeta del cliente."],
  ["¿Y cuánto le cuesta la plataforma? Nada.",
   "Sin suscripción. Sin coste de alta. Sin cargo por vehículo.",
   "Conectar el GPS que ya utiliza también es gratis.",
   "La única opción de pago es nuestro propio equipo de telemática.",
   "Todo lo demás sigue siendo gratis, mientras lo use."],
  ["Cobramos al conductor que realmente condujo, nunca a usted.",
   "Y una parte de todo lo que recuperamos se le abona a usted.",
   "Parte del propietario. Ingresos reales, con la flota que ya tiene."],
  ["Deje de perder. Empiece a ganar.",
   "MyEZToll: gratis para los propietarios de flotas.",
   "Pida una demo y véalo funcionando en su propia flota."]],
}

# ------------------------------------------------------------------ French ---
L['fr'] = {
 'title': 'Deux Minutes sur Votre Flotte', 'runtime': 'Film · ',
 'posterRuntime': 'Pour les propriétaires de flotte · ',
 'chrome': ['transactions de péage', 'infractions', 'frais',
            'gps · carte de trajet', 'registre des frais', 'relevé de compte'],
 'eyebrows': ['Une semaine · une petite flotte', "Où part l'argent",
              'Chaque frais, rapproché', 'Ce que cela vous coûte',
              "Et cela fonctionne à l'inverse"],
 'callouts': ['{total} en une seule semaine — <b>{crossings} passages</b>',
              "Pas un seul locataire nommé sur le relevé.<br>C'est le propriétaire qui paie.",
              'La voiture au portique, <b>à la seconde près</b> — et la réservation nomme le conducteur.',
              "C'est <b>le locataire</b> qui est facturé — {driver}, pas vous.",
              '<b>Part du propriétaire</b> — des revenus sur une flotte que vous possédez déjà.'],
 'leaks': [('Péages non attribués', 'Impossible de prouver qui conduisait'),
           ('Contraventions tardives', 'Publiées après la fin de la location'),
           ('Frais après le trajet', 'Dommages et carburant, trouvés trop tard'),
           ('Heures administratives', 'Tableurs contre relevés')],
 'free': ('Gratuit', 'Sans contrat, sans flotte minimale et sans commission sur vos revenus de location.'),
 'prices': [('Abonnement', 'GRATUIT'), ('Mise en service', 'GRATUIT'),
            ('Frais par véhicule', 'GRATUIT'),
            ('Connecter le GPS que vous utilisez déjà', 'GRATUIT'),
            ('Récupération des péages et contraventions', 'GRATUIT'),
            ('Notre matériel télématique', 'Optionnel · payant')],
 'slogan': 'Arrêtez de perdre.<br><em>Commencez à gagner.</em>',
 'freeline': 'Gratuit pour les propriétaires de flotte',
 'cta': 'MyEZToll — demandez une démo et voyez-la sur votre propre flotte.',
 'legal': 'Aegis AG Soft LLC · New Jersey, États-Unis · sauf le matériel télématique optionnel',
 'posterKicker': 'Pour les propriétaires de flotte',
 'posterText': "Deux minutes sur les fuites d'argent de votre flotte, et pourquoi MyEZToll ne coûte rien au propriétaire et lui reverse une part.",
 'play': 'Lire avec narration', 'fineprint': 'Narration et sous-titres · FR · EN · RU',
 'subLabel': 'Sous-titres · FR',
 'footnote': 'Les écrans sont le produit réel, capturés depuis un compte propriétaire; plaques, noms et coordonnées sont masqués.',
 'chapters': ['La fuite', 'Quatre fuites', 'Colmater', "C'est gratuit", 'On vous paie', 'Commencez'],
 'lines': [
  ["Voici une semaine de péages sur une seule petite flotte.",
   "Cent dollars et quatre-vingt-neuf cents, sur quinze passages.",
   "La question n'est jamais combien cela a coûté. C'est qui paie.",
   "Si vous ne pouvez pas nommer le locataire, c'est vous."],
  ["Et les péages ne sont que la première fuite.",
   "Les contraventions par caméra arrivent des semaines plus tard, la location déjà close.",
   "Dommages et carburant apparaissent une fois le conducteur parti.",
   "Et votre équipe brûle des heures à rapprocher relevés et réservations."],
  ["MyEZToll colmate les quatre.",
   "Le GPS place la voiture au portique; la réservation nomme le conducteur.",
   "Les contraventions sont suivies quatre-vingt-dix jours en arrière, aucune n'expire sans facturation.",
   "Et chaque frais arrive automatiquement sur la carte du locataire."],
  ["Alors, combien vous coûte la plateforme? Rien.",
   "Pas d'abonnement. Pas de frais de mise en service. Rien par véhicule.",
   "Connecter le GPS que vous utilisez déjà est également gratuit.",
   "La seule option payante est notre propre matériel télématique.",
   "Tout le reste reste gratuit, aussi longtemps que vous l'utilisez."],
  ["Nous encaissons auprès du conducteur qui a réellement conduit, jamais auprès de vous.",
   "Et une part de tout ce que nous récupérons vous est reversée.",
   "Part du propriétaire. Un vrai revenu, sur une flotte que vous possédez déjà."],
  ["Arrêtez de perdre. Commencez à gagner.",
   "MyEZToll — gratuit pour les propriétaires de flotte.",
   "Demandez une démo et voyez-la tourner sur votre propre flotte."]],
}

# -------------------------------------------------------------- Portuguese ---
L['pt'] = {
 'title': 'Dois Minutos com Sua Frota', 'runtime': 'Filme · ',
 'posterRuntime': 'Para proprietários de frota · ',
 'chrome': ['transações de pedágio', 'multas', 'cobranças',
            'gps · mapa de viagem', 'registro de cobranças', 'extrato de conta'],
 'eyebrows': ['Uma semana · uma frota pequena', 'Para onde vai o dinheiro',
              'Cada cobrança, conciliada', 'O que custa a você',
              'E funciona ao contrário'],
 'callouts': ['{total} em uma única semana — <b>{crossings} passagens</b>',
              'Nenhum locatário identificado no extrato.<br>Quem acaba pagando é o proprietário.',
              'O carro no pórtico, <b>no segundo exato</b> — e a reserva identifica o motorista.',
              'Quem é cobrado é <b>o locatário</b> — {driver}, não você.',
              '<b>Parte do proprietário</b> — receita sobre uma frota que já é sua.'],
 'leaks': [('Pedágios sem atribuição', 'Ninguém provou quem dirigia'),
           ('Multas atrasadas', 'Publicadas depois de encerrada a locação'),
           ('Cobranças pós-viagem', 'Danos e combustível, achados tarde demais'),
           ('Horas administrativas', 'Planilhas contra extratos')],
 'free': ('Grátis', 'Sem contrato, sem frota mínima e sem comissão sobre a sua receita de locação.'),
 'prices': [('Assinatura', 'GRÁTIS'), ('Implantação', 'GRÁTIS'),
            ('Cobrança por veículo', 'GRÁTIS'),
            ('Conectar o GPS que você já usa', 'GRÁTIS'),
            ('Recuperação de pedágios e multas', 'GRÁTIS'),
            ('Nosso equipamento de telemetria', 'Opcional · pago')],
 'slogan': 'Pare de perder.<br><em>Comece a ganhar.</em>',
 'freeline': 'Grátis para proprietários de frota',
 'cta': 'MyEZToll — peça uma demonstração e veja na sua própria frota.',
 'legal': 'Aegis AG Soft LLC · Nova Jersey, EUA · exceto o equipamento de telemetria opcional',
 'posterKicker': 'Para proprietários de frota',
 'posterText': 'Dois minutos sobre onde a sua frota perde dinheiro, e por que o MyEZToll não custa nada ao proprietário e ainda paga uma parte.',
 'play': 'Reproduzir com narração', 'fineprint': 'Narração e legendas · PT · EN · RU',
 'subLabel': 'Legendas · PT',
 'footnote': 'As telas são o produto real, capturadas de uma conta de proprietário; placas, nomes e contatos estão ocultos.',
 'chapters': ['O vazamento', 'Quatro vazamentos', 'Pare de perder', 'É grátis', 'Você recebe', 'Comece grátis'],
 'lines': [
  ["Esta é uma semana de pedágios em uma única frota pequena.",
   "Cem dólares e oitenta e nove centavos, em quinze passagens.",
   "A pergunta nunca é quanto custou. É quem paga.",
   "Se você não pode identificar o locatário, quem paga é você."],
  ["E os pedágios são apenas o primeiro vazamento.",
   "As multas de câmera são publicadas semanas depois, com a locação já encerrada.",
   "Danos e combustível aparecem quando o motorista já foi embora.",
   "E sua equipe queima horas conciliando extratos com reservas."],
  ["O MyEZToll fecha os quatro.",
   "O GPS coloca o carro no pórtico; a reserva identifica o motorista.",
   "As multas são rastreadas noventa dias para trás; nenhuma expira sem cobrança.",
   "E cada cobrança chega automaticamente ao cartão do locatário."],
  ["E quanto custa a plataforma para você? Nada.",
   "Sem assinatura. Sem taxa de implantação. Sem cobrança por veículo.",
   "Conectar o GPS que você já usa também é grátis.",
   "A única opção paga é o nosso próprio equipamento de telemetria.",
   "Todo o resto continua grátis, enquanto você usar."],
  ["Cobramos do motorista que realmente dirigiu, nunca de você.",
   "E uma parte de tudo o que recuperamos é paga a você.",
   "Parte do proprietário. Receita real, sobre uma frota que já é sua."],
  ["Pare de perder. Comece a ganhar.",
   "MyEZToll — grátis para proprietários de frota.",
   "Peça uma demonstração e veja funcionando na sua própria frota."]],
}

# ------------------------------------------------------------------ German ---
L['de'] = {
 'title': 'Zwei Minuten mit Ihrer Flotte', 'runtime': 'Film · ',
 'posterRuntime': 'Für Flottenbetreiber · ',
 'chrome': ['mautbuchungen', 'verstöße', 'belastungen',
            'gps · fahrtkarte', 'belastungsprotokoll', 'kontoauszug'],
 'eyebrows': ['Eine Woche · eine kleine Flotte', 'Wohin das Geld fließt',
              'Jede Belastung, zugeordnet', 'Was es Sie kostet',
              'Und es läuft andersherum'],
 'callouts': ['{total} in einer einzigen Woche — <b>{crossings} Durchfahrten</b>',
              'Kein einziger Mieter im Auszug genannt.<br>Zahlen muss am Ende der Eigentümer.',
              'Das Auto am Mautportal, <b>auf die Sekunde</b> — und die Buchung nennt den Fahrer.',
              'Belastet wird <b>der Mieter</b> — {driver}, nicht Sie.',
              '<b>Eigentümeranteil</b> — Einnahmen mit einer Flotte, die Ihnen schon gehört.'],
 'leaks': [('Nicht zugeordnete Maut', 'Niemand konnte beweisen, wer fuhr'),
           ('Späte Verstöße', 'Veröffentlicht nach Mietende'),
           ('Kosten nach der Fahrt', 'Schäden und Kraftstoff, zu spät entdeckt'),
           ('Verwaltungsstunden', 'Tabellen gegen Auszüge')],
 'free': ('Gratis', 'Kein Vertrag, keine Mindestflotte und keine Provision auf Ihre Mieteinnahmen.'),
 'prices': [('Abonnement', 'GRATIS'), ('Einrichtung', 'GRATIS'),
            ('Gebühr pro Fahrzeug', 'GRATIS'),
            ('Anbindung Ihres vorhandenen GPS', 'GRATIS'),
            ('Maut- und Verstoß-Einzug', 'GRATIS'),
            ('Unsere Telematik-Hardware', 'Optional · kostenpflichtig')],
 'slogan': 'Nicht mehr verlieren.<br><em>Endlich verdienen.</em>',
 'freeline': 'Gratis für Flottenbetreiber',
 'cta': 'MyEZToll — Demo anfragen und auf Ihrer eigenen Flotte sehen.',
 'legal': 'Aegis AG Soft LLC · New Jersey, USA · ausgenommen optionale Telematik-Hardware',
 'posterKicker': 'Für Flottenbetreiber',
 'posterText': 'Zwei Minuten darüber, wo Ihre Flotte Geld verliert — und warum MyEZToll den Eigentümer nichts kostet und ihm einen Anteil auszahlt.',
 'play': 'Mit Erzählung abspielen', 'fineprint': 'Erzählung und Untertitel · DE · EN · RU',
 'subLabel': 'Untertitel · DE',
 'footnote': 'Die Screenshots zeigen das echte Produkt aus einem Eigentümerkonto; Kennzeichen, Namen und Kontaktdaten sind unkenntlich gemacht.',
 'chapters': ['Das Leck', 'Vier Lecks', 'Lecks schließen', 'Es ist gratis', 'Sie werden bezahlt', 'Gratis starten'],
 'lines': [
  ["Das ist eine Woche Maut auf einer einzigen kleinen Flotte.",
   "Hundertzweiundachtzig Dollar und einundvierzig Cent, auf fünfundzwanzig Durchfahrten.",
   "Die Frage ist nie, was es gekostet hat. Sondern wer es bezahlt.",
   "Wenn Sie den Mieter nicht benennen können, zahlen Sie."],
  ["Und die Maut ist nur das erste Leck.",
   "Kameraverstöße werden Wochen später veröffentlicht, wenn die Miete längst beendet ist.",
   "Schäden und Kraftstoff tauchen auf, wenn der Fahrer längst weg ist.",
   "Und Ihr Team verbrennt Stunden damit, Auszüge mit Buchungen abzugleichen."],
  ["MyEZToll schließt alle vier.",
   "Das GPS setzt das Auto ans Mautportal; die Buchung nennt den Fahrer.",
   "Verstöße werden neunzig Tage rückwirkend verfolgt, keiner verfällt unberechnet.",
   "Und jede Belastung landet automatisch auf der Karte des Mieters."],
  ["Was kostet Sie die Plattform also? Nichts.",
   "Kein Abonnement. Keine Einrichtungsgebühr. Keine Gebühr pro Fahrzeug.",
   "Auch die Anbindung Ihres vorhandenen GPS ist kostenlos.",
   "Die einzige kostenpflichtige Option ist unsere eigene Telematik-Hardware.",
   "Alles andere bleibt gratis, solange Sie es nutzen."],
  ["Wir ziehen beim Fahrer ein, der tatsächlich gefahren ist — niemals bei Ihnen.",
   "Und ein Anteil an allem, was wir einziehen, wird an Sie ausgezahlt.",
   "Eigentümeranteil. Echte Einnahmen mit einer Flotte, die Ihnen schon gehört."],
  ["Nicht mehr verlieren. Endlich verdienen.",
   "MyEZToll — gratis für Flottenbetreiber.",
   "Fragen Sie eine Demo an und sehen Sie es auf Ihrer eigenen Flotte."]],
}

# ----------------------------------------------------------------- Russian ---
L['ru'] = {
 'title': 'Две Минуты о Вашем Парке', 'runtime': 'Ролик · ',
 'posterRuntime': 'Для владельцев автопарков · ',
 'chrome': ['платные транзакции', 'нарушения', 'списания',
            'gps · карта поездки', 'журнал списаний', 'выписка по счёту'],
 'eyebrows': ['Одна неделя · один небольшой парк', 'Куда уходят деньги',
              'Каждое начисление сопоставлено', 'Сколько это стоит вам',
              'И поток идёт обратно'],
 'callouts': ['{total} за одну неделю — <b>{crossings} проездов</b>',
              'В выписке не назван ни один арендатор.<br>В итоге платит владелец.',
              'Машина у рамки, <b>с точностью до секунды</b> — а бронь называет водителя.',
              'Списывается <b>с арендатора</b> — {driver}, не с вас.',
              '<b>Доля владельца</b> — доход на парке, который у вас уже есть.'],
 'leaks': [('Несопоставленные толлы', 'Никто не доказал, кто был за рулём'),
           ('Поздние штрафы', 'Приходят после закрытия аренды'),
           ('Начисления после поездки', 'Повреждения и топливо — слишком поздно'),
           ('Часы администрирования', 'Таблицы против выписок')],
 'free': ('Бесплатно', 'Без договора, без минимального парка и без комиссии с ваших доходов от аренды.'),
 'prices': [('Подписка', 'БЕСПЛАТНО'), ('Подключение и запуск', 'БЕСПЛАТНО'),
            ('Плата за машину', 'БЕСПЛАТНО'),
            ('Подключение вашего GPS', 'БЕСПЛАТНО'),
            ('Взыскание толлов и штрафов', 'БЕСПЛАТНО'),
            ('Наше оборудование телематики', 'Опция · платно')],
 'slogan': 'Перестаньте терять.<br><em>Начните зарабатывать.</em>',
 'freeline': 'Бесплатно для владельцев парков',
 'cta': 'MyEZToll — запишитесь на демо и посмотрите на своём парке.',
 'legal': 'Aegis AG Soft LLC · Нью-Джерси, США · кроме опционального оборудования телематики',
 'posterKicker': 'Для владельцев автопарков',
 'posterText': 'Две минуты о том, где ваш парк теряет деньги, и почему MyEZToll ничего не стоит владельцу и ещё платит ему долю.',
 'play': 'Смотреть с озвучкой', 'fineprint': 'Озвучка и субтитры · RU · EN',
 'subLabel': 'Субтитры · RU',
 'footnote': 'На экранах — реальный продукт из аккаунта владельца; номера, имена и контакты скрыты.',
 'chapters': ['Утечка', 'Четыре течи', 'Перестаём терять', 'Это бесплатно', 'Вам платят', 'Начните бесплатно'],
 'lines': [
  ["Это одна неделя толлов на одном небольшом парке.",
   "Сто восемьдесят два доллара сорок один цент за двадцать пять проездов.",
   "Вопрос не в том, сколько это стоило. Вопрос — кто платит.",
   "Если вы не можете назвать арендатора, платите вы."],
  ["И толлы — лишь первая течь.",
   "Штрафы с камер публикуются на недели позже, когда аренда уже закрыта.",
   "Повреждения и топливо всплывают, когда водителя уже нет.",
   "А сотрудники жгут часы, сверяя выписки с бронями."],
  ["MyEZToll закрывает все четыре.",
   "GPS ставит машину у рамки, а бронь называет водителя.",
   "Штрафы отслеживаются на девяносто дней назад — ни один не истечёт невыставленным.",
   "И каждое начисление автоматически уходит на карту арендатора."],
  ["А сколько стоит сама платформа? Ничего.",
   "Никакой подписки. Никакой платы за подключение. Ни цента за машину.",
   "Подключение GPS, которым вы уже пользуетесь, тоже бесплатно.",
   "Единственная платная опция — наше собственное оборудование телематики.",
   "Всё остальное остаётся бесплатным, пока вы этим пользуетесь."],
  ["Мы взыскиваем с водителя, который действительно ехал, — и никогда с вас.",
   "А доля со всего, что мы взыскали, выплачивается вам.",
   "Доля владельца. Реальный доход на парке, который у вас уже есть."],
  ["Перестаньте терять. Начните зарабатывать.",
   "MyEZToll — бесплатно для владельцев парков.",
   "Запишитесь на демо и посмотрите, как это работает на вашем парке."]],
}

# English source strings in the shell, in the same order as the locale lists.
EN_CHROME = ['owner.myeztoll.com / toll transactions', 'owner.myeztoll.com / violations',
             'charges', 'gps · trip map', 'charge log', 'account statement']
EN_EYEBROWS = ['One week · one small fleet', 'Where the money goes', 'Every charge, matched',
               'What it costs you', 'And it runs the other way']
EN_CALLOUTS = ['<span class="num">$412.68</span> in a single week — <b>39 crossings</b>',
               'Not one renter named on the statement.<br>So the owner absorbs it.',
               'Car at the gantry, <b>to the second</b> — and the booking names the driver.',
               '<b>The renter</b> is charged — <span class="num">$106.82</span>, not you.',
               '<b>Owner share</b> — income, on a fleet you already own.']
EN_LEAKS = [('Unmatched tolls', 'Nobody could prove who drove'),
            ('Late violations', 'Published after the rental closed'),
            ('Post-trip charges', 'Damage and fuel, found too late'),
            ('Admin hours', 'Spreadsheets against statements')]
EN_PRICES = [('Subscription', 'FREE'), ('Set-up and onboarding', 'FREE'),
             ('Charge per vehicle', 'FREE'), ('Connecting the GPS you already run', 'FREE'),
             ('Toll &amp; violation recovery', 'FREE'),
             ('Our own telematics hardware', 'Optional · paid')]

TIMINGS = [[0, 4.5, 10, 15.5], [0, 4.5, 11, 16.5], [0, 3.8, 10.5, 17.5],
           [0, 4.5, 11, 16.5, 21.5], [0, 6.5, 12.5], [0, 3.8, 8]]
DURS = [20, 22, 24, 26, 18, 14]

EN_LINES = None   # filled from the English build so the EN track stays available


def read_en_lines():
    src = io.open('two-minutes-on-your-fleet.html', encoding='utf-8').read()
    body = src[src.index('  var SCENES = ['):src.index('  var TOTAL =')]
    out, cur = [], None
    for line in body.splitlines():
        if re.match(r'\s*\{ chapter:', line):
            if cur is not None:
                out.append(cur)
            cur = []
        m = re.search(r'\ben:"((?:[^"\\]|\\.)*)"', line)
        if m and cur is not None:
            cur.append(m.group(1))
        m2 = re.search(r'\bru:"((?:[^"\\]|\\.)*)"', line)
        if m2 and cur is not None:
            cur[-1] = (cur[-1], m2.group(1))
    if cur:
        out.append(cur)
    return out


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def scenes_js(lang, en_ru):
    parts = ['  var SCENES = [']
    loc = L[lang]
    fig = FIGURES[lang]
    retold = {'en': 0, 'ru': 0}

    def retell(track, text):
        """The English film's money cue, re-said with this locale's own figures."""
        if text != (EN_MONEY_CUE if track == 'en' else RU_MONEY_CUE):
            return text
        retold[track] += 1
        return fig['spokenEn'] if track == 'en' else fig['spokenRu']

    for si in range(6):
        parts.append('    { chapter:"%s", dur:%d, cues:[' % (esc(loc['chapters'][si]), DURS[si]))
        cues = []
        for ci, text in enumerate(loc['lines'][si]):
            en, ru = en_ru[si][ci]
            if lang == 'ru':
                # a Russian-led cut must not emit the ru key twice
                cues.append('      {t:%g, ru:"%s",\n               en:"%s"}'
                            % (TIMINGS[si][ci], esc(text), esc(retell('en', en))))
            else:
                cues.append('      {t:%g, %s:"%s",\n               en:"%s",\n               ru:"%s"}'
                            % (TIMINGS[si][ci], lang, esc(text),
                               esc(retell('en', en)), esc(retell('ru', ru))))
        parts.append(',\n'.join(cues))
        parts.append('    ]},\n')
    parts.append('  ];')

    # Exactly one cue quotes money, in each track this cut emits.
    expected = {'en': 1, 'ru': 0 if lang == 'ru' else 1}
    if retold != expected:
        raise SystemExit('[%s] money cue retold %s, expected %s - has the English cut been re-worded?'
                         % (lang, retold, expected))
    return '\n'.join(parts) + '\n'


def build(lang):
    loc = L[lang]
    fig = FIGURES[lang]
    shell = io.open('two_min_shell.html', encoding='utf-8').read()

    def rep(a, b):
        nonlocal shell
        if a not in shell:
            raise SystemExit('[%s] not found: %s' % (lang, a[:70]))
        shell = shell.replace(a, b, 1)

    for en, tr in zip(EN_CHROME, loc['chrome']):
        rep('<span>%s</span>' % en, '<span>%s</span>' % tr)
    for en, tr in zip(EN_EYEBROWS, loc['eyebrows']):
        rep('<div class="eyebrow">%s</div>' % en, '<div class="eyebrow">%s</div>' % tr)
    for en, tr in zip(EN_CALLOUTS, loc['callouts']):
        tr = tr.replace('{total}', '<span class="num">%s</span>' % fig['total']) \
               .replace('{crossings}', fig['crossings']) \
               .replace('{driver}', '<span class="num">%s</span>' % fig['driver'])
        rep(en, tr)
    for (en_t, en_s), (tr_t, tr_s) in zip(EN_LEAKS, loc['leaks']):
        rep('<p>%s<small>%s</small></p>' % (en_t, en_s), '<p>%s<small>%s</small></p>' % (tr_t, tr_s))
    for (en_w, en_c), (tr_w, tr_c) in zip(EN_PRICES, loc['prices']):
        rep('<span class="what">%s</span><span class="cost">%s</span>' % (en_w, en_c),
            '<span class="what">%s</span><span class="cost">%s</span>' % (tr_w, tr_c))
    for key, (en_style, loc_style) in SPOTS.items():
        rep(en_style, loc_style)

    # localised toll/charge crops are taller than the English ones
    rep('style="left:5cqw;top:9.5cqw;width:57cqw"', 'style="left:5cqw;top:9.5cqw;width:53cqw"')
    shell = shell.replace('top:43.6cqw;max-width:34cqw', 'top:42.8cqw;max-width:34cqw')

    rep('>Free</div>', '>%s</div>' % loc['free'][0])
    rep('No contract, no minimum fleet, and no fee taken out of your rental income.', loc['free'][1])
    rep('Stop losing.<br><em>Start earning.</em></div>', loc['slogan'] + '</div>')
    rep('>Free for fleet owners<', '>%s<' % loc['freeline'])
    rep('MyEZToll — book a demo and see it on your own fleet.', loc['cta'])
    rep('Aegis AG Soft LLC · New Jersey, USA · optional telematics hardware excepted', loc['legal'])
    rep('<div class="kicker" id="posterRuntime">A film for fleet owners</div>',
        '<div class="kicker" id="posterRuntime">%s</div>' % loc['posterKicker'])
    rep('<h2>Stop losing.<br><em>Start earning.</em></h2>', '<h2>%s</h2>' % loc['slogan'])
    rep('Two minutes on where your fleet leaks money — and why MyEZToll costs the owner nothing and pays a share back.',
        loc['posterText'])
    rep('        Play with narration', '        ' + loc['play'])
    rep('<div class="fineprint">Narration &amp; subtitles · EN · ES · RU</div>',
        '<div class="fineprint">%s</div>' % loc['fineprint'])
    rep('<div class="chapter-name" id="chapterName">The leak</div>',
        '<div class="chapter-name" id="chapterName">%s</div>' % loc['chapters'][0])
    rep('Screens are the real product, captured from a live owner account; plate numbers, names and contact details are redacted at source.',
        loc['footnote'])
    rep('<title>Two Minutes on Your Fleet</title>', '<title>%s</title>' % loc['title'])

    # This locale first in the subtitle picker, then the tracks that ride along.
    # A cut only offers the languages its cues actually carry: the Russian cut has
    # no Spanish track, and offering one leaves the picker serving blank captions.
    subs = [lang] + [code for code in ('en', 'ru') if code != lang]
    labels = dict(SUB_LABELS, **{lang: loc['subLabel']})
    rep('      <option value="en">Subtitles · EN</option>\n'
        '      <option value="es">Subtítulos · ES</option>\n'
        '      <option value="ru">Субтитры · RU</option>',
        '\n'.join('      <option value="%s">%s</option>' % (code, labels[code]) for code in subs))

    engine_src = io.open('stop-losing-start-earning.html', encoding='utf-8').read()
    engine = re.search(r'<script>\n(.*)\n</script>', engine_src, re.S).group(1)
    engine = engine[:engine.index('  var SCENES = [')] + scenes_js(lang, EN_LINES) + '\n' \
        + engine[engine.index('  var TOTAL ='):]
    engine = engine.replace("  var lang = 'en', ccOn = true, voiceOn = true;",
                            "  var lang = '%s', ccOn = true, voiceOn = true;" % lang, 1)
    # ...and ?lang= accepts exactly those, so no link can select a track that is
    # not in the file.
    engine = engine.replace("/[?&]lang=(en|es|ru)/i", "/[?&]lang=(%s)/i" % '|'.join(subs), 1)
    engine = engine.replace("var runtimeText = 'Sales film · '", "var runtimeText = '%s'" % loc['runtime'], 1)
    engine = engine.replace("document.getElementById('posterRuntime').textContent = 'A film for fleet owners · '",
                            "document.getElementById('posterRuntime').textContent = '%s'" % loc['posterRuntime'], 1)
    # narrate this locale too
    engine = engine.replace("var LANG_TARGET = { en:'en-gb', es:'es-es', ru:'ru-ru' };",
                            "var LANG_TARGET = { en:'en-gb', es:'es-es', ru:'ru-ru', fr:'fr-ca', pt:'pt-br', de:'de-de' };", 1)
    engine = engine.replace("var LANG_NAME   = { en:'British English', es:'Spanish', ru:'Russian' };",
                            "var LANG_NAME   = { en:'British English', es:'Spanish', ru:'Russian', fr:'French', pt:'Portuguese', de:'German' };", 1)
    engine = engine.replace("var LANG_ADD    = { en:'English (United Kingdom)', es:'Spanish (Spain)', ru:'Russian' };",
                            "var LANG_ADD    = { en:'English (United Kingdom)', es:'Spanish (Spain)', ru:'Russian', fr:'French (Canada)', pt:'Portuguese (Brazil)', de:'German' };", 1)

    # the narrator is an adult woman, whatever the engine source defaulted to
    engine = adult_narrator(engine, lang)
    shell = pitch_markup(shell, lang)

    shots = json.load(io.open('shots_%s/shots.json' % lang, encoding='utf-8'))
    for k, v in shots.items():
        shell = shell.replace('__SHOT_%s__' % k, v)
    if re.findall(r'__SHOT_\w+__', shell):
        raise SystemExit('[%s] unfilled shot placeholders' % lang)

    out = shell + '\n<script>\n' + engine + '\n</script>\n'
    name = 'two-minutes.%s.html' % lang
    io.open(name, 'w', encoding='utf-8').write(out)
    print('%-24s %.2f MB   %s / %s crossings / %s to driver'
          % (name, len(out.encode('utf-8')) / 1048576.0, fig['total'], fig['crossings'], fig['driver']))


EN_LINES = read_en_lines()
for lg in (sys.argv[1:] or ['es', 'fr', 'pt', 'de', 'ru']):
    build(lg)
