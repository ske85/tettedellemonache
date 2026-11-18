# -*- coding: utf-8 -*-
"""
Sito "Dune di Altamura" su دونيدالتامورا.com (xn--mgbaakxar3mlevht.com), repository ske85/dune-ar.

Solo la pagina iniziale, in arabo (principale, "/") e inglese ("/en/").
Nessun riferimento al nome "tette delle monache" né alla pagina della storia.

Uso, dalla cartella principale di tettedellemonache:
    python3 _i18n/dune.py [cartella del repository dune-ar]
"""
import json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IT_ROOT = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(IT_ROOT), "dune-ar")
sys.path.insert(0, HERE)
import source  # noqa: E402
from build import strip_blocks, GLOBE  # noqa: E402

DOMAIN_U = "دونيدالتامورا.com"
DOMAIN_P = "xn--mgbaakxar3mlevht.com"
SITE = "https://" + DOMAIN_P
TODAY = "2026-11-18"

LANGS = {
    "ar": {"lang": "ar", "dir": "rtl", "og": "ar_AE", "path": "/", "name": "العربية", "short": "عربي", "label": "اللغة"},
    "en": {"lang": "en", "dir": "ltr", "og": "en_GB", "path": "/en/", "name": "English", "short": "EN", "label": "Language"},
}

T = {
    "ar": {
        "title": "Dune di Altamura — حلوى تقليدية من ألتامورا، إيطاليا — قريبًا",
        "desc": "Dune di Altamura: حلوى تقليدية من مدينة ألتامورا في منطقة بوليا جنوب إيطاليا، قبة إسفنجية خفيفة محشوة بالكريمة ومغطاة بالسكر الناعم. موقعنا قيد الإطلاق قريبًا.",
        "kw": "Dune di Altamura, حلويات إيطالية, حلوى إيطالية تقليدية, حلوى بالكريمة, حلويات بوليا, ألتامورا, مخبوزات إيطالية",
        "og_title": "Dune di Altamura — حلوى ألتامورا التقليدية",
        "og_desc": "خفيفة، كريمية، ومغطاة بالسكر الناعم كالثلج. موقعنا قيد الإطلاق قريبًا.",
        "org_desc": "Dune di Altamura: حلوى تقليدية من ألتامورا في منطقة بوليا الإيطالية.",
        "eyebrow": "<span class=\"eyebrow\">حلوى تقليدية من ألتامورا، إيطاليا</span>",
        "aria": "رسم لجبل صغير على شكل الحلوى، قمته مغطاة بالسكر الناعم كالثلج",
        "h1": "<h1>Dune di Altamura<br><em>قريبًا</em></h1>",
        "lead": "موقعنا قيد الإعداد: قريبًا ستجدون هنا Dune di Altamura، الحلوى التقليدية من مدينة ألتامورا في جنوب إيطاليا. قبة إسفنجية خفيفة كالهواء، محشوة بالكريمة ومغطاة بالسكر الناعم كأنها جبل صغير مكسوّ بالثلج.",
        "badge": "<span class=\"badge\">قيد الإنشاء</span>",
        "soon_t": "معلومات التواصل قريبًا",
        "soon_p": "نضع حاليًا اللمسات الأخيرة. قريبًا ستجدون هنا جميع المعلومات الخاصة بالمتاجر والموزّعين.",
        "privacy": "<a href=\"/privacy/\">الخصوصية</a>",
    },
    "en": {
        "title": "Dune di Altamura — Traditional pastry from Altamura, Italy — Coming soon",
        "desc": "Dune di Altamura: a traditional pastry from Altamura in Puglia, southern Italy. An airy sponge dome filled with custard and dusted with icing sugar. Our website is coming soon.",
        "kw": "Dune di Altamura, Italian pastry, traditional Italian pastry, cream pastry, Puglia desserts, Altamura, Italian bakery",
        "og_title": "Dune di Altamura — the traditional pastry of Altamura",
        "og_desc": "Airy, creamy and snowy with icing sugar. Our website is coming soon.",
        "org_desc": "Dune di Altamura: a traditional pastry from Altamura (Puglia, Italy).",
        "eyebrow": "<span class=\"eyebrow\">Traditional pastry from Altamura, Italy</span>",
        "aria": "A stylised mountain shaped like the pastry, its peak snowy with icing sugar",
        "h1": "<h1>Dune di Altamura<br><em>coming soon</em></h1>",
        "lead": "Our website is on its way: soon you will find here Dune di Altamura, the traditional pastry from the town of Altamura in southern Italy. An airy sponge dome, filled with custard and dusted with icing sugar like a small snow-capped mountain.",
        "badge": "<span class=\"badge\">Work in progress</span>",
        "soon_t": "Contact details coming soon",
        "soon_p": "We are putting the finishing touches in place. Information for retailers and distributors will be available here shortly.",
        "privacy": "<a href=\"/privacy/\">Privacy</a>",
    },
}

PRIVACY = {
    "ar": {
        "title": "الخصوصية — Dune di Altamura",
        "h1": "سياسة الخصوصية",
        "body": [
            ("الجهة المسؤولة", "Domenico Fraccalvieri — البريد الإلكتروني: <a href=\"mailto:tettedellemonache@outlook.com\">tettedellemonache@outlook.com</a>."),
            ("البيانات التي نعالجها", "هذا الموقع لا يجمع بيانات شخصية عبر النماذج، ولا يستخدم ملفات تعريف الارتباط (الكوكيز) ولا أدوات الإحصاء أو الإعلانات. تسجّل الخوادم التي تستضيف الموقع تلقائيًا بعض البيانات التقنية (مثل عنوان IP ونوع المتصفح ووقت الزيارة) لأغراض الأمان والتشغيل فقط."),
            ("الاستضافة", "يستضيف الموقع GitHub, Inc. (مجموعة Microsoft) في الولايات المتحدة، وفق الضمانات المنصوص عليها في اللائحة الأوروبية العامة لحماية البيانات (GDPR)."),
            ("حقوقكم", "يمكنكم في أي وقت طلب الاطلاع على بياناتكم أو تصحيحها أو حذفها بالكتابة إلى البريد الإلكتروني أعلاه، كما يحق لكم تقديم شكوى إلى هيئة حماية البيانات الإيطالية (Garante per la protezione dei dati personali)."),
        ],
        "updated": "آخر تحديث: 18 نوفمبر 2026",
        "back": "العودة إلى الرئيسية",
    },
    "en": {
        "title": "Privacy — Dune di Altamura",
        "h1": "Privacy notice",
        "body": [
            ("Data controller", "Domenico Fraccalvieri — email: <a href=\"mailto:tettedellemonache@outlook.com\">tettedellemonache@outlook.com</a>."),
            ("What data we process", "This website does not collect personal data through forms and does not use cookies, analytics or advertising tools. The servers hosting the site automatically record some technical data (such as IP address, browser type and time of visit) for security and operational purposes only."),
            ("Hosting", "The site is hosted by GitHub, Inc. (Microsoft group) in the United States, under the safeguards provided by the EU General Data Protection Regulation (GDPR)."),
            ("Your rights", "You may at any time ask to access, correct or delete your data by writing to the email address above, and you have the right to lodge a complaint with the Italian data protection authority (Garante per la protezione dei dati personali)."),
        ],
        "updated": "Last updated: 18 November 2026",
        "back": "Back to home",
    },
}

DUNE_CSS = """/* Dune di Altamura */
.langs{position:absolute;top:14px;right:14px;z-index:20;margin:0;font-family:"Instrument Sans",system-ui,sans-serif;font-size:.85rem;line-height:1.3;color:#4a3424}
.langs summary,.langs a{text-decoration:none!important}
.langs summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:999px;color:#4a3424;font-weight:600;background:rgba(255,255,255,.75);border:1px solid rgba(42,28,19,.14)}
.langs summary::-webkit-details-marker{display:none}
.langs summary:hover,.langs[open] summary{background:#fff}
.langs summary:focus-visible{outline:2px solid #c8994b;outline-offset:2px}
.langs ul{position:absolute;right:0;top:calc(100% + 6px);min-width:140px;list-style:none;margin:0;padding:6px;background:#fff;border:1px solid rgba(42,28,19,.12);border-radius:14px;box-shadow:0 12px 30px -12px rgba(42,28,19,.35)}
.langs li a{display:block;padding:8px 12px;border-radius:9px;color:#2a1c13}
.langs li a:hover{background:#f5efe4}
.langs li a[aria-current="page"]{font-weight:600;background:rgba(233,201,126,.3)}
.langs .vh{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
html[dir="rtl"] body{font-family:"Instrument Sans","Geeza Pro","SF Arabic","Noto Sans Arabic","Noto Naskh Arabic","Segoe UI","Tahoma",sans-serif;line-height:1.8}
html[dir="rtl"] h1,html[dir="rtl"] h2{font-family:"Fraunces","Geeza Pro","Noto Naskh Arabic","Amiri","Times New Roman",serif;letter-spacing:0}
html[dir="rtl"] em{font-style:normal}
html[dir="rtl"] .eyebrow{letter-spacing:0;text-transform:none;font-size:.88rem}
html[dir="rtl"] .langs{right:auto;left:14px}
html[dir="rtl"] .langs ul{right:auto;left:0;text-align:right}
html[dir="rtl"] .langs li a[lang="en"]{direction:ltr}
@media (max-width:560px){.langs{top:10px;right:10px}html[dir="rtl"] .langs{left:10px;right:auto}.langs ~ main{padding-top:68px}}
.privacy{max-width:680px;margin:0 auto;padding:64px 24px 40px;line-height:1.7;color:#2a1c13}
.privacy h1{font-family:"Fraunces",Georgia,serif;font-size:2rem;margin-bottom:6px}
.privacy h2{font-family:"Fraunces",Georgia,serif;font-size:1.15rem;margin:24px 0 6px}
.privacy .updated{color:#7a6553;font-size:.85rem}
.privacy a{color:#4a3424}
"""


def write(p, s, binary=False):
    full = os.path.join(OUT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f:
        f.write(s)


def hreflang(page_suffix=""):
    out = [f'<link rel="alternate" hreflang="{c}" href="{SITE}{l["path"]}{page_suffix}">' for c, l in LANGS.items()]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{page_suffix}">')
    return "\n".join(out)


def switcher(code, page_suffix=""):
    items = []
    for c, l in LANGS.items():
        cur = ' aria-current="page"' if c == code else ""
        items.append(f'<li><a href="{l["path"]}{page_suffix}" hreflang="{c}" lang="{c}"{cur}>{l["name"]}</a></li>')
    l = LANGS[code]
    return (f'<details class="langs"><summary>{GLOBE}<span>{l["short"]}</span>'
            f'<span class="vh"> · {l["label"]}: {l["name"]}</span></summary><ul>' + "".join(items) + "</ul></details>")


def jsonld(code):
    t = T[code]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}{LANGS[code]['path']}",
             "name": "Dune di Altamura", "inLanguage": code, "publisher": {"@id": f"{SITE}/#org"}},
            {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Dune di Altamura",
             "url": f"{SITE}/", "logo": f"{SITE}/og.png", "description": t["org_desc"]},
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def home(code):
    src = source.HOME
    t = T[code]
    l = LANGS[code]
    html = strip_blocks(open(os.path.join(IT_ROOT, "index.html"), encoding="utf-8").read())
    # sezione: elimina il pulsante verso la storia
    html = re.sub(r'\s*<a class="soon-link"[^>]*>.*?</a>', "", html, flags=re.S)
    for k in ("title", "desc", "kw", "og_title", "og_desc", "eyebrow", "aria", "h1", "lead", "badge", "soon_t", "soon_p", "privacy"):
        if src[k] not in html:
            raise SystemExit(f"[dune/{code}] testo non trovato: {k}")
        html = html.replace(src[k], t[k])
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: jsonld(code), html, count=1, flags=re.S)
    html = html.replace('<html lang="it">', f'<html lang="{l["lang"]}" dir="{l["dir"]}">', 1)
    html = html.replace('content="it_IT"', f'content="{l["og"]}"')
    html = html.replace('<meta property="og:site_name" content="Tette delle Monache">', '<meta property="og:site_name" content="Dune di Altamura">')
    html = html.replace('<link rel="canonical" href="https://tettedellemonache.co/">',
                        f'<link rel="canonical" href="{SITE}{l["path"]}">\n' + hreflang() + '\n<link rel="stylesheet" href="/dune.css">')
    html = html.replace('<meta property="og:url" content="https://tettedellemonache.co/">', f'<meta property="og:url" content="{SITE}{l["path"]}">')
    html = html.replace("https://tettedellemonache.co/og.png", f"{SITE}/og.png")
    html = html.replace('</span> tettedellemonache.co ·', f'</span> {DOMAIN_U} ·')
    html = html.replace('href="/privacy/"', f'href="{l["path"]}privacy/"')
    html = html.replace("<body>\n", "<body>\n" + switcher(code) + "\n", 1)
    leftovers = [w for w in ("ette delle", "tettedellemonache.co", "/storia/", "nunsbreasts") if w.lower() in html.lower().replace("tettedellemonache@outlook.com", "")]
    if leftovers:
        raise SystemExit(f"[dune/{code}] riferimenti rimasti: {leftovers}")
    write(l["path"].lstrip("/") + "index.html", html)


def privacy(code):
    p = PRIVACY[code]
    l = LANGS[code]
    sections = "\n".join(f"  <h2>{h}</h2>\n  <p>{b}</p>" for h, b in p["body"])
    html = f"""<!DOCTYPE html>
<html lang="{l['lang']}" dir="{l['dir']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}{l['path']}privacy/">
{hreflang('privacy/')}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/dune.css">
<style>body{{margin:0;background:#f5efe4;font-family:"Instrument Sans",system-ui,sans-serif}}</style>
</head>
<body>
{switcher(code, 'privacy/')}
<main class="privacy">
  <h1>{p['h1']}</h1>
  <p class="updated">{p['updated']}</p>
{sections}
  <p style="margin-top:28px"><a href="{l['path']}">{p['back']}</a></p>
</main>
</body>
</html>
"""
    write(l["path"].lstrip("/") + "privacy/index.html", html)


def main():
    os.makedirs(OUT, exist_ok=True)
    for code in LANGS:
        home(code)
        privacy(code)
    for f in ("favicon.svg", "apple-touch-icon.png"):
        shutil.copy(os.path.join(IT_ROOT, f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(IT_ROOT, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    og = os.path.join(HERE, "og-dune.png")
    if os.path.exists(og):
        shutil.copy(og, os.path.join(OUT, "og.png"))
    write("dune.css", DUNE_CSS)
    write("CNAME", DOMAIN_P)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = []
    for c, l in LANGS.items():
        alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{a}" href="{SITE}{al["path"]}"/>' for a, al in LANGS.items())
        alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
        urls.append(f"  <url>\n    <loc>{SITE}{l['path']}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("llms.txt", f"""# Dune di Altamura — {DOMAIN_U}

> Dune di Altamura is a traditional pastry from Altamura (Puglia, southern Italy): an airy sponge dome filled with custard and dusted with icing sugar. The website is under construction.

## Pages

- [العربية]({SITE}/): home page in Arabic
- [English]({SITE}/en/): home page in English
- [Privacy]({SITE}/privacy/): no cookies, no forms
""")
    print("Fatto:", OUT)


if __name__ == "__main__":
    main()
