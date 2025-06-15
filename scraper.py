import requests
import bs4 as bs
import csv
import sys

class ElectionScraper:
    """
    Třída pro scrapování dat o volbách z webu volby.cz.
    """
    def __init__(self):
        self.municipalities_data = []
        self.party_names = set()

    def scrape_municipality_list(self, url):
        """
        Scrapuje seznam obcí (jejich ID a názvy) z úvodní stránky.
        """
        print(f"Načítám seznam obcí z: {url}")
        try:
            page = requests.get(url, timeout=10)
            page.raise_for_status() # Vyvolá HTTPError pro špatné odpovědi (4xx nebo 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Chyba při načítání úvodní stránky: {e}")
            sys.exit(1)

        soup = bs.BeautifulSoup(page.text, 'html.parser')

        # Předpokládáme, že struktura stránek je konzistentní s vaším příkladem
        municipality_ids = [td.text for td in soup.find_all("td", class_="cislo")]
        municipality_names = [td.text for td in soup.find_all("td", class_="overflow_name")]

        if not municipality_ids or not municipality_names:
            print("Nenalezeny žádné obce na zadané URL. Zkontrolujte URL nebo strukturu stránky.")
            sys.exit(1)

        for i in range(len(municipality_ids)):
            self.municipalities_data.append({
                "Cislo Obce": municipality_ids[i],
                "Nazev Obce": municipality_names[i],
                "Pocet Volicu": "N/A",
                "Pocet Obalek": "N/A",
                "Pocet Validnich Obalek": "N/A",
                "PartyVotes": {}
            })
        print(f"Nalezeno {len(self.municipalities_data)} obcí.")

    def scrape_municipality_details(self, base_url):
        """
        Scrapuje detailní data pro každou obec.
        """
        print("\nZačínám stahovat detailní data pro každou obec...")
        for i, municipality in enumerate(self.municipalities_data):
            obec_id = municipality["Cislo Obce"]
            detail_url = f"{base_url.split('?')[0].replace('ps32', 'ps311')}?xjazyk=CZ&xkraj=12&xobec={obec_id}&xvyber=7103"
            
            print(f"Zpracovávám obec ID: {obec_id} ({i + 1}/{len(self.municipalities_data)})")

            try:
                response = requests.get(detail_url, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"  Chyba při načítání detailů pro obec {obec_id}: {e}. Přeskakuji.")
                continue

            soup = bs.BeautifulSoup(response.text, 'html.parser')

            # Načítání základních statistik obce
            municipality["Pocet Volicu"] = self._get_text_or_na(soup, "td", {"class": "cislo", "headers": "sa2"})
            municipality["Pocet Obalek"] = self._get_text_or_na(soup, "td", {"class": "cislo", "headers": "sa5"})
            municipality["Pocet Validnich Obalek"] = self._get_text_or_na(soup, "td", {"class": "cislo", "headers": "sa6"})

            # Načítání hlasů pro strany
            current_party_votes = {}
            
            # První tabulka
            party_names_1 = [s.text for s in soup.find_all("td", class_="overflow_name", headers="t1sa1 t1sb2")]
            party_votes_1 = [h.text.replace('\xa0', ' ') for h in soup.find_all("td", class_="cislo", headers="t1sa2 t1sb3")]
            self._update_party_votes(current_party_votes, party_names_1, party_votes_1)

            # Druhá tabulka
            party_names_2 = [s.text for s in soup.find_all("td", class_="overflow_name", headers="t2sa1 t2sb2")]
            party_votes_2 = [h.text.replace('\xa0', ' ') for h in soup.find_all("td", class_="cislo", headers="t2sa2 t2sb3")]
            self._update_party_votes(current_party_votes, party_names_2, party_votes_2)
            
            municipality["PartyVotes"] = current_party_votes
            self.party_names.update(current_party_votes.keys())
            
            print(f"  Úspěšně zpracována obec: {obec_id}")

    def _get_text_or_na(self, soup_obj, tag, attrs):
        """Pomocná funkce pro bezpečné získání textu elementu."""
        element = soup_obj.find(tag, attrs)
        return element.text.replace('\xa0', ' ') if element else "N/A"

    def _update_party_votes(self, current_party_votes_dict, names_list, votes_list):
        """Aktualizuje slovník hlasů pro strany."""
        for j, party_name in enumerate(names_list):
            if j < len(votes_list):
                current_party_votes_dict[party_name] = votes_list[j]
            else:
                current_party_votes_dict[party_name] = "N/A"

    def write_to_csv(self, output_filename):
        """
        Zapíše nasebraná data do CSV souboru.
        """
        headers = ["Cislo Obce", "Nazev Obce", "Pocet Volicu", "Pocet Obalek", "Pocet Validnich Obalek"]
        dynamic_party_headers = sorted(list(self.party_names))
        headers.extend(dynamic_party_headers)

        print(f"\nZapisuji data do souboru '{output_filename}'...")
        try:
            with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers, restval="0")
                writer.writeheader()

                for municipality in self.municipalities_data:
                    row_data = {
                        "Cislo Obce": municipality["Cislo Obce"],
                        "Nazev Obce": municipality["Nazev Obce"],
                        "Pocet Volicu": municipality["Pocet Volicu"],
                        "Pocet Obalek": municipality["Pocet Obalek"],
                        "Pocet Validnich Obalek": municipality["Pocet Validnich Obalek"]
                    }
                    row_data.update(municipality["PartyVotes"])
                    writer.writerow(row_data)
            print(f"Data byla úspěšně zapsána do souboru '{output_filename}'")
        except IOError as e:
            print(f"Chyba při zápisu do CSV souboru: {e}")
        except Exception as e:
            print(f"Nastala neočekávaná chyba při zápisu do CSV: {e}")

def main():
    if len(sys.argv) != 3:
        print("Použití: python nazev_skriptu.py <url_ke_scrapovani> <nazev_vystupniho_souboru.csv>")
        print("Příklad: python volby_scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_voleb_2017.csv")
        sys.exit(1)

    scrape_url = sys.argv[1]
    output_filename = sys.argv[2]

    if not output_filename.endswith(".csv"):
        output_filename += ".csv"

    scraper = ElectionScraper()
    scraper.scrape_municipality_list(scrape_url)
    scraper.scrape_municipality_details(scrape_url)
    scraper.write_to_csv(output_filename)

if __name__ == "__main__":
    main()