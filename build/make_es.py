"""Build the Spanish cut: Spanish screens, Spanish on-screen copy, Spanish first.

The Spanish captures show different figures than the English ones ($100.89 over
15 crossings, $48.26 charged to the driver, $400.25 of owner income), so the
narration quotes those numbers instead — the voice must match the screen.
"""
import io
import json
import re

# ---- on-screen copy and the highlight boxes that differ from the English cut --
REPLACE = [
    # chrome labels
    ('<span>owner.myeztoll.com / toll transactions</span>',
     '<span>owner.myeztoll.com / transacciones de peaje</span>'),
    ('<span>owner.myeztoll.com / violations</span>',
     '<span>owner.myeztoll.com / infracciones</span>'),
    ('<span>charges</span>', '<span>cargos</span>'),
    ('<span>gps · trip map</span>', '<span>gps · mapa de viaje</span>'),
    ('<span>charge log</span>', '<span>registro de cargos</span>'),
    ('<span>account statement</span>', '<span>estado de cuenta</span>'),

    # S1
    ('<div class="eyebrow">One week · one small fleet</div>',
     '<div class="eyebrow">Una semana · una flota pequeña</div>'),
    ('style="left:0.4%;top:18.5%;width:15%;height:6.5%"',
     'style="left:0.4%;top:24%;width:17%;height:5.4%"'),
    ('<span class="num">$412.68</span> in a single week — <b>39 crossings</b>',
     '<span class="num">$100.89</span> en una sola semana — <b>15 pasos</b>'),
    ('Not one renter named on the statement.<br>So the owner absorbs it.',
     'Ni un solo cliente identificado en el extracto.<br>Lo acaba pagando el propietario.'),

    # S2
    ('<div class="eyebrow">Where the money goes</div>',
     '<div class="eyebrow">Adónde va el dinero</div>'),
    ('<p>Unmatched tolls<small>Nobody could prove who drove</small></p>',
     '<p>Peajes sin atribuir<small>Nadie pudo probar quién conducía</small></p>'),
    ('<p>Late violations<small>Published after the rental closed</small></p>',
     '<p>Multas tardías<small>Publicadas tras cerrar el alquiler</small></p>'),
    ('<p>Post-trip charges<small>Damage and fuel, found too late</small></p>',
     '<p>Cargos posteriores<small>Daños y combustible, hallados tarde</small></p>'),
    ('<p>Admin hours<small>Spreadsheets against statements</small></p>',
     '<p>Horas de administración<small>Hojas de cálculo contra extractos</small></p>'),
    ('style="left:58%;top:38%;width:41%;height:50%"',
     'style="left:39%;top:56%;width:29%;height:34%"'),

    # S3
    ('<div class="eyebrow">Every charge, matched</div>',
     '<div class="eyebrow">Cada cargo, emparejado</div>'),
    ('Car at the gantry, <b>to the second</b> — and the booking names the driver.',
     'El coche en el pórtico, <b>al segundo</b> — y la reserva identifica al conductor.'),
    ('style="left:4%;top:12%;width:34%;height:46%"',
     'style="left:60%;top:58%;width:22%;height:32%"'),

    # S4
    ('<div class="eyebrow">What it costs you</div>',
     '<div class="eyebrow">Lo que le cuesta a usted</div>'),
    ('<div class="big" data-cue="0" data-cue-offset="0.3">Free</div>',
     '<div class="big" data-cue="0" data-cue-offset="0.3">Gratis</div>'),
    ('No contract, no minimum fleet, and no fee taken out of your rental income.',
     'Sin contrato, sin flota mínima y sin comisión sobre sus ingresos de alquiler.'),
    ('<span class="what">Subscription</span><span class="cost">FREE</span>',
     '<span class="what">Suscripción</span><span class="cost">GRATIS</span>'),
    ('<span class="what">Set-up and onboarding</span><span class="cost">FREE</span>',
     '<span class="what">Alta y puesta en marcha</span><span class="cost">GRATIS</span>'),
    ('<span class="what">Charge per vehicle</span><span class="cost">FREE</span>',
     '<span class="what">Cargo por vehículo</span><span class="cost">GRATIS</span>'),
    ('<span class="what">Connecting the GPS you already run</span><span class="cost">FREE</span>',
     '<span class="what">Conectar el GPS que ya utiliza</span><span class="cost">GRATIS</span>'),
    ('<span class="what">Toll &amp; violation recovery</span><span class="cost">FREE</span>',
     '<span class="what">Recuperación de peajes y multas</span><span class="cost">GRATIS</span>'),
    ('<span class="what">Our own telematics hardware</span><span class="cost">Optional · paid</span>',
     '<span class="what">Nuestro equipo de telemática</span><span class="cost">Opcional · de pago</span>'),

    # S5
    ('<div class="eyebrow">And it runs the other way</div>',
     '<div class="eyebrow">Y funciona al revés</div>'),
    ('style="left:33%;top:19%;width:16%;height:8%"',
     'style="left:35%;top:79%;width:15%;height:6.5%"'),
    ('<b>The renter</b> is charged — <span class="num">$106.82</span>, not you.',
     'Se cobra <b>al cliente</b> — <span class="num">$48.26</span>, no a usted.'),
    ('<b>Owner share</b> — income, on a fleet you already own.',
     '<b>Parte del propietario</b> — ingresos con la flota que ya tiene.'),

    # S6
    ('<div class="slogan" data-cue="0" data-cue-offset="0">Stop losing.<br><em>Start earning.</em></div>',
     '<div class="slogan" data-cue="0" data-cue-offset="0">Deje de perder.<br><em>Empiece a ganar.</em></div>'),
    ('>Free for fleet owners<', '>Gratis para propietarios de flotas<'),
    ('MyEZToll — book a demo and see it on your own fleet.',
     'MyEZToll — pida una demo y véalo en su propia flota.'),
    ('Aegis AG Soft LLC · New Jersey, USA · optional telematics hardware excepted',
     'Aegis AG Soft LLC · Nueva Jersey, EE. UU. · salvo el equipo de telemática opcional'),

    # poster
    ('<div class="kicker" id="posterRuntime">A film for fleet owners</div>',
     '<div class="kicker" id="posterRuntime">Para propietarios de flotas</div>'),
    ('<h2>Stop losing.<br><em>Start earning.</em></h2>',
     '<h2>Deje de perder.<br><em>Empiece a ganar.</em></h2>'),
    ('Two minutes on where your fleet leaks money — and why MyEZToll costs the owner nothing and pays a share back.',
     'Dos minutos sobre dónde pierde dinero su flota, y por qué MyEZToll no le cuesta nada al propietario y además le paga una parte.'),
    ('        Play with narration', '        Reproducir con narración'),
    ('<div class="fineprint">Narration &amp; subtitles · EN · ES · RU</div>',
     '<div class="fineprint">Narración y subtítulos · ES · EN · RU</div>'),

    # transport + chrome text
    ('<div class="chapter-name" id="chapterName">The leak</div>',
     '<div class="chapter-name" id="chapterName">La fuga</div>'),
    ('Screens are the real product, captured from a live owner account; plate numbers, names and contact details are redacted at source.',
     'Las pantallas son el producto real, capturadas de una cuenta de propietario; matrículas, nombres y datos de contacto están ocultos.'),
    ('<title>Two Minutes on Your Fleet</title>', '<title>Dos Minutos con Su Flota</title>'),
]

SCENES = '''  var SCENES = [
    { chapter:"La fuga", dur:20, cues:[
      {t:0,    es:"Esto es una semana de peajes en una sola flota pequeña.",
               en:"This is one week of tolls on a single small fleet.",
               ru:"Это одна неделя толлов на одном небольшом парке."},
      {t:4.5,  es:"Cien dólares con ochenta y nueve centavos, en quince pasos.",
               en:"A hundred dollars and eighty-nine cents, across fifteen crossings.",
               ru:"Сто долларов восемьдесят девять центов за пятнадцать проездов."},
      {t:10,   es:"La pregunta nunca es cuánto costó. Es quién lo paga.",
               en:"The question is never what it cost. It is who pays it.",
               ru:"Вопрос не в том, сколько это стоило. Вопрос — кто платит."},
      {t:15.5, es:"Si no puede identificar al cliente, lo paga usted.",
               en:"If you cannot name the renter, you do.",
               ru:"Если вы не можете назвать арендатора, платите вы."}
    ]},

    { chapter:"Cuatro fugas", dur:22, cues:[
      {t:0,    es:"Y los peajes son solo la primera fuga.",
               en:"And tolls are only the first leak.",
               ru:"И толлы — лишь первая течь."},
      {t:4.5,  es:"Las multas de cámara se publican semanas después, con el alquiler ya cerrado.",
               en:"Camera violations publish weeks late, after the rental has closed.",
               ru:"Штрафы с камер публикуются на недели позже, когда аренда уже закрыта."},
      {t:11,   es:"Los daños y el combustible aparecen cuando el conductor ya se fue.",
               en:"Damage and fuel surface once the driver is gone.",
               ru:"Повреждения и топливо всплывают, когда водителя уже нет."},
      {t:16.5, es:"Y su personal quema horas cuadrando extractos con reservas.",
               en:"And your staff burn hours matching statements to bookings.",
               ru:"А сотрудники жгут часы, сверяя выписки с бронями."}
    ]},

    { chapter:"Deje de perder", dur:24, cues:[
      {t:0,    es:"MyEZToll cierra las cuatro.",
               en:"MyEZToll closes all four.",
               ru:"MyEZToll закрывает все четыре."},
      {t:3.8,  es:"El GPS sitúa el coche en el pórtico; la reserva identifica al conductor.",
               en:"GPS puts the car at the gantry; the booking names the driver.",
               ru:"GPS ставит машину у рамки, а бронь называет водителя."},
      {t:10.5, es:"Las multas se rastrean noventa días atrás; ninguna caduca sin facturar.",
               en:"Violations are chased ninety days back, so none expire unbilled.",
               ru:"Штрафы отслеживаются на девяносто дней назад — ни один не истечёт невыставленным."},
      {t:17.5, es:"Y cada cargo llega automáticamente a la tarjeta del cliente.",
               en:"Every charge then lands on the renter's card automatically.",
               ru:"И каждое начисление автоматически уходит на карту арендатора."}
    ]},

    { chapter:"Es gratis", dur:26, cues:[
      {t:0,    es:"¿Y cuánto le cuesta la plataforma? Nada.",
               en:"So what does the platform cost you? Nothing.",
               ru:"А сколько стоит сама платформа? Ничего."},
      {t:4.5,  es:"Sin suscripción. Sin coste de alta. Sin cargo por vehículo.",
               en:"No subscription. No set-up fee. No charge per vehicle.",
               ru:"Никакой подписки. Никакой платы за подключение. Ни цента за машину."},
      {t:11,   es:"Conectar el GPS que ya utiliza también es gratis.",
               en:"Connecting the GPS you already run is free as well.",
               ru:"Подключение GPS, которым вы уже пользуетесь, тоже бесплатно."},
      {t:16.5, es:"La única opción de pago es nuestro propio equipo de telemática.",
               en:"The only paid option is our own telematics hardware.",
               ru:"Единственная платная опция — наше собственное оборудование телематики."},
      {t:21.5, es:"Todo lo demás sigue siendo gratis, mientras lo use.",
               en:"Everything else stays free, for as long as you use it.",
               ru:"Всё остальное остаётся бесплатным, пока вы этим пользуетесь."}
    ]},

    { chapter:"Le pagamos", dur:18, cues:[
      {t:0,    es:"Cobramos al conductor que realmente condujo, nunca a usted.",
               en:"We collect from the driver who actually drove — never from you.",
               ru:"Мы взыскиваем с водителя, который действительно ехал, — и никогда с вас."},
      {t:6.5,  es:"Y una parte de todo lo que recuperamos se le abona a usted.",
               en:"And a share of everything we recover is paid out to you.",
               ru:"А доля со всего, что мы взыскали, выплачивается вам."},
      {t:12.5, es:"Parte del propietario. Ingresos reales, con la flota que ya tiene.",
               en:"Owner share. Real income, on a fleet you already own.",
               ru:"Доля владельца. Реальный доход на парке, который у вас уже есть."}
    ]},

    { chapter:"Empiece gratis", dur:14, cues:[
      {t:0,    es:"Deje de perder. Empiece a ganar.",
               en:"Stop losing. Start earning.",
               ru:"Перестаньте терять. Начните зарабатывать."},
      {t:3.8,  es:"MyEZToll: gratis para los propietarios de flotas.",
               en:"MyEZToll — free for fleet owners.",
               ru:"MyEZToll — бесплатно для владельцев парков."},
      {t:8,    es:"Pida una demo y véalo funcionando en su propia flota.",
               en:"Book a demo, and see it running on your own fleet.",
               ru:"Запишитесь на демо и посмотрите, как это работает на вашем парке."}
    ]},
  ];
'''


def main():
    shell = io.open('two_min_shell.html', encoding='utf-8').read()
    for a, b in REPLACE:
        if a not in shell:
            raise SystemExit('not found in shell: ' + a[:70])
        shell = shell.replace(a, b, 1)

    # Spanish first in the subtitle picker
    shell = shell.replace(
        '      <option value="en">Subtitles · EN</option>\n'
        '      <option value="es">Subtítulos · ES</option>\n'
        '      <option value="ru">Субтитры · RU</option>',
        '      <option value="es">Subtítulos · ES</option>\n'
        '      <option value="en">Subtitles · EN</option>\n'
        '      <option value="ru">Субтитры · RU</option>', 1)

    engine_src = io.open('stop-losing-start-earning.html', encoding='utf-8').read()
    engine = re.search(r'<script>\n(.*)\n</script>', engine_src, re.S).group(1)
    start = engine.index('  var SCENES = [')
    end = engine.index('  var TOTAL =')
    engine = engine[:start] + SCENES + '\n' + engine[end:]

    # default to Spanish, and label the runtime in Spanish
    engine = engine.replace("  var lang = 'en', ccOn = true, voiceOn = true;",
                            "  var lang = 'es', ccOn = true, voiceOn = true;", 1)
    engine = engine.replace("var runtimeText = 'Sales film · '", "var runtimeText = 'Película · '", 1)
    engine = engine.replace("document.getElementById('posterRuntime').textContent = 'A film for fleet owners · '",
                            "document.getElementById('posterRuntime').textContent = 'Para propietarios de flotas · '", 1)

    shots = json.load(io.open('shots_es/shots.json', encoding='utf-8'))
    for k, v in shots.items():
        token = '__SHOT_%s__' % k
        if token not in shell:
            raise SystemExit('unused shot: ' + k)
        shell = shell.replace(token, v)
    left = re.findall(r'__SHOT_\w+__', shell)
    if left:
        raise SystemExit('unfilled placeholders: %s' % set(left))

    out = shell + '\n<script>\n' + engine + '\n</script>\n'
    io.open('dos-minutos-con-su-flota.html', 'w', encoding='utf-8').write(out)
    print('dos-minutos-con-su-flota.html  %.2f MB' % (len(out.encode('utf-8')) / 1048576.0))


main()
