# -*- coding: utf-8 -*-
"""Write the closing card for every language the film is narrated in.

    python make_endcards.py

The card is drawn rather than generated because it is the one frame whose wording has
to be exact — the logo, the campaign line and the address. Only the words change between
languages, so they live here and the markup comes from endcard.html; keeping five
near-identical HTML files hand-edited is how one of them ends up saying something else.

The claim is the same in all of them and must stay that way: free for the fleet owner,
who receives the toll in full plus a share of the fee charged to the renter.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

CARDS = {
    'ru': {
        'title': 'End card (RU)',
        'slogan': 'Хватит терять.<br><em>Пора зарабатывать.</em>',
        'free': ('Бесплатно для владельцев парков.<br>\n'
                 '    Вы получаете <b>весь толл</b> — плюс <i>долю нашей комиссии</i>.'),
        'note': 'Wording is Russian as the narration says it: «толл», not a translation of it.',
    },
    'de': {
        'title': 'End card (DE)',
        'slogan': 'Schluss mit Verlieren.<br><em>Fangen Sie an zu verdienen.</em>',
        'free': ('Kostenlos für Flottenbetreiber.<br>\n'
                 '    Die <b>Maut ganz für Sie</b> — plus <i>ein Anteil unserer Gebühr</i>.'),
        'note': 'Sie-form throughout, as in the narration.',
    },
    'fr': {
        'title': 'End card (FR)',
        'slogan': 'Arrêtez de perdre.<br><em>Commencez à gagner.</em>',
        'free': ('Gratuit pour les loueurs.<br>\n'
                 '    <b>Le péage entier</b> pour vous — plus <i>une part de notre commission</i>.'),
        'note': 'Vouvoiement throughout, as in the narration.',
    },
    'pt': {
        'title': 'End card (PT)',
        'slogan': 'Pare de perder.<br><em>Comece a ganhar.</em>',
        'free': ('Grátis para donos de frota.<br>\n'
                 '    Você fica com o <b>pedágio inteiro</b> — mais <i>uma parte da nossa taxa</i>.'),
        'note': 'Brazilian Portuguese, as in the narration: pedágio, não portagem.',
    },
    'uk': {
        'title': 'End card (UK)',
        'slogan': 'Досить втрачати.<br><em>Час заробляти.</em>',
        'free': ('Безкоштовно для власників парків.<br>\n'
                 '    Ви отримуєте <b>весь толл</b> — плюс <i>частку нашої комісії</i>.'),
        'note': 'Ukrainian as the narration says it: «толл», not a translation of it.',
    },
    'tr': {
        'title': 'End card (TR)',
        'slogan': 'Kaybetmeyi bırakın.<br><em>Kazanmaya başlayın.</em>',
        'free': ('Filo sahipleri için ücretsiz.<br>\n'
                 '    <b>Geçiş ücretinin tamamı</b> sizin — artı <i>komisyonumuzdan bir pay</i>.'),
        'note': 'Siz-form throughout, as in the narration.',
    },
    'zh': {
        'title': 'End card (ZH)',
        'slogan': '别再亏损。<br><em>开始赚钱。</em>',
        'free': ('车队东主免费。<br>\n'
                 '    <b>过路费全额归您</b> — 再加 <i>我们佣金的一部分</i>。'),
        'note': 'Simplified Chinese; one recording serves both written forms.',
    },
    'hy': {
        'title': 'End card (HY)',
        'slogan': 'Բավական է կորցնել։<br><em>Ժամանակն է վաստակելու։</em>',
        'free': ('Անվճար ավտոպարկերի սեփականատերերի համար։<br>\n'
                 '    Դուք ստանում եք <b>ամբողջ վճարը</b> — գումարած <i>մեր միջնորդավճարի մասը</i>։'),
        'note': 'Eastern Armenian, and the Armenian full stop, which is not a Latin one.',
    },
    'ka': {
        'title': 'End card (KA)',
        'slogan': 'საკმარისია დანაკარგები.<br><em>დროა გამოიმუშაოთ.</em>',
        'free': ('უფასოა ავტოპარკის მფლობელებისთვის.<br>\n'
                 '    <b>მთელი გადასახადი</b> თქვენია — პლუს <i>ჩვენი საკომისიოს წილი</i>.'),
        'note': 'Georgian has no upper case; the display face carries the weight instead.',
    },
    'fa': {
        'title': 'End card (FA)',
        'slogan': 'دیگر ضرر نکنید.<br><em>درآمد را شروع کنید.</em>',
        'free': ('برای صاحبان ناوگان رایگان است.<br>\n'
                 '    <b>کل عوارض</b> مال شماست — به‌علاوه <i>سهمی از کارمزد ما</i>.'),
        'note': 'Right to left. Persian, in Naskh.',
    },
    'ur': {
        'title': 'End card (UR)',
        'slogan': 'نقصان اٹھانا بند کریں۔<br><em>کمانا شروع کریں۔</em>',
        'free': ('بیڑے کے مالکان کے لیے مفت۔<br>\n'
                 '    <b>پورا ٹول</b> آپ کا — ساتھ <i>ہماری فیس کا ایک حصہ</i>۔'),
        'note': 'Right to left, and in Nastaliq, which is what Urdu is read in.',
    },
    'uz': {
        'title': 'End card (UZ)',
        'slogan': 'Yoʻqotishni bas qiling.<br><em>Daromad topishni boshlang.</em>',
        'free': ('Avtopark egalari uchun bepul.<br>\n'
                 '    <b>Toʻlov toʻliq sizniki</b> — ustiga <i>komissiyamizdan ulush</i>.'),
        'note': ('Uzbek is the one cut nobody reads aloud: the voice is English and the '
                 'words on screen are Uzbek, so this card is Uzbek like the captions.'),
    },
}

# Right to left is a property of the script, not of the card, and it has to reach the
# markup: a browser given no direction lays Persian out left to right and puts the full
# stop at the wrong end of the line.
RTL = ('fa', 'ur')

source = io.open(os.path.join(HERE, 'endcard.html'), encoding='utf-8').read()
head, card = source.split('<div class="card">', 1)

for lang, copy in CARDS.items():
    text = head.replace('<title>End card</title>', '<title>%s</title>' % copy['title'])
    text = text.replace(
        ' * The closing card the generator cannot be trusted to draw.',
        ' * The closing card the generator cannot be trusted to draw — %s.\n *\n * %s'
        % (lang.upper(), copy['note']))
    text += ('<div class="card lang-%s"%s>\n' % (lang, ' dir="rtl"' if lang in RTL else '')
             + '  <img class="logo" src="logo-alpha.png" alt="MyEZToll">\n'
             '  <div class="rule"></div>\n'
             '  <div class="slogan">%s</div>\n'
             '  <div class="free">%s</div>\n'
             '  <div class="url">myeztoll.com</div>\n'
             '</div>\n' % (copy['slogan'], copy['free']))
    out = os.path.join(HERE, 'endcard.%s.html' % lang)
    io.open(out, 'w', encoding='utf-8').write(text)
    print('wrote %s' % os.path.basename(out))

# The address is the one string that must never be translated or restyled.
for lang in CARDS:
    body = io.open(os.path.join(HERE, 'endcard.%s.html' % lang), encoding='utf-8').read()
    assert re.search(r'class="url">myeztoll\.com<', body), lang
print('every card carries the address unchanged')
