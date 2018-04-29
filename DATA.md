# Daten

Dokumentation der Datenmodelle, von Rohdaten über Datenbank bis hin zum Client. 

## Identifiers

### Gemeindekennzahl

Die Gemeindekennzahl ist 5-stellig und eine offiziell verwendete Zahl mit der Gemeinden beschrieben werden.

1te Stelle
* = 0: Eintrag ist Gesamtergebnis für Österreich. GKZ ist 00000.
* 1-9: Eintrag ist ein Bundesland in alphabetischer Reihenfolge (entspricht der [ISO 3166-2:AT](https://de.wikipedia.org/wiki/ISO_3166-2:AT)).

2-3te Stelle
* = 00: Eintrag ist ein Bundesland. GKZ endet dann mit 00 auf Stelle 4-5.
* zwei Zahlen, von 01 aufsteigend: Eintrag ist eine Gemeinde oder ein Bezirk.
* Ziffer 2 ein Buchstabe: Eintrag ist ein Regional-Wahlkreis.

4-5te Stelle 
* zwei Zahlen, von 01 aufsteigend: Eintrag ist eine Gemeinde.
* 99: Eintrag ist eine Wahlkarte. Die Stellen 2-3 stehen dann für Bezirk oder Wahlkreis.

Beispiel:
32521 = Rappottenstein
* 3 Niederösterreich
* 25 Bezirk Zwettl
* 21 Gemeinde Rappottenstein

Weitere Beispiele:
* Gemeinde: `10201` für Rust
* Bezirk: `10100` für Eisenstadt
* Bundesland: `10000` für Burgenland
* Regionalwahlkreis: `1a1000` für Burgenland Nord
* Wahlkarte: `1a299` für Burgenland Süd


### Kürzel Wahl

Ein Kürzel, dass von uns selber zur Identifizierung der Wahl dient.

Aktuell verwendet:
* `nrw13`: Nationalratswahl 2013
* `nrw17`: Nationalratswahl 2017

### Kürzel Partei

Ein Kürzel, dass von uns selber zur Identifizierung einer Partei dient. Grundlage sind etablierte Kürzel. 

Beispiele
* `oevp`: Österreichische Volkspartei
* `spoe`: Sozialdemokratische Partei Österreichs

### Kürzel Wahlwerbende Liste

Ein Kürzel, dass von uns selber zur Identifizierung einer wahlwerbenden Liste dient. Grundlage sind etablierte Kürzel von Parteien, welche dann mit dem Kürzel der jeweiligen Wahl erweitert werden. 

Beispiele
* `oevp_nrw13`: Liste der Österreichischen Volkspartei bei der Nationalratswahl 2013
* `spoe_nrw17`: Liste der Sozialdemokratischen Partei Österreichs bei der Nationalratswahl 2017

## Wahlergebnisse vom Innenministerium

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

Liste mit Gemeinden. `data/base/municipalities_20170101.json`

Enthält alle Gemeinden Österreichs am Stichtag 1. 1. 2017. Dies ist die Grundlage für die Wahl-Stationen. 

Die Daten sind an sich komplett, falls Sie Fehler oder Verbesserungen finden aber bitte melden, siehe [mitmachen](README.md#mitmachen).

Versionen:
* raw: CSV file `municipalities_20170101_1.csv`
* v1: `municipalities_20170101_1.json`
* v2: `municipalities_20170101_2.json`

Attribute:
* district: Bezirks-Name
* municipality_code: Gemeinde-Code
* municipality_id: Gemeindekennzahl
* name: Name der Gemeinde
* regional_electoral_district: Kurzbezeichnung des Regionalwahlkreises, in dem die Gemeinde liegt (siehe `municipality2red_20170101.json`)
* state: Bundesland, in dem die Gemeinde liegt.

### Parteien

Liste der Parteien. `data/base/parties.json`

Enthält alle Parteien die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md#mitmachen) erwünscht.

Key: Kürzel der Partei (short_name)

Attribute:
* full_name: Vollständiger Name der Partei
* short_name: Kürzel der Partei
* short_name_text: Kürzel der Partei in Text-Format
* family: Zugehörigkeit zur Partei-Familie (EU)
* wikidata_id: ID des zugehörigen Wikidata Items
* website: url zur offiziellen Website

### Wahlwerbende Listen

Liste der wahlwerbenden Listen. `data/base/lists.json`

Enthält alle Listen die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md#mitmachen) erwünscht.

Key: Kürzel der Wahl (short_name)

Attribute:
* short_name: Kürzel der Partei
* full_name: Vollständiger Name der Partei
* short_name_text: Kürzel der Partei in Text-Format
* candidate_in: Liste an Bundesländern in denen kandidiert wird. 0 ist Österreichweit.
* party: zugehörige Partei.

### Wahlen

Liste mit Wahlen. `data/base/elections.json`

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
* status: Status der Wahl

### Mapping: Bundesland 2 Bezirk (2017-01-01)

Mapping von Bezirken zu jedem Bundesland. `data/base/states-to-districts_20170101.json`

Enthält zu allen Bundesländern sämtliche darin enthaltene Bezirke am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md#mitmachen).

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

Mapping von Gemeinden zu den Regionalwahlkreisen. `data/base/municipality2red_20170101.json`

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

### Geometrien (1. 1. 2017)

TopoJSON-Datei zu Österreich am Stichtag 1. Januar 2017.

`data/setup/municipalities_topojson_999_20170101.json`: 

## postgreSQL

In die PostgreSQL-Datenbank werden Tabellen zu jeder Klasse aus `src/viz/models.py` angelegt. Am besten direkt in der Datei nachlesen, welche Daten gespeichert werden.

Tables:
* Election: Wahlen
* RegionalElectoralDistrict: Regionalwahlkreise
* Party: Parteien
* List: Wahlwerbenden Listen
* State: Bundesländer
* District: Bezirke
* Municipality: Gemeinden
* PollingStation: Wahl-Station. Zumeist die Gemeinde.
* PollingStationResult: Ergebnisse auf Gemeindeebene (ohne Partei-Ergebnisse).
* ListResult: Ergebnisse der Listen zur jeweiligen Wahl-Station.
* RawData: Rohdaten

![Database model](https://raw.githubusercontent.com/OKFNat/offenewahlen-nrw17/master/docs/database-model.png)

[PNG](https://raw.githubusercontent.com/OKFNat/offenewahlen-nrw17/master/docs/database-model.png)

## Wahlen

### NRW2013

#### Ergebnisse

Ergebnisse der Nationalratswahl 2013 aufbereitet für die Gemeinden (Stichtag 1. 1. 2017). `data/results/nrw_2013_1_results.json`

* raw: Rohdaten von Flooh Perlot
* v1: 
  * löschen folgender Attribute: m
  * ausbessern der Parteikürzel von: Piraten, Der Wandel, Team Stronach, 
  * Bei der Gemeindekennzahl das "G" entfernt

Attribute:
* MUNICIPALITY_CODE: Gemeindecode oder Gemeindekennzahl
* VOTE_TYPE: Kürzel der Partei oder Typ der aggregierten Stimmen auf Wahl-Stations-Ebene.
* VOTES: Zahl der Stimmen


Datenmodell:
```json
{
  "MUNICIPALITY_CODE": {
    "VOTE_TYPE": "VOTES",
    "VOTE_TYPE": "VOTES",
    .
  },
  .
}
```

#### Mapping

Mapping der Keys aus `data/results/nrw13_config.json` auf den internen Standard.

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

## API 

Die Django-App wird die benötigten Daten ab dem Wahltag über eine restful-API ausliefern.

## Datenquellen

Daten rund um Wahlen in Österreich sind hier zu finden: 
* [BMI Wahlen](http://www.bmi.gv.at/cms/BMI_wahlen/): offizielle Seite des Bundesinnenministeriums (der Bundeswahlbehörde) zu Wahlen.
* [BMI Parteienregister](http://www.bmi.gv.at/cms/bmi_service/parteienverz/start.aspx): Parteienregister des Bundesinnenministeriums.
* [data.gv.at](http://data.gv.at/): Open Data Portal des Bundes.
* [Regionalwahlkreise - Statistik Austria](https://www.statistik.at/web_de/klassifikationen/regionale_gliederungen/regionalwahlkreise/index.html): Regionalwahlkreis-Daten der Statistik Austria.



