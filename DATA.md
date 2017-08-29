# Daten

Dokumentation der Datenmodelle, von Rohdaten über Datenbank bis hin zum Client. 

## Identifiers

**Gemeindekennzahl**

Die Gemeindekennzahl ist 5-stellig.
* 1. Stelle
  * 0 => Österreich
  * Bundesland in alphabetischer Reihenfolge und entspricht der [ISO 3166-2:AT](https://de.wikipedia.org/wiki/ISO_3166-2:AT).
* 2-3. Stelle
  * 00 => Bundesland. GKZ endet dann mit 00
  * zwei Zahlen, von 01 aufsteigend => Bezirk. GKZ endet dann mit 00.
  * Ziffer 2 ein Buchstabe => Regional-Wahlkreis. GKZ endet dann mit 000.
* 4-5. Stelle 
  * laufend von 01 startend sind die Gemeinden
  * 99 => Wahlkarte. Davor Zeichen für Bezirk oder Wahlkreis.

Beispiel:
3 25 21 = Rappottenstein
* 3 Niederösterreich
* 25 Bezirk Zwettl
* 21 Gemeinde Rappottenstein

Weitere Beispiele:
* Gemeinde: `10201` für Rust
* Bezirk: `10100` für Eisenstadt
* Bundesland: `10000` für Burgenland
* Regionalwahlkreis: `1a1000` für Burgenland Nord
* Wahlkarte: `1a299` für Burgenland Süd

**Kürzel Wahl**

Wird von uns selber definiert. Grundlage sind etablierte Kürzel, z. B. "nrw" für Nationalratswahl gefolgt von Jahresziffer => "nrw17".

* `nrw13`: Nationalratswahl 2013
* `nrw17`: Nationalratswahl 2017

**Kürzel Partei**

Von uns selber definiert. Grundlage sind etablierte Kürzel. Kürzel sind in der `parties.json` zu finden.


## Ergebnisdaten vom BMI

Zur Nationalratswahl 2017 bietet das BMI ausgewählten NutzerInnen die Ergebnisse in Echtzeit an. Es wird zum ersten Mal die Daten neben dem alt-ehrwürdigen TXT-Format auch als CSV und JSON Datei via https geben.

Einige Tage vor der Wahl (zw. 4 und 14 Tage) wird es eine Test-Wahl geben, wo die Ergebnisse der NRW13 in der aktuellen Struktur (also mit aktuellen Gemeinde-Daten), aber mit den alten Parteien, ausgeliefert werden.

Die Daten enthalten immer die zuletzt aktuelle und vorhandenen Ergebnisse. Es gibt zu jeder Gemeinde maximal einen Eintrag.

Es wird diese Mal abgeschätzte Daten geben, da Wahlkarten aus einem Regionalwahlkreis nicht klar einem Bezirk oder einer Gemeinde zugewiesen werden können. Daher werden je nach Bevölkerung gewichtet die RWK-Ergebnisse auf die Bezirke / Gemeinden aufgeteilt, jedoch ohne genau zu wissen, ob die Stimme wirklich aus dem/der jeweiligen Bezirk / Gemeinde gekommen ist.

**TXT**

Beachte: Reihenfolge der Parteien kann je nach Sprengel unterschiedlich sein.

**JSON**

**CSV**


## Basisdaten

Die Basis-Daten dienen zum Setup der App und als Datengrundlage, um die Ergebnisse passend visualisieren zu können.

### Gemeinden (2017-01-01)

Liste mit Gemeinden. `data/setup/municipalities_20170101.json`

Enthält alle Gemeinden Österreichs am Stichtag 1. 1. 2017. Ist die Grundlage für die Wahl-Stationen. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md#mitmachen).

Versionen:
* raw: CSV file `municipalities_20170101_1.csv`
* v1: angereichert mit Daten aus `municipalities_20170101_1.csv`

Liste mit allen Gemeinden Österreichs am Stichtag 1. Januar 2017. Diese Datei wird zum Setup von #NRW17 verwendet.

Attribute:
* district: Bezirks-Name
* municipality_code: Gemeinde-Code
* municipality_id: Gemeindekennzahl
* name: Name der Gemeinde
* regional_electoral_district: Kurzbezeichnung des Regionalwahlkreises, in dem die Gemeinde liegt (siehe `municipality2red_20170101.json`)
* state: Bundesland, in dem die Gemeinde liegt.

### Parteien

Liste der Parteien. `data/setup/parties.json`

Enthält alle Parteien die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md#mitmachen) erwünscht.

Key: Kürzel der Partei (short_name)

Attribute:
* full_name: Vollständiger Name der Partei
* short_name: Kürzel der Partei
* short_name_text: Kürzel der Partei in Text-Format
* family: Zugehörigkeit zur Partei-Familie (EU)
* wikidata_id: ID des zugehörigen Wikidata Items
* website: url zur offiziellen Website
* description: kurze Beschreibung der Partei

### Wahlwerbende Listen

Liste der wahlwerbenden Listen. `data/setup/lists.json`

Enthält alle Parteien die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md#mitmachen) erwünscht.

Key: Kürzel der Wahl (short_name)

Attribute:
* short_name: Kürzel der Partei
* full_name: Vollständiger Name der Partei
* short_name_text: Kürzel der Partei in Text-Format
* candidate_in: Liste an Bundesländern in denen kandidiert wird. 0 ist Österreichweit.
* party: zugehörige Partei.

### Wahlen

Liste mit Wahlen. `data/setup/elections.json`

Enthält alle Wahlen die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md#mitmachen) erwünscht.

Key: Kürzel der Wahl (short_name)

Attribute:
* full_name: Vollständige Bezeichnung der Wahl
* short_name: Kurzbezeichnung / Akronym der Wahl, zb. NRW17
* short_name_text: Kurzbezeichnung / Akronym der Wahl in Text-Format
* election_type: Art der Wahl, zB Präsidentenwahl, Nationalratswahl
* election_day: Wahltag, als `yyyy-mm-dd`
* administrative_level: federal, state, district oder municipal
* wikidata_id: Wikidate ID des dazugehörigen Items

### Mapping: Bundesland 2 Bezirk (2017-01-01)

Mapping von Bezirken zu jedem Bundesland. `data/setup/states-to-districts_20170101.json`

Enthält zu allen Bundesländern sämtliche enthaltene Bezirke am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md#mitmachen).

Attribute:
* NAME_DISTRICT: Bezirksname
* ID_DISTRICT: Ziffer für Bezirk (1-3 Stelle des Gemeinde-Codes, z.B. bei 91582 = 915)
* ID_STATE: Ziffer für Bundesland (erste Stelle des Gemeinde-Codes, z.B. bei 91582 = 9)
* NAME_STATE: Name Bundesland

Datenmodell:
```json
{
  "ID_STATE": {
    "name": "NAME_STATE
    "districts": {
        "ID_DISTRICT": "NAME_DISTRICT",
        "ID_DISTRICT": "NAME_DISTRICT",
        .
    }
  },
  .
}
```

### Mapping: Gemeinde 2 Regionalwahlkreis  (2017-01-01)

Mapping von Gemeinden zu den Regionalwahlkreisen. `data/setup/municipality2red_20170101.json`

Mapping aller Regionalwahlkreise mit den darin enthaltenen Gemeinden am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md#mitmachen).

Attribute:
* MUNICIPALITY_CODE: Gemeinde-Code
* SHORT_NAME: Kürzel für Regionalwahlkreis

Datenmodell:
```json
{
  "MUNICIPALITY_CODE": "SHORT_NAME",
  .
}
```

## postgreSQL

In die PostgreSQL-Datenbank werden Tabellen zu jeder Klasse aus `src/viz/models.py` angelegt. Am besten direkt in der Datei nachlesen, welche Daten gespeichert werden.

Tables:
* Election: Wahlen
* List: wahlwerbenden Listen
* RegionalElectoralDistrict: Regionalwahlkreise
* Party: Parteien
* PollingStation: Wahl-Station. Zumeist auf Gemeindeebene
* PollingStationResult: Ergebnisse auf Gemeindeebene (ohne Partei-Ergebnisse)
* PartyResult: Partei-Ergebnisse zu jeder Wahl-Station.
* RawData: Rohdaten
* District: Bezirke
* State: Bundesländer

## Test-Daten

### NRW2013 Ergebnisse

Ergebnisse der Nationalratswahl 2013 aufbereitet für die Gemeinden ( Stichtag 1. 1. 2017). `data/test/nrw_2013_1.json`

* raw: Rohdaten von Flooh Perlot
* v1: 
  * löschen folgender Attribute: m
  * ausbessern der Parteikürzel von: Piraten, Der Wandel, Team Stronach, 
  * Bei der Gemeindekennzahl das "G" entfernt

Attribute:
* MUNICIPALITY_CODE: Gemeindecode
* SHORT_PARTY_NAME: Kürzel der Partei
* VOTES: Zahl der Stimmen

Datenmodell:
```json
{
  "MUNICIPALITY_CODE": {
    "SHORT_PARTY_NAME": "VOTES",
    "SHORT_PARTY_NAME": "VOTES",
    .
  },
  .
}
```

### NRW2013 Mapping

Mapping der Keys aus `data/test/nrw_2013_1.json` auf den internen Standard.

`data/test/nrw_2013_mapping.json`

Standard-Werte:
* municipality_kennzahl: Gemeindekennzahl
* municipality_code: Gemeindecode
* invalid: ungültige Stimmen
* valid: gültige Stimmen
* votes: gesamte Stimmen
* timestamp: Zeitstempel
* eligible_voters: Anzahl wahlberechtigter Personen
* id: interne ID
* LIST_SHORT_NAME+ELECTION_SHORT_NAME: für die Listen

### Simuliertes Ergebnis-XML

Da das BMI vermutlich die Ergebnisse zum ersten Mal in einem neuen XML-Dateiformat ausliefert und wir noch nicht wissen wie diese aussieht, haben wir vorab selber eine Test-Datei erstellt um so die Funktionen implementieren und testen zu können. Um die sich ständig ändernden Ergebnis-Dateien an einem Wahlabend zu simulieren, wurden drei Versionen erstellt.

* `data/test/example_1.xml`
* `data/test/example_2.xml`
* `data/test/example_2.xml`

Die XML-Dateien sind mit dem selben Filenamen auch online unter [http://stefankasberger.at/wp-content/uploads/nrw17/](http://stefankasberger.at/wp-content/uploads/nrw17/) zu finden.

Folgende Ergebnisse sind darin enthalten:

**example_1.xml**

1. 41747: Vöcklamarkt
  * fehler: `eligible_voters` ist kleiner als `votes`
2. 80204: Bezau
  * fehler: summe der partei-stimmen ist nicht gleich `valid`
3. 70367: Wattens
  * alles korrekt
  * `gruene` ist ausreisser
  * `invalid` ist ausreisser
4. 30917: Hirschbach
  * alles korrekt
  * `timestamp` nach 17h

**example_2.xml**

1. gleich
2. Fehler korrigiert
3. gleich
4. gleich

### BMI Ergebnis-TXT 

* `data/test/example_1.txt`
* `data/test/example_2.txt`
* `data/test/example_3.txt`

### BMI Ergebnis-JSON 

## Frontend

Die Django-App liefert die benötigten Daten über eine restfull-API aus. Näheres dazu findet man unter [nrw17.offenewahlen.at/api](https://nrw17.offenewahlen.at/api)

### Geometrien (1. 1. 2017)

TopoJSON-Datei zu Österreich am Stichtag 1. Januar 2017.

`data/setup/municipalities_topojson_999_20170101.json`: 

## Datenquellen

Daten rund um Wahlen in Österreich sind hier zu finden: 
* [BMI Wahlen](http://www.bmi.gv.at/cms/BMI_wahlen/): offizielle Seite des Bundesinnenministeriums (der Bundeswahlbehörde) zu Wahlen.
* [BMI Parteienregister](http://www.bmi.gv.at/cms/bmi_service/parteienverz/start.aspx): Parteienregister des Bundesinnenministeriums.
* [data.gv.at](http://data.gv.at/): Open Data Portal des Bundes.
* [Regionalwahlkreise - Statistik Austria](https://www.statistik.at/web_de/klassifikationen/regionale_gliederungen/regionalwahlkreise/index.html): Regionalwahlkreis-Daten der Statistik Austria.



