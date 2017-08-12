# Daten

Dokumentation der Datenmodelle, von Rohdaten über Datenbank bis hin zum Client. 

## Basisdaten

Die Basis-Daten dienen zum Setup der App und als Datengrundlage, um die Ergebnisse passend visualisieren zu können.

### Gemeinden (2017-01-01)

Liste mit Gemeinden. `data/setup/municipalities_20170101.json`

Enthält alle Gemeinden Österreichs am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md).

Versionen:
- raw: CSV file `municipalities_20170101_1.csv`
- v1: angereichert mit Daten aus `municipalities_20170101_1.csv`
- v2: angereichert mit Bezirken und Bundesländern aus `states2districts_20170101`

Liste mit allen Gemeinden Österreichs am Stichtag 1. Januar 2017. Diese Datei wird zum Setup von #NRW17 verwendet.

Attribute:
- district: Bezirks-Name
- municipality_code: Gemeinde-Code
- municipality_id: Gemeindekennzahl
- name: Name der Gemeinde
- regional_electoral_district: Kurzbezeichnung des Regionalwahlkreises, in dem die Gemeinde liegt (siehe `regional-electoral-district2municipalities_20170101.json`)
- state: Bundesland, in dem die Gemeinde liegt.

### Parteien

Liste mit Parteien. `data/setup/parties.json`

Enthält alle Parteien die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md) erwünscht.

Attribute:
- full_name: Vollständiger Name der Partei
- short_name: Kürzel der Partei
- family: Zugehörigkeit zur Partei-Familie (EU)
- wikidata_id: ID des zugehörigen Wikidata Items
- website: url zur offiziellen Website
- description: kurze Beschreibung der Partei

### Wahlen

Liste mit Wahlen. `data/setup/elections.json`

Enthält alle Wahlen die für die Visualisierung notwendig sind. Wird kontinuierlich erweitert, [mitmachen](README.md) erwünscht.

Attribute:
- full_name: Vollständige Bezeichnung der Wahl
- short_name: Kurzbezeichnung / Akronym der Wahl, zb. NRW17
- election_type: Art der Wahl, zB Präsidentenwahl, Nationalratswahl
- election_day: Wahltag, als `yyyy-mm-dd`
- administrative_level: federal, state, district oder municipal
- wikidata_id: Wikidate ID des dazugehörigen Items

### Bundesland 2 Bezirke Mapping (2017-01-01)

Mapping von Bezirken zu jedem Bundesland. `data/setup/states2districts_20170101.json`

Enthält zu allen Bundesländern sämtliche enthaltene Bezirke am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md).

Attribute:
- NAME_DISTRICT: Bezirksname
- ID_DISTRICT: Ziffer für Bezirk (2+3 Stelle des Gemeinde-Codes, zB 91582 = 15)
- ID_STATE: Ziffer für Bundesland (erste Stelle des Gemeinde-Codes, zB 91582 = 9)
- NAME_STATE: Name Bundesland

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

### Regionalwahlkreis 2 Gemeinden Mapping (2017-01-01)

Mapping von Gemeinden zu den Regionalwahlkreisen. `data/setup/regional-electoral-district2municipalities_20170101.json`

Mapping aller Regionalwahlkreise mit den darin enthaltenen Gemeinden am Stichtag 1. 1. 2017. An sich komplett, Fehler oder Verbesserungen aber bitte melden, siehe [mitmachen](README.md).

Attribute:
- MUNICIPALITY_CODE: Gemeinde-Code
- SHORT_NAME: Kürzel für Regionalwahlkreis
- REGIONAL_ELECTORAL_DISTRICT_NAME: Bezeichnung des Regionalwahlkreises

Datenmodell:
```json
{
  "SHORT_NAME": {
    "municipalities": [
      "MUNICIPALITY_CODE",
      "MUNICIPALITY_CODE",
      .
    ],
    "name": "REGIONAL_ELECTORAL_DISTRICT_NAME"
  },
  .
}
```

## postgreSQL

In die PostgreSQL-Datenbank werden Tabellen zu jeder Klasse aus `src/viz/models.py` angelegt. Am besten direkt in der Datei nachlesen, welche Daten gespeichert werden.

Tables:
- Election: Wahlen
- RegionalElectoralDistrict: Regionalwahlkreise
- Party: Parteien
- Municipality: Gemeinden
- MunicipalityResult: Ergebnisse auf Gemeindeebene (ohne Partei-Ergebnisse)
- PartyResult: Partei-Ergebnisse auf Gemeindeebene
- RawData: Rohdaten

## Test-Daten

### NRW2013 Ergebnisse

Ergebnisse der Nationalratswahl 2013 aufbereitet für die Gemeinden ( Stichtag 1. 1. 2017). `data/test/nrw_2013_1.json`

- raw: Rohdaten von Flooh Perlot
- v1: 
  - löschen folgender Attribute: m
  - ausbessern der Parteikürzel von: Piraten, Der Wandel, Team Stronach, 
  - Bei der Gemeindekennzahl das "G" entfernt

Attribute:
- MUNICIPALITY_CODE: Gemeindecode
- SHORT_PARTY_NAME: Kürzel der Partei
- VOTES: Zahl der Stimmen

Datenmodell:
```json
{
  "MUNICIPALITY_CODE": {
    "SHORT_PARTY_NAME": "VOTES",
    "SHORT_PARTY_NAME": "VOTES",
    .
  },
  "MUNICIPALITY_CODE": {
    "SHORT_PARTY_NAME": "VOTES",
    "SHORT_PARTY_NAME": "VOTES",
    .
  },
  .
}
```

### NRW2013 Parteien Relation

Mapping der Parteien aus `data/test/nrw_2013_1.json` auf die Kurzbezeichnung aus `data/setup/parties.json`.

`data/test/nrw_2013_parties-relation.json`

### Simuliertes Ergebnis-XML

Da das BMI vermutlich die Ergebnisse zum ersten Mal in einem neuen XML-Dateiformat ausliefert und wir noch nicht wissen wie diese aussieht, haben wir vorab selber eine Test-Datei erstellt um so die Funktionen implementieren und testen zu können. Um die sich ständig ändernden Ergebnis-Dateien an einem Wahlabend zu simulieren, wurden drei Versionen erstellt.

* `data/test/example_1.xml`
* `data/test/example_2.xml`
* `data/test/example_2.xml`

Die XML-Dateien sind auch online unter [http://stefankasberger.at/wp-content/uploads/nrw17/](http://stefankasberger.at/wp-content/uploads/nrw17/) zu finden.

Folgende Ergebnisse sind darin enthalten:

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

### BMI Ergebnis-TXT 

* `data/test/example_1.txt`
* `data/test/example_2.txt`
* `data/test/example_3.txt`

## Frontend

Die Django-App liefert zwei JSON-Files an das Frontend aus. Eines mit den Ergebnisse, und eines mit den Geometrien.

### Ergebnisse

```json
{
	[
		{
			'id' = '',
			'eligible_voter': '',
			'votes': '',
			'valid': '',
			'invalid': '',
			'spatial_id': '',
			'ts_result': '',
			'ts_storage': '',
			'party_votes': [
				'spoe': '',
				'oevp': '',
				.
				.
				.
			],
			'is_final': ''
		},
		.
		.
		.
	]
}
```

### Geometrien (1. 1. 2017)

TopoJSON-Datei zu Österreich am Stichtag 1. Januar 2017.

`data/setup/municipalities_topojson_999_20170101.json`: 

## Datenquellen

Daten rund um Wahlen in Österreich sind hier zu finden: 
- [BMI Wahlen](http://www.bmi.gv.at/cms/BMI_wahlen/): offizielle Seite des Bundesinnenministeriums (der Bundeswahlbehörde) zu Wahlen.
- [BMI Parteienregister](http://www.bmi.gv.at/cms/bmi_service/parteienverz/start.aspx): Parteienregister des Bundesinnenministeriums.
- [data.gv.at](http://data.gv.at/): Open Data Portal des Bundes.
- [Regionalwahlkreise - Statistik Austria](https://www.statistik.at/web_de/klassifikationen/regionale_gliederungen/regionalwahlkreise/index.html): Regionalwahlkreis-Daten der Statistik Austria.
