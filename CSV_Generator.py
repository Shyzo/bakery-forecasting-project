import pdfplumber
import pandas as pd
import re
from datetime import datetime
from meteostat import Stations, Daily

#extract sales data from PDF
def extract_data_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                #match lines with the expected format
                match = re.match(r"(\d{2}/\d{2}/\d{4})\s+([\d,]+)\s+([\d,]+)\s+0\s+0\s+(\d+)\s+([\d.,]+)\s+0", line)
                if match:
                    date = match.group(1)
                    nb_produit = match.group(2).replace(",", ".")
                    ca = match.group(3).replace(",", ".")
                    nb_client = match.group(4)
                    vente_moyenne = match.group(5).replace(",", ".")
                    data.append([date, float(nb_produit), float(ca), int(nb_client), float(vente_moyenne)])
    return data

#extract sales data from the two PDF reports
data_1 = extract_data_from_pdf("DATASET1.pdf")
data_2 = extract_data_from_pdf("DATASET3.pdf")

#combine and clean sales DataFrame
df_ventes = pd.DataFrame(data_1 + data_2, columns=["Date", "Nb_Produit", "CA", "Nb_Clients", "Vente_Moyenne"])
df_ventes = df_ventes.drop_duplicates()
df_ventes["Date"] = pd.to_datetime(df_ventes["Date"], dayfirst=True)

#add weather data using Meteostat
stations = Stations().nearby(48.1206, -1.3572)
station_id = stations.fetch(1).index[0]
start = df_ventes["Date"].min()
end = df_ventes["Date"].max()
df_meteo = Daily(station_id, start, end).fetch().reset_index()
df_meteo = df_meteo.rename(columns={
    "time": "Date",
    "tavg": "TempMoy",
    "prcp": "Precipitations"
})

#merge sales and weather data
df_merged = pd.merge(df_ventes, df_meteo, on="Date", how="left")

#drop unused columns
df_merged.drop(["snow", "wdir", "wspd", "wpgt", "pres", "tsun","tmin","tmax"], axis=1, inplace=True)

#delete lines with no sales
df_merged = df_merged[df_merged["Nb_Clients"] > 0]

#define realistic basket size limits
MIN_PANIER = 1.0   #no one leaves with less than 1 euro spent
MAX_PANIER = 50.0  #small retail store so higher than 50 euros average basket is unlikely

#remove noise
lignes_avant = len(df_merged)
df_merged = df_merged[(df_merged["Vente_Moyenne"] >= MIN_PANIER) &(df_merged["Vente_Moyenne"] <= MAX_PANIER)]
df_merged.drop("Vente_Moyenne", axis=1, inplace=True)

SEUIL_MIN_CA = 300#realistically no days with less than 300 euros of sales
df_merged = df_merged[df_merged["CA"] > SEUIL_MIN_CA].copy()
print("Lignes supprimees (noise) : " + str(lignes_avant - len(df_merged)))


#add weekday and month columns
df_merged["Jour_semaine"] = df_merged["Date"].dt.dayofweek  #0=monday, 6=sunday
df_merged["Mois"] = df_merged["Date"].dt.month
df_merged["Annee"] = df_merged["Date"].dt.year

#remove Christmas noise
noel_imprevisible = (df_merged["Date"].dt.month == 12) & (df_merged["Date"].dt.day >= 20)
df_merged = df_merged.drop(df_merged[noel_imprevisible].index)
df_final = df_merged

#Save final merged dataset to CSV
df_final.to_csv("SalesDATA.csv", index=False)