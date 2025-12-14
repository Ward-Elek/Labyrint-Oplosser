# Metrics-overzicht

Deze map bevat de geëxporteerde visualisaties die na een trainingsrun zijn gegenereerd. Onderstaande toelichting beschrijft wat je normaal gesproken in elke grafiek zou moeten zien en hoe je de waardes kunt interpreteren.

## Overzicht van de grafieken

### `metric_cumulative_reward_YYYYMMDD_HHMMSS.png`
Toont de totale beloning per episode. Een stijgende lijn geeft aan dat de agent gemiddeld hogere beloningen behaalt en het labyrint efficiënter oplost. Kleine schommelingen zijn normaal, maar een langdurige daling kan wijzen op regressie in het beleid.

### `metric_reward__rolling_avg__YYYYMMDD_HHMMSS.png`
Laat het voortschrijdend gemiddelde van de beloning zien (bijvoorbeeld over de laatste ~50 episodes). Deze gladgestreken curve helpt trends te herkennen: een geleidelijke stijging betekent dat de leerstrategie werkt, terwijl een vlakke of dalende lijn suggereert dat hyperparameters of beloningsstructuur moeten worden bijgesteld.

### `metric_steps_YYYYMMDD_HHMMSS.png`
Geeft het aantal stappen per episode weer. Minder stappen betekenen dat de agent sneller de eindpositie vindt. Na een leercurve verwacht je dat deze waarde naar beneden beweegt of stabiliseert rond een laag niveau. Grote pieken kunnen duiden op verkenningsfases of moeilijkere doolhoven.

### `metric_steps__rolling_avg__YYYYMMDD_HHMMSS.png`
Het voortschrijdend gemiddelde van het aantal stappen. Deze grafiek filtert pieken weg en laat zien of de algemene efficiëntie verbetert. Een dalende of stabiele lijn op laag niveau is het gewenste patroon.

### `metric_epsilon_YYYYMMDD_HHMMSS.png`
Visualiseert de epsilon-waarde van ε-greedy verkenning. Gewoonlijk start epsilon dicht bij 1 (veel verkenning) en daalt richting 0 (meer exploitatie). Een vloeiende, afnemende lijn betekent dat de agent geleidelijk meer vertrouwt op de geleerde strategie.

### `metric_success_ratio_YYYYMMDD_HHMMSS.png`
Toont het percentage episodes waarin het doel is bereikt. De waarde loopt van 0 tot 1. Een stijgende curve richting 1 geeft aan dat de agent bijna altijd het einde haalt. Een dalende of instabiele lijn kan betekenen dat de agent nog niet stabiel presteert.

### `metrics_panel_YYYYMMDD_HHMMSS.png`
Een compositie van alle metriekplots boven elkaar, handig om correlaties te zien (bijvoorbeeld of een dalende epsilon samenvalt met stijgende beloning en dalende stappen).

## CSV- en JSON-bestanden
- `metric_series_YYYYMMDD_HHMMSS.csv`
- `metric_series_YYYYMMDD_HHMMSS.json`

Deze bestanden bevatten dezelfde gegevens als de grafieken, zodat je ze kunt hergebruiken voor verdere analyse of om aangepaste grafieken te maken. De kolommen tonen per episode onder andere `cumulative_reward`, `reward (rolling avg)`, `steps`, `steps (rolling avg)`, `epsilon` en `success ratio`.

## Hoe de grafieken te lezen
- **Stabiele vooruitgang**: stijgende beloning + success ratio richting 1, terwijl stappen dalen of stabiliseren.
- **Te veel verkenning**: hoge epsilon gecombineerd met wisselende beloningen en veel stappen; stel eventueel een sneller afbouwschema in.
- **Plateau**: vlakke beloningscurves en stabiele, maar niet optimale stappenwaarden; experimenteer met leerparameters of beloningsfunctie.

De bestandsnamen bevatten een timestamp (`YYYYMMDD_HHMMSS`) zodat je meerdere runs naast elkaar kunt bewaren.
