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
 ##  Použití
Uložte kód do souboru, například volby_scraper.py.
Otevřete terminál a přejděte do adresáře, kde je uložen váš skript.
Spusťte skript s URL a názvem výstupního CSV souboru jako argumenty:
bash
Run
Copy code
python volby_scraper.py <url_ke_scrapovani> <nazev_vystupniho_souboru.csv>
Příklad:
bash
Run
Copy code
python volby_scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_voleb_2017.csv
Po úspěšném spuštění skriptu by měl být vytvořen CSV soubor s názvem, který jste zadali.

## Struktura CSV souboru
CSV soubor bude obsahovat následující sloupce:

Cislo Obce: ID obce
Nazev Obce: Název obce
Pocet Volicu: Počet voličů
Pocet Obalek: Počet obálek
Pocet Validnich Obalek: Počet platných obálek
Hlasovací výsledky pro jednotlivé politické strany
## Příspěvky
Pokud máte návrhy na vylepšení nebo naleznete chyby, neváhejte přispět k projektu nebo otevřít issue.
