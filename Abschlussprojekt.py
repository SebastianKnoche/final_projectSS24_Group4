import pandas as pd
import matplotlib.pyplot as plt

# Speichere den relativen Pfad und den Dateinamen der Quelle 
file_besucher = 'data/besucher.csv'
file_geo = 'data/geo.txt'
file_kunden = 'data/kunden.csv'

# Importiere Daten aus der Quelle in Dataframes
df_besucher = pd.read_csv(file_besucher, sep=";", decimal=',')
df_geo = pd.read_table(file_geo, decimal='.')
df_kunden = pd.read_csv(file_kunden, sep=";", decimal='.')

# Ersetze alle Instanzen von "NRW" in der Spalte "Niederlassung" mit "Nordrhein-Westfalen"
df_geo['Niederlassung'] = df_geo['Niederlassung'].apply(lambda x: 'Nordrhein-Westfalen' if 'NRW' in x else x)
# Ersetze alle Einträge, die "Berlin" in der Spalte "Niederlassung" enthalten, mit "Berlin"
df_geo['Niederlassung'] = df_geo['Niederlassung'].apply(lambda x: 'Berlin' if 'Berlin' in x else x)

# Berechne den Modus für die Werte in der Spalte "Geschlecht"
geschlecht_mode = df_kunden['Geschlecht'].mode()[0]
print("Der Modus ist " + str(geschlecht_mode))

# Ersetze alle leeren Einträge in der Spalte "Geschlecht" mit dem Modus der Werte in der Spalte "Geschlecht"
df_kunden['Geschlecht'].fillna(geschlecht_mode, inplace=True)
# Konvertiere die Spalte "Geschlecht" in den entsprechenden Integer-Datentyp
df_kunden['Geschlecht'] = df_kunden['Geschlecht'].astype(int)

# Berechnung von Q1 (25. Perzentil), Q3 (75. Perzentil) und IQR
Q1 = df_kunden['Einkommen'].quantile(0.25)
Q3 = df_kunden['Einkommen'].quantile(0.75)
IQR = Q3 - Q1

# Berechnung der Ausreißer-Grenzen
untere_grenze = Q1 - 1.5 * IQR
obere_grenze = Q3 + 1.5 * IQR

# Identifizierung von Ausreißern
df_kunden['Ausreißer'] = (df_kunden['Einkommen'] < untere_grenze) | (df_kunden['Einkommen'] > obere_grenze)

# Berechne den Median für die Werte in der Spalte "Einkommen"
eink_medianwert = df_kunden['Einkommen'].median()
print("Der Median ist " + str(eink_medianwert))

# Ersetze extreme Werte mit dem Median der Spalte "Einkommen"
df_kunden.loc[df_kunden['Ausreißer'] == True, 'Einkommen'] = eink_medianwert

# Zusammenführen von df_besucher und df_geo basierend auf KundeNr
df_besucher_geo = pd.merge(df_besucher, df_geo, on='KundeNr', how='left')

# Zusammenführen von df_kunden und df_geo basierend auf KundeNr
df_kunden_geo = pd.merge(df_kunden, df_geo, on='KundeNr', how='left')

# Zusammenführen von df_besucher_geo und df_kunden_geo basierend auf gemeinsamen Spalten
df_gesamt = pd.concat([df_besucher_geo, df_kunden_geo], ignore_index=True)

# Zeige die ersten Zeilen des finalen DataFrames an
print(df_gesamt.head())
