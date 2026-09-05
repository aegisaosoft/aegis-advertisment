"""Assemble the two-minute cut: the shell markup + the proven player engine +
a fresh, half-length script + the inlined product screenshots."""
import io
import json
import re

from voice_defaults import adult_narrator, pitch_markup

SCENES = '''  var SCENES = [
    { chapter:"The leak", dur:20, cues:[
      {t:0,    en:"This is one week of tolls on a single small fleet.",
               es:"Esto es una semana de peajes en una sola flota pequeña.",
               ru:"Это одна неделя толлов на одном небольшом парке."},
      {t:4.5,  en:"Four hundred and twelve dollars, across thirty-nine crossings.",
               es:"Cuatrocientos doce dólares, en treinta y nueve pasos.",
               ru:"Четыреста двенадцать долларов за тридцать девять проездов."},
      {t:10,   en:"The question is never what it cost. It is who pays it.",
               es:"La pregunta nunca es cuánto costó. Es quién lo paga.",
               ru:"Вопрос не в том, сколько это стоило. Вопрос — кто платит."},
      {t:15.5, en:"If you cannot name the renter, you do.",
               es:"Si no puede identificar al cliente, lo paga usted.",
               ru:"Если вы не можете назвать арендатора, платите вы."}
    ]},

    { chapter:"Four leaks", dur:22, cues:[
      {t:0,    en:"And tolls are only the first leak.",
               es:"Y los peajes son solo la primera fuga.",
               ru:"И толлы — лишь первая течь."},
      {t:4.5,  en:"Camera violations publish weeks late, after the rental has closed.",
               es:"Las multas de cámara se publican semanas después, con el alquiler ya cerrado.",
               ru:"Штрафы с камер публикуются на недели позже, когда аренда уже закрыта."},
      {t:11,   en:"Damage and fuel surface once the driver is gone.",
               es:"Los daños y el combustible aparecen cuando el conductor ya se fue.",
               ru:"Повреждения и топливо всплывают, когда водителя уже нет."},
      {t:16.5, en:"And your staff burn hours matching statements to bookings.",
               es:"Y su personal quema horas cuadrando extractos con reservas.",
               ru:"А сотрудники жгут часы, сверяя выписки с бронями."}
    ]},

    { chapter:"Stop losing", dur:24, cues:[
      {t:0,    en:"MyEZToll closes all four.",
               es:"MyEZToll cierra las cuatro.",
               ru:"MyEZToll закрывает все четыре."},
      {t:3.8,  en:"GPS puts the car at the gantry; the booking names the driver.",
               es:"El GPS sitúa el coche en el pórtico; la reserva identifica al conductor.",
               ru:"GPS ставит машину у рамки, а бронь называет водителя."},
      {t:10.5, en:"Violations are chased ninety days back, so none expire unbilled.",
               es:"Las multas se rastrean noventa días atrás; ninguna caduca sin facturar.",
               ru:"Штрафы отслеживаются на девяносто дней назад — ни один не истечёт невыставленным."},
      {t:17.5, en:"Every charge then lands on the renter's card automatically.",
               es:"Y cada cargo llega automáticamente a la tarjeta del cliente.",
               ru:"И каждое начисление автоматически уходит на карту арендатора."}
    ]},

    { chapter:"It is free", dur:26, cues:[
      {t:0,    en:"So what does the platform cost you? Nothing.",
               es:"¿Y cuánto le cuesta la plataforma? Nada.",
               ru:"А сколько стоит сама платформа? Ничего."},
      {t:4.5,  en:"No subscription. No set-up fee. No charge per vehicle.",
               es:"Sin suscripción. Sin coste de alta. Sin cargo por vehículo.",
               ru:"Никакой подписки. Никакой платы за подключение. Ни цента за машину."},
      {t:11,   en:"Connecting the GPS you already run is free as well.",
               es:"Conectar el GPS que ya utiliza también es gratis.",
               ru:"Подключение GPS, которым вы уже пользуетесь, тоже бесплатно."},
      {t:16.5, en:"The only paid option is our own telematics hardware.",
               es:"La única opción de pago es nuestro propio equipo de telemática.",
               ru:"Единственная платная опция — наше собственное оборудование телематики."},
      {t:21.5, en:"Everything else stays free, for as long as you use it.",
               es:"Todo lo demás sigue siendo gratis, mientras lo use.",
               ru:"Всё остальное остаётся бесплатным, пока вы этим пользуетесь."}
    ]},

    { chapter:"You get paid", dur:18, cues:[
      {t:0,    en:"We collect from the driver who actually drove — never from you.",
               es:"Cobramos al conductor que realmente condujo, nunca a usted.",
               ru:"Мы взыскиваем с водителя, который действительно ехал, — и никогда с вас."},
      {t:6.5,  en:"And a share of everything we recover is paid out to you.",
               es:"Y una parte de todo lo que recuperamos se le abona a usted.",
               ru:"А доля со всего, что мы взыскали, выплачивается вам."},
      {t:12.5, en:"Owner share. Real income, on a fleet you already own.",
               es:"Participación del propietario. Ingresos reales, con la flota que ya tiene.",
               ru:"Доля владельца. Реальный доход на парке, который у вас уже есть."}
    ]},

    { chapter:"Start free", dur:14, cues:[
      {t:0,    en:"Stop losing. Start earning.",
               es:"Deje de perder. Empiece a ganar.",
               ru:"Перестаньте терять. Начните зарабатывать."},
      {t:3.8,  en:"MyEZToll — free for fleet owners.",
               es:"MyEZToll: gratis para los propietarios de flotas.",
               ru:"MyEZToll — бесплатно для владельцев парков."},
      {t:8,    en:"Book a demo, and see it running on your own fleet.",
               es:"Pida una demo y véalo funcionando en su propia flota.",
               ru:"Запишитесь на демо и посмотрите, как это работает на вашем парке."}
    ]},
  ];
'''


def main():
    engine_src = io.open('stop-losing-start-earning.html', encoding='utf-8').read()
    m = re.search(r'<script>\n(.*)\n</script>', engine_src, re.S)
    if not m:
        raise SystemExit('engine not found')
    engine = m.group(1)

    # swap in the shorter script
    start = engine.index('  var SCENES = [')
    end = engine.index('  var TOTAL =')
    engine = engine[:start] + SCENES + '\n' + engine[end:]

    # the two-minute cut has its own runtime label
    engine = engine.replace("var runtimeText = 'Sales film · '", "var runtimeText = 'Sales film · '", 1)

    # the narrator is an adult woman, whatever the engine source defaulted to
    engine = adult_narrator(engine, 'en')

    shell = io.open('two_min_shell.html', encoding='utf-8').read()
    shell = shell.replace('No renter名 on the statement.', 'No renter named on the statement.', 1)
    shell = pitch_markup(shell, 'en')

    shots = json.load(io.open('shots/shots.json', encoding='utf-8'))
    for k, v in shots.items():
        token = '__SHOT_%s__' % k
        if token not in shell:
            raise SystemExit('unused shot: ' + k)
        shell = shell.replace(token, v)
    left = re.findall(r'__SHOT_\w+__', shell)
    if left:
        raise SystemExit('unfilled shot placeholders: %s' % set(left))

    out = shell + '\n<script>\n' + engine + '\n</script>\n'
    io.open('two-minutes-on-your-fleet.html', 'w', encoding='utf-8').write(out)
    print('two-minutes-on-your-fleet.html  %.2f MB' % (len(out.encode('utf-8')) / 1048576.0))


main()
