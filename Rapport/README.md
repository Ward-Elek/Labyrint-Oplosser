# Labyrint Oplosser

**Opleiding:** Bachelor in de Elektronica‑ICT – studiegebied AI Programming (Hogeschool VIVES, campus Brugge)   
**Docent:** Franky Loret  
**Academiejaar:** 2025‑2026

Dit project onderzoekt hoe een kunstmatige intelligentie zelfstandig een labyrint kan oplossen en visualiseren, met een in Python geïmplementeerde agent en een Pygame‑omgeving die het doolhof en het zoekproces in real time weergeeft. Klassieke pathfinding‑algoritmen (A\*, BFS, DFS, Dijkstra) worden toegepast om paden te vinden en hun prestaties te analyseren in uiteenlopende labyrinten.

---

## Inhoud

- [Inleiding](#inleiding)
- [1. Doelstellingen](#1-doelstellingen)
  - [1.1 Hoofddoelstellingen](#11-hoofddoelstellingen)
  - [1.2 Subdoelstellingen](#12-subdoelstellingen)
- [2. Probleemstelling](#2-probleemstelling)
  - [2.1 Context](#21-context)
  - [2.2 Doelgroepen](#22-doelgroepen)
- [3. Analyse](#3-analyse)
- [4. Resultaat](#4-resultaat)
- [5. Conclusie](#5-conclusie)
- [6. Uitbreiding](#6-uitbreiding)
- [7. Reflectie](#7-reflectie)
- [8. Bibliografie](#8-bibliografie)

---

## Inleiding

Auteur: Jarno

Dit project demonstreert hoe een eenvoudige AI op basis van zoekalgoritmen een pad kan leren vinden van een start‑ naar een eindpunt in een labyrint, waarbij het doolhof als graaf‑ of gridstructuur wordt gemodelleerd. De nadruk ligt op de didactische waarde van het visualiseren van zoek‑ en optimalisatieprincipes voor beginnende AI‑ontwikkelaars.

---

## 1. Doelstellingen

Auteur: Jarno

### 1.1 Hoofddoelstellingen

Het hoofddoel is een AI‑oplossing te ontwikkelen die zelfstandig uiteenlopende labyrinten kan analyseren, efficiënt kan doorlopen en een optimaal of bijna optimaal pad naar de uitgang bepaalt met behulp van klassieke zoekalgoritmen. Het labyrint wordt voorgesteld als een graaf of grid, zodat de agent systematisch paden kan evalueren, kosten kan inschatten en kan balanceren tussen snelheid, padlengte en robuustheid van de oplossing.

### 1.2 Subdoelstellingen

- Implementeren van meerdere pathfinding‑algoritmen (A\*, BFS, DFS, Dijkstra) om de sterke en zwakke punten in verschillende soorten labyrinten te vergelijken. 
- Visualiseren van het labyrint, bezochte knopen en het uiteindelijke pad om het zoekproces stap voor stap inzichtelijk te maken.
- Optimaliseren van prestaties (snelheid, geheugengebruik) via geschikte datastructuren zoals queues, stacks en priority queues.
- Vergelijken van algoritmen op basis van padlengte, rekentijd en aantal bezochte knopen, met resultaten in tabellen of grafieken.
- Valideren op uiteenlopende labyrint‑complexiteiten, van eenvoudige grids tot grotere sterk vertakte doolhoven, om robuustheid en generaliseerbaarheid aan te tonen.

---

## 2. Probleemstelling

Auteur: Jarno

Een labyrint is een klassiek AI‑probleem waarbij de kern bestaat uit het vinden van een efficiënte en betrouwbare route van start naar eindpunt door een complexe structuur met meerdere mogelijke paden en doodlopende gangen. Dit vereist intelligente zoekstrategieën, efficiënte datastructuren en weloverwogen keuzes tussen verschillende pathfinding‑algoritmen. 

### 2.1 Context

Dit project situeert zich binnen klassieke AI‑problemen met focus op zoek‑ en optimalisatietaken, en gebruikt traditionele algoritmen en heuristische methoden in plaats van machine learning of deep learning. Dergelijke technieken worden breed toegepast in autonome systemen, robotica en game‑ontwikkeling en vormen een basis voor meer geavanceerde AI‑toepassingen. 

### 2.2 Doelgroepen

- **Educatieve instellingen:** Visualiseren en onderwijzen van zoek‑ en optimalisatieconcepten in een interactief kader. 
- **Game‑developers:** Toepassen van efficiënte pathfinding voor vloeiende gameplay en realistische navigatie in virtuele omgevingen. 

- **Robotica‑toepassingen:** Navigatie van autonome robots met aandacht voor obstakelvermijding en route‑efficiëntie. 

- **AI‑onderzoekers:** Vergelijken en evalueren van zoekstrategieën op nauwkeurigheid, schaalbaarheid en prestaties in uiteenlopende labyrintconfiguraties. 

---

## 3. Analyse
---

Auteur: Geal

Voor de implementatie werd gekozen voor Python in combinatie met de Pygame‑library, omdat deze combinatie zich goed leent tot het snel ontwikkelen en visualiseren van AI‑logica en grid‑gebaseerde omgevingen. 
Het project is modulair opgebouwd in aparte scripts voor labyrintgeneratie en ‑weergave, live training van de agent en het tonen van het finale resultaat, wat een duidelijke scheiding tussen logica, visualisatie en uitvoering oplevert. 
De agent gebruikt een zoekstrategie die mogelijke bewegingen evalueert, toegestane stappen controleert en bezochte posities bijhoudt, zodat eindeloos in cirkels lopen vermeden wordt.   
De software draait lokaal op een standaardcomputer zonder specifieke hardwarevereisten, waarbij alle berekeningen op de CPU uitgevoerd worden en het project als gewoon Python‑script kan worden gedeployed. 

---

## 4. Resultaat



---

## 5. Conclusie

Auteur: Jarno

De oorspronkelijke doelstelling om een intelligente oplossing te bouwen die labyrinten efficiënt kan analyseren, doorlopen en een (bij voorkeur optimaal) pad kan bepalen met verschillende pathfinding‑algoritmen is in grote mate bereikt. De implementatie van A\*, BFS, DFS en Dijkstra, gecombineerd met visualisatie en prestatieanalyse, sluit goed aan bij de vooropgestelde subdoelstellingen. 

Binnen de context van klassieke AI‑algoritmen biedt het resultaat een geldige en bruikbare oplossing voor het efficiënt bepalen van een weg door complexe labyrinten. Tests met labyrinten van verschillende complexiteit tonen dat vooral A\* een goede balans biedt tussen snelheid en kwaliteit van het gevonden pad, terwijl de andere algoritmen nuttige referenties vormen.

---

## 6. Uitbreiding

Auteur: Jarno

Voor toekomstig werk zijn meerdere uitbreidingen mogelijk, zoals het toevoegen en vergelijken van extra algoritmen of varianten van de strategie om de impact op rekentijd, padlengte en stabiliteit gedetailleerder te onderzoeken.   
Daarnaast kan een uitgebreidere benchmarkomgeving met grotere en willekeurig gegenereerde doolhoven en een gebruiksvriendelijkere interface helpen om schaalbaarheid, generalisatie en gebruikerservaring verder te verbeteren.

Andere interessante uitbreidingen zijn het ondersteunen van gewogen paden en dynamische obstakels, zodat de agent leert omgaan met variabele kosten en veranderende omgevingen. 
Ten slotte kunnen statistieken zoals beloningscurves, heatmaps van bezochte velden en herhalingsmogelijkheden van runs de interpretatie van het leer‑ en zoekproces verder ondersteunen. 

---

## 7. Reflectie

- **Jarno:** “In dit project heb ik bijgeleerd hoe je een labyrint‑oplossend algoritme ontwerpt, implementeert en test, en hoe belangrijk het is om de code stap voor stap logisch op te bouwen. Als reflectie neem ik mee dat ik vroeger moet beginnen aan zulke projecten, omdat ik onderschat heb hoelang het zou duren.”  

- **Geal:** “Ik heb niet echt een interesse in software of AI‑learning, maar dit project heeft me wel bijgeleerd hoe algoritmes op verschillende manieren gebruikt kunnen worden. Ik wist bijvoorbeeld niet dat een DFS‑algoritme kon worden ingezet om een maze te genereren.” 

- **Ward:** 



---

## 8. Bibliografie

- Algfoor, Z. A., Sunar, M. S., & Kolivand, H. (2015). *A comprehensive study on pathfinding techniques for robotics and video games*. International Journal of Computer Games Technology. 

- Baeldung. (2024). *Tracing the path in DFS, BFS, and Dijkstra’s algorithm*.

- GeeksforGeeks. (2012). *Breadth first search (BFS) for a graph*. 

- PuppyGraph. (2025). *DFS vs BFS: A guide for deep understanding*. 

- *Research of the Path Finding Algorithm A\* in Video Games*. HSET Journal. 

- Russell, S., & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach* (3e ed.). Prentice Hall.
- Wikipedia. *Pathfinding*. 

- Hurbans, R. (2020). *Grokking artificial intelligence algorithms*. Manning Publications.
