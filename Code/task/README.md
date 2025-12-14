# Code/task README

Deze map bevat alle Python bestanden voor het Labyrint-Oplosser project. Dit project gebruikt Q-learning (reinforcement learning) om labyrints automatisch op te lossen.

## Setup

1. Gebruik Python 3.10 of hoger.
2. Maak en activeer een virtualenv in deze `task`-map:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Installeer de afhankelijkheden:
   ```bash
   pip install -r requirements.txt
   ```

## Overzicht van de bestanden

### Kern modules

#### `maze.py`
**Doel:** Definieert de `Maze` klasse die verantwoordelijk is voor het genereren van random labyrints.

**Belangrijkste functionaliteit:**
- Maakt een grid van cellen met gegeven dimensies
- Genereert automatisch een labyrint met behulp van depth-first search algoritme
- Markeert start- en eindpunt van het labyrint
- Beheert de muren tussen cellen

**Rol in het geheel:** Levert de basis labyrintstructuur waarop de agent getraind wordt.

---

#### `cell.py`
**Doel:** Definieert de `Cell` klasse die individuele cellen in het labyrint representeert.

**Belangrijkste functionaliteit:**
- Slaat positie (x, y) van de cel op
- Beheert de 4 muren (N, S, E, W) van elke cel
- Bevat methodes om muren tussen cellen af te breken
- Houdt de status bij (Start, End, of None)

**Rol in het geheel:** Bouwsteen voor het labyrint; elke cel weet welke muren aanwezig zijn.

---

#### `convert.py`
**Doel:** Converteert het labyrint naar een feasibility matrix voor de Q-learning agent.

**Belangrijkste functionaliteit:**
- Definieert de `Feasibility` klasse
- Nummert alle cellen in het labyrint sequentieel
- Creëert een F-matrix (feasibility matrix) die aangeeft welke cellen bereikbaar zijn vanaf elke cel
- Implementeert `find_reachable_neighbors()` functie om buurcellen te vinden zonder muur ertussen

**Rol in het geheel:** Vertaalslag tussen het fysieke labyrint en de state-space representatie voor Q-learning. De F-matrix geeft aan welke state transitions mogelijk zijn.

---

#### `learn.py`
**Doel:** Implementeert de Q-learning agent die leert het labyrint op te lossen.

**Belangrijkste functionaliteit:**
- Definieert de `Agent` klasse met Q-learning algoritme
- Implementeert de Bellman vergelijking voor Q-value updates
- Ondersteunt epsilon-greedy exploration strategie
- Bevat `train()` methode voor het trainen van de agent
- Bevat `walk()` methode om het geleerde pad te doorlopen
- Beheert de Q-matrix (state-action values) en R-matrix (rewards)

**Rol in het geheel:** Het intelligente brein van het project. Leert door trial-and-error welke route door het labyrint het beste is.

---

### Visualisatie modules

#### `draw.py`
**Doel:** Biedt functies voor het tekenen van het labyrint als statische afbeelding.

**Belangrijkste functionaliteit:**
- Tekent individuele cellen met hun muren
- Visualiseert het volledige labyrint
- Markeert start en eindpunten
- Gebruikt PIL (Python Imaging Library) voor het genereren van PNG afbeeldingen
- Nummert cellen optioneel voor debugging

**Rol in het geheel:** Maakt statische visualisaties van het labyrint voor debugging en presentatie.

---

#### `live_view.py`
**Doel:** Real-time Pygame visualisatie van het trainingsproces.

**Belangrijkste functionaliteit:**
- Definieert de `LiveMazeViewer` klasse
- Toont de agent live tijdens training
- Visualiseert het pad van de agent met een trail
- Gebruikt kleurgradaties om te tonen hoe vaak cellen bezocht zijn
- Ondersteunt zoom functionaliteit
- Toont het opgeloste pad in groen na voltooiing

**Rol in het geheel:** Geeft real-time visuele feedback tijdens het trainingsproces, zodat je kunt zien hoe de agent leert.

---

#### `callback_protocol.py`
**Doel:** Definieert constanten voor communicatie tussen de agent en viewer.

**Belangrijkste functionaliteit:**
- Bevat `RESET_SIGNAL` constante om episode resets te signaleren

**Rol in het geheel:** Zorgt voor gestandaardiseerde communicatie tussen training loop en live viewer.

---

### Hoofdprogramma's

#### `maze_maker.py`
**Doel:** Simpel startpunt voor het project - genereert alleen een labyrint.

**Belangrijkste functionaliteit:**
- Vraagt gebruiker om labyrint dimensies en startpunt
- Creëert een labyrint
- Tekent en slaat het labyrint op als PNG

**Rol in het geheel:** Eenvoudig entry point voor het testen van labyrint generatie zonder training.

---

#### `train_and_solve.py`
**Doel:** Volledige pipeline voor training en visualisatie van de oplossing.

**Belangrijkste functionaliteit:**
- Vraagt gebruiker om parameters (dimensies, gamma, learning rate)
- Creëert labyrint en feasibility matrix
- Traint de agent met Q-learning
- Print F-matrix en Q-matrix
- Toont het opgeloste pad in live viewer
- Gebruikt threading voor smooth playback

**Rol in het geheel:** Hoofdprogramma voor het uitvoeren van een complete training run met visualisatie van het resultaat.

---

#### `live_training_viewer.py`
**Doel:** Toont het trainingsproces live terwijl de agent leert.

**Belangrijkste functionaliteit:**
- Vraagt gebruiker om parameters met input validatie
- Start training in een aparte thread
- Toont elke stap van de agent tijdens training live
- Visualiseert het eindresultaat als de training klaar is
- Gebruikt callbacks voor real-time updates

**Rol in het geheel:** Beste programma voor het observeren van het leerproces; je ziet de agent live exploreren en verbeteren.

---

### Ondersteunende bestanden

#### `__init__.py`
**Doel:** Maakt de `task` directory een Python package.

**Rol in het geheel:** Technisch bestand nodig voor Python import structuur.

---

#### `feasibility.png`
**Doel:** Voorbeeld afbeelding van een feasibility matrix visualisatie.

**Rol in het geheel:** Documentatie/referentie materiaal.

---

## Hoe te gebruiken

### `maze_maker.py`
- **Gebruikersinput:** Labyrintdimensies (`x y`) en startcoördinaten (`x y`). Validatie zorgt dat waarden positief zijn en binnen het raster vallen.
- **Resultaten:** Genereert een labyrint en slaat een PNG op (standaard `maze.png`) in dezelfde map.

### `train_and_solve.py`
- **Gebruikersinput:** Labyrintdimensies, startcoördinaten, gamma en learning rate. Er worden 1000 episodes getraind.
- **Resultaten:** Print F- en Q-matrices in de terminal en toont de opgeloste route in een Pygame-venster. Er worden geen bestanden opgeslagen; sluit het venster om het script af te ronden.

### `live_training_viewer.py`
- **Gebruikersinput:** Labyrintdimensies, startcoördinaten, gamma en learning rate.
- **Resultaten:** Start training in een thread, streamt states en metrics live naar de viewer (met rolling gemiddelde statistieken). Geeft het gevonden pad weer zodra training klaar is. Geen bestand-uitvoer.

Voor alle scripts geldt: voer ze uit vanuit de `Code/task`-map zodat relatieve paden (zoals `maze.png`) kloppen.

## Dependencies
- numpy
- pandas
- PIL (Pillow)
- pygame (vereist werkende grafische omgeving/SDL-driver)
- wrapt_timeout_decorator

### Bekende afhankelijkheden en valkuilen
- Pygame heeft een beschikbare display-driver nodig; op headless servers kan het nodig zijn om een virtuele display (bijv. `SDL_VIDEODRIVER=dummy`) te configureren.
- PIL/Pillow gebruikt systeembibliotheken voor beeldverwerking; zorg dat standaard build-dependencies aanwezig zijn als installatie faalt.
- Scripts lezen gebruikersinput vanaf stdin; voer ze in een interactief shell-venster uit.
- De viewer-sluiter bepaalt de scripts; sluit het Pygame-venster om processen netjes te beëindigen.

## Q-learning Parameters

- **gamma (γ)**: Discount factor (0-1) - bepaalt hoe belangrijk toekomstige rewards zijn
- **learning rate (α)**: Learning rate (0-1) - bepaalt hoe snel de agent leert
- **max_epochs**: Aantal training episodes
- **epsilon**: Exploration rate voor epsilon-greedy strategie
