# 01 Preprocessing

Dieses Notebook enthält die Vorverarbeitungsschritte. Zunächst werden Daten, die aufgrund zu weniger Instanzen nicht repräsentativ sind, aussortiert. 
Danach werden die Daten lemmatisiert und Stoppwörter (aus der Spacy-Datenbank) entfernt. Dieser Schritt findet in zwei verschiedenen Ausmaßen statt.
rough_lemmatization' in der JSON-Datei enthält eine einfache Version der Lemmatisierung. Nachdem jedoch eine andere Verarbeitung und Analyse des Datensatzes durchgeführt wurde, müssen zusätzliche Begriffe oder Inhalte herausgefiltert werden. Dazu gehören Fehler, die durch die Tokenisierung entstanden sind. Zum Beispiel werden einzelne Buchstaben von Krankheiten wie "Hepatitis B" herausgefiltert. Außerdem wurden aus der Beschreibung die Firmennamen herausgefiltert, da diese einen großen Einfluss auf die Klassifizierung haben, aber nichts mit der eigentlichen Branche zu tun haben.  
Diese zusätzlich verarbeiteten Daten werden im JSON als "explicit_lemmatization" gespeichert.
Zusätzlich wird eine zusätzliche "Datenbank" angelegt, um in den folgenden Schritten eine Suchmaschine generieren zu können.
Aufgrund der oft ungenauen Ergebnisse wurde auf die Verarbeitung mittels eines "Porter Stemers" verzichtet.

# 02 General information about the corpus and search engine

Dieses Notebook zeigt verschiedene Metriken über den Korpus. Es zeigt den Umfang und die Verteilung der verschiedenen Texte.
Darüber hinaus ermöglicht das Notebook die Suche von Wörtern, bzw. gibt aus in welchen Texten diese vorkommen. Diese Suchabfrage kann eine beliebige Anzahl von Wörtern enthalten und die Abfrage kann durch eine Vereinigungs- oder Schnittstellensuche optimiert werden.

# 03 TfIdf - most relevant words of the corpus

Um feststellen zu können, welche Wörter für die einzelnen Klassen am relevantesten sind, werden TfIdf-Werte verwendet. Dazu wird der Vektorisierer aus der Sklearn-Bibliothek verwendet. Dieser Vektor wird verwendet, um eine Liste mit allen Wörtern und ihren entsprechenden TfIdf-Werten zu erstellen. 
Das Notebook bietet die Eingabe einer Suchanfrage an. Die Abfrage kann mit einem einzelnen Wort arbeiten und den TfIdf-Wert des Wortes zurückgeben, sowie den Sektor, zu dem das Wort gehört (mit dem höchsten TfIdf-Wert). Dies ermöglicht die Zuordnung eines Wortes zu einem Sektor. 
Außerdem wird die TfIdf-Liste nach den höchsten TfIdf-Werten und den Sektoren sortiert. Dabei wird eine Liste mit den relevantesten Wörtern eines jeden Sektors angezeigt. So lässt sich feststellen, welche Wörter in einem bestimmten Sektor am wichtigsten sind. 

# 04 Classification

Der Kern des Projekts ist die Einordnung eines Textes in einen bestimmten Bereich. Dazu verwendet dieses Notebook zwei unterschiedlich vorverarbeitete Datensätze und drei verschiedene Klassifizierungsmethoden: K-Nearest Neighbors, Random Forest und nearest Centroid.
Um diesen Schritt automatisieren zu können, wird eine Klasse verwendet. Dies ermöglicht die Erstellung eines Leistungsmaßes für die beiden unterschiedlichen Datensätze, mit unterschiedlichen Klassifizierungsmethoden und unterschiedlichen Hyperparametern der Methode. 
Dieses Notebook ermöglicht den Vergleich der Leistung zwischen den verschiedenen Datensätzen. Darüber hinaus verdeutlicht die Visualisierung einer Konfusionsmatrix die Ergebnisse und ermöglicht den Vergleich der Klassifizierung zwischen den verschiedenen Bereichen. 

# 05 Most used words with visualization

Um die Ergebnisse von Notebook 03 zu untermauern und mehr über die Zusammensetzung der Texte aus den verschiedenen Sektoren zu erfahren, zählt dieses Notebook die am häufigsten vorkommenden Wörter in jedem Sektor. 
Diese Aufgabe wird mit Hilfe des Count Vectorizer aus der Sklearn-Bibliothek gelöst. 
Die folgende Tabelle hat die Form:

<br>
<p>|      Sektor     |      Sektor     |
<p>|-----------------|-----------------|.....
<p>| Wort | Zählwert | Wort | Zählwert |
<\br>
Sie zeigt die wichtigsten Wörter in absteigender Reihenfolge an. Die Anzahl der angezeigten Wörter kann variiert werden. Diese Tabelle zeigt in Kombination mit der Tabelle aus dem Notebook 03, wie sich die Texte der verschiedenen Bereiche zusammensetzen. So lässt sich nachvollziehen, welche Wörter einen Text aus dem Bereich Energie zu einem "Energietext" machen. 
Um dies visuell zu verdeutlichen, enthält das Notebook eine Word Cloud für jeden Sektor.

# 06 Thesaurus - Arbitrarily long texts

Dies ist ein weiteres interaktives Notebook. Anders als der Thesaurus aus 03 erlaubt es dieses Notizbuch, einen beliebig langen
Text einzugeben und ihn klassifizieren zu lassen. Es bietet die Möglichkeit, jede der zuvor gesehenen Klassifikationsmethoden sowie Hyperparameter zu verwenden. Mit einer maximalen Genauigkeit von ~85 % (siehe 03 TfIdf) liefert dieses Notebook eine ziemlich genaue Klassifizierung des gewünschten Textes.

Hinweis: Alle interaktiven Abfragen des Notizbuchs können durch einfaches Importieren der entsprechenden JSON-Daten verwendet werden. Es ist nicht notwendig, das gesamte Notebook auszuführen.
