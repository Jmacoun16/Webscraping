# Webscraping
# Election Scraper

Tento projekt je Python skript pro scrapování dat o volbách z webové stránky [volby.cz](https://www.volby.cz). Skript shromažďuje informace o obcích a jejich volebních výsledcích a ukládá je do CSV souboru.

## Funkce

- Scrapování seznamu obcí včetně jejich ID a názvů.
- Scrapování detailních volebních výsledků pro každou obec.
- Uložení shromážděných dat do CSV souboru.

## Požadavky

- Python 3.x
- Knihovny:
  - `requests`
  - `beautifulsoup4`

## Instalace

1. Ujistěte se, že máte nainstalovaný Python 3.x.
2. Nainstalujte potřebné knihovny pomocí pip:
   ```bash
   pip install requests beautifulsoup4
