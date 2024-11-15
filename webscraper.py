import pandas as pd
import requests
from bs4 import BeautifulSoup
from substringfunc import find_substring_between
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
all_data = []

#Przechodzenie przez konkretne regiony (na stronie wyszczególnione są 4)
#Można do finalnej tabeli dodać kolumne Region i wpisywać tam odpowiednią nazwę
for region in range(1, 5):
    page = 1
    while True:
      #warunek na blokowanie wczytaniu ostatnich stron w danym regionie
      if page == 2:
        break

        #Strona url zmienia w konkretnym miejscu liczbe region i strone
      url = f"https://www.e-drewno.pl/stock/?product=stock&module=auctions&action=showAuctions&options=all&region={region}&page={page}"
      response = requests.get(url, headers=headers)
      response.encoding = 'utf-8'
      if response.status_code != 200:
          print(f"Failed to retrieve page {page} for region {region}")
          break

      soup = BeautifulSoup(response.text, 'html.parser')
      #tabela w html jest nazywana "okienko"
      table = soup.find("table",class_ = 'okienko')
      if not table:
          print(f"Table not found on page {page} for region {region}. Moving to next region or stopping.")
          break

      tbody = table.find("tbody")
      data_rows = table.find_all("tr")[2:]

      for row in data_rows:
          cols = row.find_all("td")
          #Tworzenie linkudo strony na której znajduje się większa ilość danych o aukcji
          link = row.find('a', href=True)
          link = link.get('href')
          full_path = "https://www.e-drewno.pl/stock/" + link
          full_path = full_path.replace('®', '&reg')
          response_2 = requests.get(full_path, headers=headers)
          if response_2.status_code != 200:
              print(f"Failed to retrieve specific data")
          soup_2 = BeautifulSoup(response_2.text, 'html.parser')
          table_2 = soup_2.find("table",class_ = 'okienko')
          cols_2 = table_2.find_all("td",class_ = 'aukcja_legend')
          table_table = table_2.find("table",class_ = 'okienko')
          text = table_2.text

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
                  "Do końca pozostało": cols[10].text.strip(),
                  "Opis aukcji": cols_2[0].text.strip(),
                  "Termin na podpisanie umowy": table_2.find("td",class_ = 'aukcja_legend_agreementdeadline').text.strip(),
                  "Termin odbioru drewna": cols_2[1].text.strip(),
                  "Tel. kontaktowy": cols_2[2].text.strip(),
                  "Przewidywany procentowy udział klas jakości i grubości": str(find_substring_between(text,"oferowanego drewna."))
              }
              all_data.append(data)

      page += 1

df = pd.DataFrame(all_data)
df.to_csv("e_drewno_data.csv", index=False)
print("Data saved to e_drewno_data.csv")