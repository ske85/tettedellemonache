# -*- coding: utf-8 -*-
"""
Generatore delle versioni in lingua del sito.

Uso (dalla cartella principale del sito):
    python3 _i18n/build.py

Cosa fa:
  1. legge le pagine italiane (index.html e storia/index.html), che restano la versione di riferimento;
  2. aggiunge a tutte le pagine i collegamenti hreflang e il selettore della lingua;
  3. crea /en/, /fr/, /es/, /pt/, /zh/, /ja/ sostituendo i testi italiani di source.py
     con le traduzioni dei file <lingua>.py;
  4. rigenera sitemap.xml e la sezione lingue di llms.txt.

La cartella _i18n inizia con "_" e quindi GitHub Pages non la pubblica.
"""
import importlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import source  # noqa: E402

SITE = "https://tettedellemonache.co"
TODAY = "2026-11-18"

# codice, attributo lang, og:locale, inLanguage, hreflang, nome nella propria lingua, sigla, home, storia
LANGS = [
    ("it", "it",      "it_IT", "it-IT",   "it",      "Italiano",  "IT", "/",    "/storia/"),
    ("en", "en",      "en_GB", "en",      "en",      "English",   "EN", "/en/", "/en/history/"),
    ("fr", "fr",      "fr_FR", "fr-FR",   "fr",      "Français",  "FR", "/fr/", "/fr/histoire/"),
    ("es", "es",      "es_ES", "es-ES",   "es",      "Español",   "ES", "/es/", "/es/historia/"),
    ("pt", "pt-PT",   "pt_PT", "pt-PT",   "pt",      "Português", "PT", "/pt/", "/pt/historia/"),
    ("zh", "zh-Hans", "zh_CN", "zh-Hans", "zh-Hans", "简体中文",   "中文", "/zh/", "/zh/history/"),
    ("ja", "ja",      "ja_JP", "ja-JP",   "ja",      "日本語",     "日本語", "/ja/", "/ja/history/"),
]
BY = {l[0]: l for l in LANGS}

HEAD_A, HEAD_B = "<!-- i18n:head -->", "<!-- /i18n:head -->"
SW_A, SW_B = "<!-- i18n:switch -->", "<!-- /i18n:switch -->"

GLOBE = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
         'stroke-width="1.7"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.7 2.6 15.3 0 18M12 3c-2.6 2.7-2.6 15.3 0 18"/></svg>')


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, s):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(s)


def strip_blocks(html):
    """Toglie i blocchi inseriti da una generazione precedente."""
    for a, b in ((HEAD_A, HEAD_B), (SW_A, SW_B)):
        html = re.sub(r"\n?[ \t]*" + re.escape(a) + r".*?" + re.escape(b), "", html, flags=re.S)
    return html


def head_block(page):
    idx = 7 if page == "home" else 8
    links = [f'<link rel="alternate" hreflang="{l[4]}" href="{SITE}{l[idx]}">' for l in LANGS]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{BY["it"][idx]}">')
    links.append('<link rel="stylesheet" href="/lang.css">')
    return HEAD_A + "\n" + "\n".join(links) + "\n" + HEAD_B


def switcher(page, code):
    idx = 7 if page == "home" else 8
    cur = BY[code]
    items = []
    for l in LANGS:
        attrs = f'href="{l[idx]}" hreflang="{l[4]}" lang="{l[1]}"'
        if l[0] == code:
            attrs += ' aria-current="page"'
        items.append(f'<li><a {attrs}>{l[5]}</a></li>')
    label = {"it": "Lingua", "en": "Language", "fr": "Langue", "es": "Idioma",
             "pt": "Idioma", "zh": "语言", "ja": "言語"}[code]
    cls = "langs langs-float" if page == "home" else "langs"
    return (SW_A + f'\n<details class="{cls}"><summary>{GLOBE}'
            f'<span>{cur[6]}</span><span class="vh"> · {label}: {cur[5]}</span></summary><ul>' + "".join(items) + "</ul></details>\n" + SW_B)


def inject(html, page, code):
    html = strip_blocks(html)
    # hreflang subito dopo il canonical
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
    home, story = l[7], l[8]
    html = html.replace('<html lang="it">', f'<html lang="{l[1]}">', 1)
    html = html.replace('content="it_IT"', f'content="{l[2]}"')
    html = html.replace('"inLanguage": "it-IT"', f'"inLanguage": "{l[3]}"')
    if page == "home":
        html = html.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}{home}">')
        html = html.replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}{home}">')
    else:
        html = html.replace(f"{SITE}/storia/", f"{SITE}{story}")
        html = html.replace(f'"item": "{SITE}/"', f'"item": "{SITE}{home}"')
    html = html.replace('href="/storia/"', f'href="{story}"')
    html = html.replace('href="/"', f'href="{home}"')
    return html


def check(html, label):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            raise SystemExit(f"[{label}] dati strutturati non validi: {e}")


def sitemap():
    pages = [("home", 7), ("storia", 8)]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for _, idx in pages:
        for l in LANGS:
            out.append("  <url>")
            out.append(f"    <loc>{SITE}{l[idx]}</loc>")
            out.append(f"    <lastmod>{TODAY}</lastmod>")
            for a in LANGS:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{a[4]}" href="{SITE}{a[idx]}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{BY["it"][idx]}"/>')
            out.append("  </url>")
    out.append("  <url>")
    out.append(f"    <loc>{SITE}/privacy/</loc>")
    out.append(f"    <lastmod>{TODAY}</lastmod>")
    out.append("  </url>")
    out.append("</urlset>")
    write("sitemap.xml", "\n".join(out) + "\n")


def llms():
    s = read("llms.txt")
    s = re.sub(r"\n## Lingue\n.*?(?=\n## |\Z)", "\n", s, flags=re.S).rstrip() + "\n"
    block = ["", "## Lingue", ""]
    for l in LANGS:
        block.append(f"- {l[5]}: [{SITE}{l[7]}]({SITE}{l[7]}) · [{SITE}{l[8]}]({SITE}{l[8]})")
    s = s.replace("\n## Contatti", "\n".join(block) + "\n\n## Contatti", 1)
    write("llms.txt", s)


def main():
    base = {"home": strip_blocks(read("index.html")), "storia": strip_blocks(read("storia/index.html"))}
    srcs = {"home": source.HOME, "storia": source.STORIA}
    paths = {"home": 7, "storia": 8}
    # italiano: solo hreflang e selettore
    for page in base:
        out = inject(base[page], page, "it")
        check(out, f"it/{page}")
        write(BY["it"][paths[page]].lstrip("/") + "index.html", out)
    # altre lingue
    for l in LANGS[1:]:
        mod = importlib.import_module(l[0])
        dsts = {"home": mod.HOME, "storia": mod.STORIA}
        for page in base:
            out = translate(base[page], srcs[page], dsts[page], page, l[0])
            out = inject(out, page, l[0])
            check(out, f"{l[0]}/{page}")
            write(l[paths[page]].lstrip("/") + "index.html", out)
    sitemap()
    llms()
    print("Fatto:", ", ".join(l[0] for l in LANGS))


if __name__ == "__main__":
    main()
