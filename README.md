## Projektarbeit Klassifizierung von Unternehmensbeschreibungen

### Projektbeschreibung
Die Plattform Yahoo Finance verfügt über eine Vielzahl von Informationen zu an der Börse gelisteter Unternehmen. 
Beispielsweise bietet die Plattform für jedes Unternehmen eine eigene Seite mit Unternehmensdaten und einer Beschreibung an. 
Ziel dieser Projektarbeit soll es sein, mithilfe der Unternehmensbeschreibungen eine Klassifizierung des jeweiligen Sektors des Unternehmens vorzunehmen. 
Dazu sollen verschiedene Modelle antrainiert und schließlich das Modell mit der höchsten Genauigkeit bestimmt werden.

### Erklärung zu den erstellten Dateien
Ordner 1 erhält die Projektspezifikationen. Ordner 2 enthält CSV, TXT und JSON Dateien die Ticker von an Börsen gelisteter Unternehmen aufzählen. 
Diese Ticker werden anschließend verwendet, um Unternehmensbeschreibungen auf Yahoo Finance herunterzuladen. 
Die Dateien, die Tickerinformationen zu den Börsen enthalten, wurden von folgenden Links heruntergeladen. 

- NASDAQ Tickers: https://www.advfn.com/nasdaq/nasdaq.asp?companies=
- NYSE Tickers: https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=
- AMEX Tickers: https://www.advfn.com/amex/americanstockexchange.asp?companies=
- Tokyo Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- Toronto Tickers: https://www.tsx.com/trading/market-data-and-statistics/market-statistics-and-reports/interlisted-companies
- Frankfurt (Xetra) Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- Bolsa de Madrid Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- London Stock Exchange Tickers: https://stockmarketmba.com/listofstocksforanexchange.php

Die Ticker der Börsen NASDAQ, NYSE und AMEX wurden mit einem Script heruntergeladen und as JSON-Dateien gespeichert. 
Das Script steht ebenfalls im Ordner 2 zur Verfügung. In Ordner 2 sind ansonsten alle Dateien, die Listen mit Tickers der jeweiligen Börse enthalten. 


Das Notebook 3 läd die Unternehmensbeschreibungen herunter. Dazu wird jede Liste in Ordner 2 eingelesen und separat heruntergeladen. 
Dieses separate Herunterladen wurde verwendet, da es weniger anfällig gegenüber Verbindungsproblemen ist.
Die heruntergeladenen JSON-Dateien werden in Ordner 4 gespeichert.
Am Ende des Notebooks 3 werden alle JSON-Dateien in Ordner 4 eingelesen und in einer JSON-Datei konsolidiert. 
Diese Datei trägt den Namen "data_raw.json" und sie enthält 9856 Einträge.


Das Notebook 5 nimmt eine Datenbereinigung und -konsolidierung vor. Beispielsweise werden Unternehmenssektoren die zu wenig vorkommen zu anderen hinzugefügt. 
Am Ende werden die verarbeiteten Daten in JSON-Datei "data_prep.json" gespeichert. Zur Übersicht: 9833 Unternehmensbeschreibungen verbleiben am Ende, die in 10 Sektoren eingeteilt sind. 


Ordner 6 vergleicht zwei Methoden zur Datenbeschaffung. Die erste Methode ist ein synchrones Skript. 
Die zweite Methode ein asynchrones Skript, das mithilfe der Libraries "Asyncio" und "Aiohttp" arbeitet.
Im Vergleich werden die Unternehmensbeschreibungen der Börse AMEX heruntergeladen. Datei benötigt das synchrone Skript 16 Minuten und 36 Sekunden. 
Das asynchrone Skript benötigt für die gleiche Datenmenge gerade einmal 25 Sekunden (vergl. 2 Screenshots in diesem Ordner). 
Grund für diese Performanceverbesserung liegt in dem Connection-Sharing von Aiohttp und dem gleichzeiten Anfragen von Requests an Yahoo Finance.
Während eine Seite geladen wird, werden automatisch weitere Seiten angefragt. Diese gleichzeitigen Anfragen erhöhen erheblich die Dauer des Data Retrievals.


Ordner 7 enthält die neuronalen Netze, die für die Klassifizierung erstellt wurden. 
Notebook 1 betrachtet nur einen Sektor und versucht zu bestimmen, ob das betrachtete Unternehmen zu diesem Sektor gehört oder nicht. 
Der betrachtete Sektor ist hierbei der Financial Service Sektor. 
Notebook 2 nimmt alle Sektoren zur Hand und versucht diese den Unternehmensbeschreibungen zuzuordnen. 
Beim Erstellen der neuronalen Netze wurde darauf geachtet das die Trainings-, Validierungs- und Testdatensätze gleichmäßig verteilt sind in ihrer Anzahl an Sektoren 
(stratified sampling). Die Aufteilung der Samples ist auf 80 % Trainings-Datensatz, 10 % Validierungs- und Test-Datensatz gelegt.
Notebook 2 arbeitet mit einem vortrainierten Eingangslayer, der gleichzeitig ein token-based text embedding vornimmt. 
Notebook 3 verwendet kein vortrainiertes Netz und einen Long Short-Term Memory (LSTM) Layer. Dieser wird als Kurzzeitgedächtnis des Models verwendet. 

# Ergebnisse

## Data Retrieval

Das Data Retrieval funktioniert mit einem asynchrones Skript wesentlich schneller. 
Interessanterweise scheitert beim asynchronen Skript ein Request der 717 gestellten auch nach mehrmaliger Ausführung. 
Vermutlich braucht dieses zu lange zu laden, da es bei einem moderaten Stellen von Requests beinhaltet ist.
Dieses moderatere Stellen von Requests wird bereits bei einer Pause von 0,1 Sekunden zwischen den Requests erreicht. 

| Data retrieval                | Synchronous Programming | Asynchronous Programming |      Asynchronous with breaks of 0.1 seconds       |
|:------------------------------|:-----------------------:|:------------------------:|:--------------------------------------------------:|
| Duration                      |       996 seconds       |        25 seconds        |                     72 seconds                     |
| Number of scraped requests    |      717 requests       |       717 requests       |                    717 requests                    |
| Number of successful requests |      287 requests       |       286 requests       |                    287 requests                    | 


## Klassifizierung

Folgende Tabellen zeigen die Ergebnisse der einzelnen Klassifizierungsmethoden. 

|                         | K-Nearest Neighbor | Random Forest | Nearest Centroid |
| :---:                   | :---:              |     :---:     |      :---:       |
| rough_lemmatization     | 84,8 %             | 71,7 %        |  78,0 %          |
| explicit_lemmatization  | 85,5 %             | 72,4 %        |  78,2 %          |

Die Tabelle zeigt, dass die Cluster Methode K-Nearest Neighbor unter der erweiterten Vorverarbeitung die besten Ergebnisse liefert. 
Die Cluster Methode K-Nearest Neighbor würden wir für eine Klassifizierung verwenden. 
Die binäre Klassifizierung kann nicht mit den anderen Methoden verglichen werden. Sie zeigt allerdings, dass neuronale Netze imstande sind, sehr Accuracy Scores zu erreichen. 
Müsste man nur zwischen neuronalen Netzen entscheiden, so schneided die Sektor Klassifizierung mit einem vortrainierten Model am besten ab. 
Wird kein vortrainiertes Modell verwendet, ist die Datenmenge zu wenig, um das neuronale Netz ausreichend für eine Sektor Klassifizierung zu trainieren. Auch ein LSTM Layer führt hierbei zu keiner signifikaten Verbesserung.


| Accuracy scores on test dataset                 | Descriptions | Descriptions without stopwords and lemmatized |
|:------------------------------------------------|:------------:|:---------------------------------------------:|
| Binary classification                           |    0.9878    |                    0.9908                     | 
| Sector classification with pretrained tokenizer |    0.7862    |                    0.8308                     |
| Sector classification with LSTM layer           |    0.6191    |                    0.6575                     |
