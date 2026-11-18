# Versioni in lingua

Le pagine italiane (`index.html`, `storia/index.html`) sono la versione di riferimento.
Le versioni in inglese, francese, spagnolo, portoghese, cinese e giapponese vengono generate da qui.

## Come aggiornare

1. Modifica il testo nella pagina italiana.
2. Aggiorna la stessa voce in `source.py` (testo italiano identico) e nei file delle lingue (`en.py`, `fr.py`, `es.py`, `pt.py`, `zh.py`, `ja.py`).
3. Dalla cartella principale del sito esegui `python3 _i18n/build.py`.

Lo script si ferma con un messaggio se un testo italiano non si trova più nella pagina o se manca una traduzione.
Rigenera anche `sitemap.xml` e la sezione "Lingue" di `llms.txt`.

## Indirizzi

| Lingua | Home | Storia |
|---|---|---|
| Italiano | / | /storia/ |
| English | /en/ | /en/history/ |
| Français | /fr/ | /fr/histoire/ |
| Español | /es/ | /es/historia/ |
| Português (Portogallo) | /pt/ | /pt/historia/ |
| 简体中文 | /zh/ | /zh/history/ |
| 日本語 | /ja/ | /ja/history/ |

La pagina privacy esiste solo in italiano; nelle altre lingue il link lo indica.
