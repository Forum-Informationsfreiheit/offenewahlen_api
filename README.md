# #NRW17 Visualisierung

In diesem Repository wird gemeinsam der Code, sowie die Dokumentation und Vorgangsweise für das Projekt **#NRW17 Visualisierung** organisiert. Dabei handelt es sich um eine Django-App mit einem HTML5 + JavaScript (D3.js, Bootstrap, jQuery) Frontend, welche auf Heroku läuft. Alles ist Open Source und mit einem Open Data Ethos (wenn auch die Rohdaten bis jetzt noch nicht Open Data sind, aber mal sehen).

**Alle nötigen Infos sowie die Dokumentation zu dem Projekt findest du im [Wiki](https://github.com/OKFNat/offenewahlen-nrw17/wiki), die Tasks werden via [Issue](https://github.com/okfnat/offenewahlen-nrw17/issues) koordiniert.**

Die Visualisierung wird am 15. Oktober kurz nach 17:00 Uhr unter [nrw17.offenewahlen.at](https://nrw17.offenewahlen.at) online gehen.

Dies ist ein Open Source Projekt, daher freuen wir uns über jede helfende Hand. Näheres, wie du mitmachenkannst erfährst du [hier](https://github.com/OKFNat/offenewahlen-nrw17/wiki#mitmachen).

## Daten

Die von uns zusammen getragenen Daten sind die erste Grundlage für die App. Wir erheben keinen Anspruch auf Vollständigkeit oder Korrektheit, glauben aber das die Datenlage schon recht okay ist für den Start. Uns ist dabei ein Crowd-Souring Zugang wichtig. Also wenn du einen Fehler findest, Daten für die Anreicherung oder neue Daten hast -> meld dich bitte! Weiters wollen wir die Daten kontinuierlich in Wikidata importieren um Wikidata so als den primären Ort für Identifier rund um Wahlen zu etablieren.

Nähere Infos zu den einzelnen Daten findet man unter [Dokumentieren#Datenmodelle](https://github.com/OKFNat/offenewahlen-nrw17/wiki/Dokumentieren#datenmodelle).

### Basisdaten

Folgende Basisdaten wurden gesammelt, um die Ergebnisse darstellen zu können.
- `data/setup/parties.json`: Liste mit allen bekannten **Parteien**. Sind aktuell nur die bekanntesten, da uns viele Daten zu den restlichen Parteien fehlen. Hilfe erwünscht.
- `data/setup/elections.json`: Liste mit bekannten **Wahlen**. Aktuell nur die NRW17 enthalten, da uns auch hier die Daten fehlen. Hilfe erwünscht.
- `data/setup/municipalities_20170101.json`: Liste mit allen **Gemeinden Österreichs am Stichtag 1. Januar 2017**. An sich komplett, Fehler oder Verbesserungen aber bitte melden.
- `data/setup/states2districts_20170101.json`: Mapping von **Bezirken mit den zugehörigen Bundesländern am Stichtag 1. Januar 2017**. An sich komplett, Fehler oder Verbesserungen aber bitte melden.
- `data/setup/regional-electoral-district2municipalities_20170101.json`: Mapping **Regionalwahlkreise mit den darin enthaltenen Gemeinden am Stichtag 1. Januar 2017**. An sich komplett, Fehler oder Verbesserungen aber bitte melden.

### Test-Daten

- `data/test/nrw_2013_1.json`: Ergebnisse der **Nationalratswahl 2013** aufbereitet für die Gemeinden mit Stichtag 1. 1. 2017.
- `data/test/example.xml`: Simulierte **Ergebnis-XML** Bundeswahlbehörde (BMI).


