# Projektarbeit Klassifizierung von Unternehmensbeschreibungen

Yannick Maurer (68036) & Daniel Gauermann (71411)

## Projektbeschreibung

Die Plattform Yahoo Finance verfügt über eine Vielzahl von Informationen zu an der Börse gelisteter Unternehmen. 
Beispielsweise bietet die Plattform für jedes Unternehmen eine eigene Seite mit Unternehmensdaten und einer Beschreibung an. 
Ziel dieser Projektarbeit soll es sein, mithilfe der Unternehmensbeschreibungen eine Klassifizierung des jeweiligen Sektors des Unternehmens vorzunehmen. 
Dazu sollen verschiedene Modelle antrainiert und schließlich das Modell mit der höchsten Genauigkeit bestimmt werden.

## Erklärung zu den erstellten Dateien

In dem ersten Ordner sind die Spezifikationen des Projekts abgelegt. 
Ordner 2 enthält CSV, TXT und JSON-Dateien welche Ticker (Symbole) der betrachteten Börsen AMEX, NASDAQ, NYSE, FSE, London SE, Bolsa de Madrid, Tokyo SE und Toronto SE beinhalten. 
Diese Ticker werden anschließend verwendet, um Unternehmensbeschreibungen von Yahoo Finance herunterzuladen. 
Dazu werden die Ticker in einer entsprechenden URL von Yahoo Finance zusammen mit einer Länderabkürzung eingefügt.
Die Dateien in Ordner 2 wurden mithilfe der folgenden Links heruntergeladen bzw. die Börsen AMEX, NASDAQ und NYSE wurden mit einem Skript extrahiert, das ebenfalls im Ordner zur Verfügung steht.


- NASDAQ Tickers: https://www.advfn.com/nasdaq/nasdaq.asp?companies=
- NYSE Tickers: https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=
- AMEX Tickers: https://www.advfn.com/amex/americanstockexchange.asp?companies=
- Tokyo Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- Toronto Tickers: https://www.tsx.com/trading/market-data-and-statistics/market-statistics-and-reports/interlisted-companies
- Frankfurt (Xetra) Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- Bolsa de Madrid Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
- London Stock Exchange Tickers: https://stockmarketmba.com/listofstocksforanexchange.php


Das Notebook 3 läd die Unternehmensbeschreibungen von Yahoo Finance herunter. Dazu wird jede Liste in Ordner 2 eingelesen und separat heruntergeladen. 
Dieses separate Herunterladen wurde verwendet, da es weniger anfällig gegenüber Verbindungsproblemen ist.
Die heruntergeladenen JSON-Dateien werden schließlich in Ordner 4 gespeichert.
Am Ende des Notebooks 3 werden alle JSON-Dateien in Ordner 4 eingelesen und in einer einzigen JSON-Datei konsolidiert. 
Diese Datei "data_raw.json" befindet sich außerhalb aller Ordner und sie enthält 9856 Einträge.


Das Notebook 5 nimmt eine Datenbereinigung und -konsolidierung vor. Beispielsweise werden Unternehmenssektoren mit geringer Anzahl an Sektoren mit einer höheren Anzahl zugeordnet. 
Am Ende werden die verarbeiteten Daten in JSON-Datei "data_prep.json" gespeichert. Zur Übersicht: 9833 Unternehmensbeschreibungen verbleiben am Ende, die in 10 Sektoren eingeteilt sind. 

### Vergleich synchrones und asynchrones Skript zur Datenextraktion

Ordner 6 vergleicht zwei Methoden zur Datenbeschaffung. Dieser Vergleich ist nicht in der Projektspezifikation erwähnt, wurde allerdings durchgeführt, da am Ende des Projektes noch Ressourcen hierfür frei waren.
Die erste betrachtete Methode ist ein synchrones Skript, welches wie das Skript in Notebook 3 arbeitet. 
Die zweite Methode ein asynchrones Skript, das mithilfe der Libraries "Asyncio" und "Aiohttp" arbeitet.
Im Vergleich werden die Unternehmensbeschreibungen der Börse AMEX heruntergeladen, während die Laufzeit gemessen wird.
Im Abschnitt Ergebnisse werden die Laufzeiten vorgestellt und verglichen.

### Neuronale Netze

Ordner 7 enthält die neuronalen Netze, die für die Klassifizierung erstellt wurden. 
Beim Erstellen der neuronalen Netze wurde darauf geachtet, dass die Trainings-, Validierungs- und Testdatensätze gleichmäßig verteilt sind bezüglich ihrer Anzahl an Sektoren (stratified sampling).
Die Samples wurden in 80 % Trainings-Datensatz, 10 % Validierungs- und Test-Datensatz verteilt.
Notebook 1 betrachtet nur einen Sektor und versucht zu bestimmen, ob das betrachtete Unternehmen zu diesem Sektor gehört oder nicht (binäre Klassifizierung). 
Der betrachtete Sektor ist hierbei der Financial Services Sektor, da dieser über die meisten Werte verfügt. 
In Notebook 1 wird zunächst ein neuronales Netz mit den normalen Unternehmensbeschreibungen aus dem Datensatz "data_prep.json" antrainiert.
Anschließend wird ein weiteres neuronales Netz mit dem bereinigten und lemmatisierten Datensatz antrainiert.
Die Performanceverbesserung von den normalen Beschreibungen auf die lemmatisierten und gefilterten Beschreibungen (Stoppwörter) wird im Abschnitt Ergebnis behandelt.


Notebook 2 nimmt alle Sektoren zur Hand und versucht diese den Unternehmensbeschreibungen zuzuordnen (Sektor-Klassifizierung). 
Die neuronalen Netze in Notebook 2 arbeiten mit einem vortrainierten Eingangslayer, der gleichzeitig ein "token-based text embedding" vornimmt.
Anschließend wird, wie in Notebook 1, ein neuronales Netz mit dem Datensatz "data_prep.json" und dem lemmatisierten Datensatz "Unternehmen_preprocessed.json" antrainiert.


Notebook 3 verwendet kein vortrainiertes Netz und stattdessen einen Encoder. Ebenfalls wird ein Long Short-Term Memory (LSTM) Layer als Kurzzeitgedächtnis des Models verwendet.
Wieder werden zwei Modelle anhand der zwei Datensätze antrainiert und bewertet.


# Ergebnisse


## Data Retrieval


Das Data Retrieval funktioniert mit einem asynchrones Skript wesentlich schneller. 
Grund für diese Performanceverbesserung liegt in dem Connection-Sharing von Aiohttp und dem gleichzeiten Anfragen von Requests an Yahoo Finance.
Während eine Seite geladen wird, werden automatisch weitere Seiten angefragt. Diese gleichzeitigen Anfragen senkt erheblich die Dauer des Data Retrievals.
Interessanterweise scheitert beim asynchronen Skript ein Request der 717 gestellten auch nach mehrmaliger Ausführung und es verbleiben 286 erfolgreiche Requests. 
Vermutlich braucht dieser Request zu lange zu laden, da er bei dem asynchronen Skript mit Pausen beinhaltet ist.
Dieses Skript mit Pausen wartet 0,1 Sekunden bevor es den nächsten Request stellt. Das asynchrone Skript mit Pausen bietet die beste Möglichkeit, Daten von Yahoo Finance zu extrahieren.

| Data retrieval                | Synchronous Programming | Asynchronous Programming |      Asynchronous with breaks of 0.1 seconds       |
|:------------------------------|:-----------------------:|:------------------------:|:--------------------------------------------------:|
| Duration                      |       996 seconds       |        25 seconds        |                     72 seconds                     |
| Number of scraped requests    |      717 requests       |       717 requests       |                    717 requests                    |
| Number of successful requests |      287 requests       |       286 requests       |                    287 requests                    | 


## Klassifizierung

Die folgenden Tabellen zeigen die Ergebnisse der einzelnen Klassifizierungsmethoden: 

|                        | K-Nearest Neighbor | Random Forest | Nearest Centroid |
|:----------------------:|:------------------:|:-------------:|:----------------:|
|  rough_lemmatization   |       84,8 %       |    71,7 %     |      78,0 %      |
| explicit_lemmatization |       85,5 %       |    72,4 %     |      78,2 %      |


Die binäre Klassifizierung kann nicht mit den anderen Methoden verglichen werden. 
Sie zeigt allerdings, dass neuronale Netze imstande sind, sehr gute Genauigkeiten zu erreichen. 
Bei der Sektor-Klassifizierung schneidet das Model mit einem vortrainierten Layer und Tokenizer am besten ab. 
Wird kein vortrainiertes Modell verwendet, ist die Datenmenge zu gering, um ein neuronales Netz ausreichend für eine Sektor-Klassifizierung zu trainieren. 
Auch der LSTM Layer führt hierbei zu keiner signifikaten Performance Verbesserung.

| Accuracy scores on test dataset                   | Binary classification |
|:--------------------------------------------------|:---------------------:|
| rough_lemmatization                               |        98,8 %         |
| explicit_lemmatization                            |        99,1 %         |


| Accuracy scores on test dataset                   | Sector classification with pretrained tokenizer | Sector classification with encoder and LSTM layer |
|:--------------------------------------------------|:-----------------------------------------------:|:-------------------------------------------------:|
| rough_lemmatization                               |                     78,6 %                      |                      61,9 %                       | 
| explicit_lemmatization                            |                     83,1 %                      |                      65,8 %                       |



Als Ergebnis kann formuliert werden, dass die Cluster Methode K-Nearest Neighbor unter der erweiterten Vorverarbeitung (Filtern von Stoppwörtern und Lemmatisierung) die höchste Genauigkeit liefert. 
Damit kann die Problemfrage aus der Projektspezifikation mit der K-Nearest Neighbor Methode mit einer Genauigkeit von 85,5 % beantwortet werden.