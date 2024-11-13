import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

all_data = []

# Przechodzenie przez konkretne regiony (na stronie wyszczególnione są 4)
# Można do finalnej tabeli dodać kolumne Region i wpisywać tam odpowiednią nazwę
for region in range(1, 5):
    page = 1
    while True:
        # warunek na blokowanie wczytaniu ostatnich stron w danym regionie
        if page == 5:
            break

            # Strona url zmienia w konkretnym miejscu liczbe region i strone
        url = f"https://www.e-drewno.pl/stock/?product=stock&module=auctions&action=showAuctions&options=all&region={region}&page={page}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page} for region {region}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        # tabela w html jest nazywana "okienko"
        table = soup.find("table", class_='okienko')
        if not table:
            print(f"Table not found on page {page} for region {region}. Moving to next region or stopping.")
            break

        tbody = table.find("tbody")
        data_rows = table.find_all("tr")[2:]

        for row in data_rows:
            cols = row.find_all("td")
            if len(cols) >= 11:
                data = {
                    "Lp": cols[0].text.strip(),
                    "RDLP": cols[1].text.strip(),
                    "Nadleśnictwo": cols[2].text.strip(),
                    "Nr aukcji": cols[3].text.strip(),
                    "Gr. handlowo-gatunkowa": cols[4].text.strip(),
                    "Zakończenie licytacji": cols[5].text.strip(),
                    "Ilość": cols[6].text.strip(),
                    "Ilość ofert złożonych/wygrywających": cols[7].text.strip(),
                    "Cena otwarcia netto": cols[8].text.strip(),
                    "Teraz wygrywa": cols[9].text.strip(),
                    "Do końca pozostało": cols[10].text.strip()
                }
                all_data.append(data)

        page += 1

df = pd.DataFrame(all_data)
df.to_csv("e_drewno_data.csv", index=False)
print("Data saved to e_drewno_data.csv")