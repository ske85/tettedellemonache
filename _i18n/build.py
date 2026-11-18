# -*- coding: utf-8 -*-
"""
Generatore delle versioni in lingua.

  - Italiano      -> tettedellemonache.co   (questo repository)
  - Altre lingue  -> nunsbreasts.com        (repository ske85/nunsbreasts)
                     inglese nella pagina principale, poi /fr/ /es/ /pt/ /zh/ /ja/

Uso, dalla cartella principale di tettedellemonache:
    python3 _i18n/build.py [cartella del repository nunsbreasts]
(se non indicata: ../nunsbreasts)

Cosa fa:
  1. legge le pagine italiane (index.html, storia/index.html): restano la versione di riferimento;
  2. aggiunge a tutte le pagine i collegamenti hreflang (anche tra i due domini) e il selettore lingua;
  3. scrive le pagine tradotte nella cartella di nunsbreasts, con le risorse che servono
     (caratteri, icone, immagine social, robots.txt, sitemap.xml, llms.txt, CNAME);
  4. in tettedellemonache.co lascia, al posto delle vecchie /en/ /fr/ ..., pagine che reindirizzano;
  5. rigenera sitemap.xml e la sezione "Lingue" di llms.txt di tettedellemonache.co.

La cartella _i18n inizia con "_" e quindi GitHub Pages non la pubblica.
"""
import importlib, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IT_ROOT = os.path.dirname(HERE)
NB_ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(IT_ROOT), "nunsbreasts")
sys.path.insert(0, HERE)
import source  # noqa: E402

IT_SITE = "https://tettedellemonache.co"
NB_SITE = "https://nunsbreasts.com"
TODAY = "2026-11-18"

# codice, lang, og:locale, inLanguage, hreflang, nome, sigla, sito, home, storia
LANGS = [
    ("it", "it",      "it_IT", "it-IT",   "it",      "Italiano",  "IT",   IT_SITE, "/",    "/storia/"),
    ("en", "en",      "en_GB", "en",      "en",      "English (UK)", "EN", NB_SITE, "/",  "/history/"),
    ("us", "en-US",   "en_US", "en-US",   "en-US",   "English (US)", "US", NB_SITE, "/us/", "/us/history/"),
    ("fr", "fr",      "fr_FR", "fr-FR",   "fr",      "Français",  "FR",   NB_SITE, "/fr/", "/fr/histoire/"),
    ("es", "es",      "es_ES", "es-ES",   "es",      "Español",   "ES",   NB_SITE, "/es/", "/es/historia/"),
    ("pt", "pt-PT",   "pt_PT", "pt-PT",   "pt",      "Português", "PT",   NB_SITE, "/pt/", "/pt/historia/"),
    ("zh", "zh-Hans", "zh_CN", "zh-Hans", "zh-Hans", "简体中文",   "中文", NB_SITE, "/zh/", "/zh/history/"),
    ("ja", "ja",      "ja_JP", "ja-JP",   "ja",      "日本語",     "日本語", NB_SITE, "/ja/", "/ja/history/"),
    ("ar", "ar",      "ar_AE", "ar",      "ar",      "العربية",   "عربي", NB_SITE, "/ar/", "/ar/history/"),
]
BY = {l[0]: l for l in LANGS}
PAGES = {"home": 8, "storia": 9}
X_DEFAULT = "en"   # versione mostrata a chi non parla nessuna delle lingue

# vecchi indirizzi pubblicati su tettedellemonache.co che ora reindirizzano a nunsbreasts.com
OLD_IT_PATHS = {
    "en": ("/en/", "/en/history/"), "fr": ("/fr/", "/fr/histoire/"), "es": ("/es/", "/es/historia/"),
    "pt": ("/pt/", "/pt/historia/"), "zh": ("/zh/", "/zh/history/"), "ja": ("/ja/", "/ja/history/"),
}

HEAD_A, HEAD_B = "<!-- i18n:head -->", "<!-- /i18n:head -->"
SW_A, SW_B = "<!-- i18n:switch -->", "<!-- /i18n:switch -->"
GLOBE = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
         'stroke-width="1.7"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 2.6 15.3 0 18M12 3c-2.6 2.7-2.6 15.3 0 18"/></svg>')
LABEL = {"it": "Lingua", "en": "Language", "us": "Language", "fr": "Langue", "es": "Idioma", "pt": "Idioma",
         "zh": "语言", "ja": "言語", "ar": "اللغة"}
RTL = {"ar"}
# nomi alternativi nei dati strutturati, per le lingue che ne vogliono una versione diversa
ALT_NAMES = {
    "ar": '["Sospiri", "Sospiri pugliesi", "Sospiri di Altamura", "Sise delle monache", "حلوى راهبات ألتامورا"]',
}


def url(code, page):
    l = BY[code]
    return l[7] + l[PAGES[page]]


def read(root, p):
    with open(os.path.join(root, p), encoding="utf-8") as f:
        return f.read()


def write(root, p, s):
    full = os.path.join(root, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(s)


def strip_blocks(html):
    for a, b in ((HEAD_A, HEAD_B), (SW_A, SW_B)):
        html = re.sub(r"\n?[ \t]*" + re.escape(a) + r".*?" + re.escape(b), "", html, flags=re.S)
    return html


def head_block(page):
    links = [f'<link rel="alternate" hreflang="{l[4]}" href="{url(l[0], page)}">' for l in LANGS]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{url(X_DEFAULT, page)}">')
    links.append('<link rel="stylesheet" href="/lang.css">')
    return HEAD_A + "\n" + "\n".join(links) + "\n" + HEAD_B


def switcher(page, code):
    cur = BY[code]
    items = []
    for l in LANGS:
        href = l[PAGES[page]] if l[7] == cur[7] else url(l[0], page)
        attrs = f'href="{href}" hreflang="{l[4]}" lang="{l[1]}"'
        if l[0] == code:
            attrs += ' aria-current="page"'
        items.append(f'<li><a {attrs}>{l[5]}</a></li>')
    cls = "langs langs-float" if page == "home" else "langs"
    return (SW_A + f'\n<details class="{cls}"><summary>{GLOBE}'
            f'<span>{cur[6]}</span><span class="vh"> · {LABEL[code]}: {cur[5]}</span></summary><ul>'
            + "".join(items) + "</ul></details>\n" + SW_B)


def inject(html, page, code):
    html = strip_blocks(html)
    html = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + "\n" + head_block(page), html, count=1)
    if page == "home":
        html = html.replace("<body>\n", "<body>\n" + switcher(page, code) + "\n", 1)
    else:
        html = html.replace("</header>", switcher(page, code) + "\n</header>", 1)
    return html


def translate(html, src, dst, page, code):
    l = BY[code]
    missing = [k for k in src if k not in dst]
    if missing:
        raise SystemExit(f"[{code}/{page}] traduzioni mancanti: {missing}")
    for k in sorted(src, key=lambda k: -len(src[k])):
        if src[k] not in html:
            raise SystemExit(f"[{code}/{page}] testo italiano non trovato nella pagina: {k!r}")
        html = html.replace(src[k], dst[k])
    site, home, story = l[7], l[8], l[9]
    dir_attr = ' dir="rtl"' if code in RTL else ""
    html = html.replace('<html lang="it">', f'<html lang="{l[1]}"{dir_attr}>', 1)
    if code in ALT_NAMES:
        html = re.sub(r'"alternateName": \["Tette della monaca"[^\]]*\]', '"alternateName": ' + ALT_NAMES[code], html)
    html = html.replace('content="it_IT"', f'content="{l[2]}"')
    html = html.replace('"inLanguage": "it-IT"', f'"inLanguage": "{l[3]}"')
    html = html.replace(f"{IT_SITE}/og.png", f"{site}/og.png")
    if page == "home":
        html = html.replace(f'<link rel="canonical" href="{IT_SITE}/">', f'<link rel="canonical" href="{site}{home}">')
        html = html.replace(f'<meta property="og:url" content="{IT_SITE}/">', f'<meta property="og:url" content="{site}{home}">')
        html = html.replace(f'"@id": "{IT_SITE}/#sito",\n      "url": "{IT_SITE}/",',
                            f'"@id": "{site}/#site",\n      "url": "{site}{home}",')
        html = html.replace(f'"sameAs": ["https://dunedialtamura.com/"', f'"sameAs": ["{NB_SITE}/", "https://dunedialtamura.com/"')
    else:
        html = html.replace(f"{IT_SITE}/storia/", f"{site}{story}")
        html = html.replace(f'"item": "{IT_SITE}/"', f'"item": "{site}{home}"')
    domain = site.replace("https://", "")
    html = html.replace('</span> tettedellemonache.co ·', f'</span> {domain} ·')
    html = html.replace('© 2026 tettedellemonache.co', f'© 2026 {domain}')
    html = html.replace('href="/privacy/"', f'href="{IT_SITE}/privacy/"')
    html = html.replace('href="/storia/"', f'href="{story}"')
    html = html.replace('href="/"', f'href="{home}"')
    return html


def check(html, label):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            raise SystemExit(f"[{label}] dati strutturati non validi: {e}")
    for old in ("tettedellemonache.co/en/", "tettedellemonache.co/fr/", "tettedellemonache.co/zh/"):
        if old in html:
            raise SystemExit(f"[{label}] è rimasto un vecchio indirizzo: {old}")


def sitemap(codes, extra=()):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES:
        for c in codes:
            out += ["  <url>", f"    <loc>{url(c, page)}</loc>", f"    <lastmod>{TODAY}</lastmod>"]
            for a in LANGS:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{a[4]}" href="{url(a[0], page)}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(X_DEFAULT, page)}"/>')
            out.append("  </url>")
    for u in extra:
        out += ["  <url>", f"    <loc>{u}</loc>", f"    <lastmod>{TODAY}</lastmod>", "  </url>"]
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def redirect_page(target, lang):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>nunsbreasts.com</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}");</script>
</head>
<body><p><a href="{target}">{target}</a></p></body>
</html>
"""


def it_llms():
    s = read(IT_ROOT, "llms.txt")
    s = re.sub(r"\n## Lingue\n.*?(?=\n## |\Z)", "\n", s, flags=re.S).rstrip() + "\n"
    block = ["", "## Lingue", "",
             "La versione italiana è su tettedellemonache.co; le altre lingue sono sul sito internazionale nunsbreasts.com.", ""]
    for l in LANGS:
        block.append(f"- {l[5]}: [{url(l[0], 'home')}]({url(l[0], 'home')}) · [{url(l[0], 'storia')}]({url(l[0], 'storia')})")
    s = s.replace("\n## Contatti", "\n".join(block) + "\n\n## Contatti", 1)
    write(IT_ROOT, "llms.txt", s)


def nb_llms():
    lines = [
        "# Tette delle Monache — nunsbreasts.com",
        "",
        "> International website of Tette delle Monache, the traditional pastry of Altamura (Puglia, southern Italy): "
        "a very light dome of sponge cake, filled with custard and dusted with icing sugar. The Italian name literally means "
        "\"nuns' breasts\" and refers to the pastry's shape and its convent origin. The website is under construction; "
        "the Italian version is at https://tettedellemonache.co/.",
        "",
        "Useful information:",
        "",
        "- Other names: tette della monaca, sospiri, sospiri pugliesi, sise delle monache (a similar pastry from Guardiagrele, Abruzzo).",
        "- Tradition links the pastry to the Poor Clare nuns and to the Monastery of Saint Clare in Altamura's old town.",
        "- Products, trade terms and contacts for retailers and distributors will be published soon.",
        "",
        "## Pages",
        "",
    ]
    for l in LANGS:
        lines.append(f"- {l[5]}: [{url(l[0], 'home')}]({url(l[0], 'home')}) · [{url(l[0], 'storia')}]({url(l[0], 'storia')})")
    lines += ["", "## Privacy", "", f"- [Privacy and cookies (Italian)]({IT_SITE}/privacy/): this site uses no cookies."]
    return "\n".join(lines) + "\n"


def main():
    if not os.path.isdir(NB_ROOT):
        raise SystemExit(f"Cartella di nunsbreasts non trovata: {NB_ROOT}")
    base = {p: strip_blocks(read(IT_ROOT, f)) for p, f in (("home", "index.html"), ("storia", "storia/index.html"))}
    srcs = {"home": source.HOME, "storia": source.STORIA}

    # 1. italiano
    for page in base:
        out = inject(base[page], page, "it")
        check(out, f"it/{page}")
        write(IT_ROOT, BY["it"][PAGES[page]].lstrip("/") + "index.html", out)

    # 2. altre lingue su nunsbreasts.com
    for l in LANGS[1:]:
        mod = importlib.import_module(l[0])
        dsts = {"home": mod.HOME, "storia": mod.STORIA}
        for page in base:
            out = translate(base[page], srcs[page], dsts[page], page, l[0])
            out = inject(out, page, l[0])
            check(out, f"{l[0]}/{page}")
            write(NB_ROOT, l[PAGES[page]].lstrip("/") + "index.html", out)

    # 3. risorse condivise per nunsbreasts.com
    for f in ("lang.css", "favicon.svg", "apple-touch-icon.png"):
        shutil.copy(os.path.join(IT_ROOT, f), os.path.join(NB_ROOT, f))
    shutil.copytree(os.path.join(IT_ROOT, "fonts"), os.path.join(NB_ROOT, "fonts"), dirs_exist_ok=True)
    og_nb = os.path.join(HERE, "og-nunsbreasts.png")
    if os.path.exists(og_nb):
        shutil.copy(og_nb, os.path.join(NB_ROOT, "og.png"))
    write(NB_ROOT, "CNAME", "nunsbreasts.com")
    write(NB_ROOT, "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {NB_SITE}/sitemap.xml\n")
    write(NB_ROOT, "sitemap.xml", sitemap([l[0] for l in LANGS[1:]]))
    write(NB_ROOT, "llms.txt", nb_llms())

    # 4. vecchie pagine su tettedellemonache.co -> reindirizzamento
    for code, (h, s) in OLD_IT_PATHS.items():
        for old, page in ((h, "home"), (s, "storia")):
            write(IT_ROOT, old.lstrip("/") + "index.html", redirect_page(url(code, page), BY[code][1]))

    # 5. sitemap e llms.txt italiani
    write(IT_ROOT, "sitemap.xml", sitemap(["it"], extra=[f"{IT_SITE}/privacy/"]))
    it_llms()
    print("Fatto. Italiano:", IT_ROOT, "| Internazionale:", NB_ROOT)


if __name__ == "__main__":
    main()
