# Projektarbeit Natural Language Processing

### Projektbeschreibung
Die Plattform Yahoo Finance verfügt über eine Vielzahl von Informationen zu an der Börse gelisteter Unternehmen. 
Beispielsweise bietet die Plattform für jedes Unternehmen eine eigene Seite mit Unternehmensdaten und einer Beschreibung an. 
Ziel dieser Projektarbeit soll es sein, mithilfe der Unternehmensbeschreibungen eine Klassifizierung des jeweiligen Sektors des Unternehmens vorzunehmen. 
Dazu sollen verschiedene Modelle antrainiert und schließlich das Modell mit der höchsten Genauigkeit bestimmt werden.

### Erklärung zu den erstellten Dateien
Ordner 1 erhält die Projektspezifikationen. Ordner 2 enthält CSV, TXT und JSON Dateien die Ticker von an Börsen gelisteter Unternehmen aufzählen. 
Diese Ticker werden anschließend verwendet, um Unternehmensbeschreibungen auf Yahoo Finance herunterzuladen. 
Die Dateien, die Tickerinformationen zu den Börsen enthalten, wurden von folgenden Links heruntergeladen. 

NASDAQ Tickers: https://www.advfn.com/nasdaq/nasdaq.asp?companies=
NYSE Tickers: https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=
AMEX Tickers: https://www.advfn.com/amex/americanstockexchange.asp?companies=
Tokyo Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
Toronto Tickers: https://www.tsx.com/trading/market-data-and-statistics/market-statistics-and-reports/interlisted-companies
Frankfurt (Xetra) Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
Bolsa de Madrid Tickers: https://stockmarketmba.com/listofstocksforanexchange.php
London Stock Exchange Tickers: https://stockmarketmba.com/listofstocksforanexchange.php

Die Ticker der Börsen NASDAQ, NYSE und AMEX wurden mit einem Script heruntergeladen und as JSON-Dateien gespeichert. 
Das Script steht ebenfalls im Ordner 2 zur Verfügung. In Ordner 2 sind ansonsten alle Dateien, die Listen mit Tickers der jeweiligen Börse enthalten. 


Das Notebook 3 läd die Unternehmensbeschreibungen herunter. Dazu wird jede Liste in Ordner 2 eingelesen und separat heruntergeladen. 
Dieses separate Herunterladen wurde verwendet, da es weniger anfällig gegenüber Verbindungsproblemen ist. 
Die einzelnen JSON Dateien der Börsen werden ebenfalls in dem Script konsolidiert. 
Die JSON-Datei mit Nummer 4 ist das finale Produkt des Notebooks 3 (Information Retrieval). 


Das Notebook 5 nimmt eine Datenbereinigung und -konsolidierung vor. Beispielsweise werden Unternehmenssektoren die zu wenig vorkommen zu anderen hinzugefügt. 
Am Ende werden die verarbeiteten Daten in JSON-Datei 6 gespeichert. Zur Übersicht: 9833 Unternehmensbeschreibungen verbleiben am Ende, die in 10 Sektoren eingeteilt sind. 


Ordner 7 vergleicht zwei Methoden zur Datenbeschaffung. Die erste Methode ist ein synchrones Skript. Die zweite Methode ein asynchrones Skript, mithilfe der Library "asyncio" und "aiohttp".
Im Vergleich werden die Unternehmensbeschreibungen der Börse AMEX heruntergeladen. Datei benötigt das synchrone Skript 16 Minuten und 36 Sekunden. 
Das asynchrone Skript benötigt für die gleiche Datenmenge gerade einmal 25 Sekunden (vergl. 2 Screenshots in diesem Ordner). 
Grund für diese Performanceverbesserung liegt in dem Connection Handover von aiohttp und dem gleichzeiten Stellen von Requests an Yahoo Finance. 


Ordner 8 enthält die neuronalen Netze, die für die Klassifizierung erstellt wurden. 
Das erste neuronale Netz betrachtet nur einen Sektor und versucht zu bestimmen, ob das betrachtete Unternehmen zu diesem Sektor gehört oder nicht.
Das zweite neuronale Netz nimmt alle Sektoren zur Hand und versucht diese den Unternehmensbeschreibungen zuzuordnen. 
Beim Erstellen der neuronalen Netze wurde darauf geachtet das die Trainings-, Validierungs- und Testdatensätze gleichmäßig verteilt sind in ihrer Anzahl an Sektoren. 


Das finale Notebook 9 nimmt eine Thema-Modellierung vor. Diese Thema-Modellierung bestimmt welche Anzahl an Sektoren optimal wäre.