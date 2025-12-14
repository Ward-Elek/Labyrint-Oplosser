# Labyrint-Oplosser

Dit project onderzoekt hoe een AI een labyrint kan oplossen met behulp van Python. Het doel is om een agent te bouwen die efficiënt de uitgang van een doolhof vindt.

## Projectstructuur

- `Code/task`: Bevat de Python-code voor het genereren van labyrinten, de agent en de trainingslogica.
- `data`: Bevat geëxporteerde afbeeldingen en metriekbestanden die tijdens sessies zijn opgeslagen.
- `requirements.txt`: Lijst met alle Python-dependencies die nodig zijn om het project uit te voeren.  

## Installatie

1. Clone deze repository:

    git clone https://github.com/Ward-Elek/Labyrint-Oplosser.git

2. Ga naar de projectmap:

        cd Labyrint-Oplosser

3. Installeer de vereiste pakketten:

        pip install -r requirements.txt

Zorg dat je een recente versie van Python 3 geïnstalleerd hebt.

## Gebruik / Quickstart

1. Zorg dat de dependencies geïnstalleerd zijn (`pip install -r requirements.txt`).
2. Start een van de onderstaande scripts vanuit de projectroot:

   - **Laatste getrainde agent draaien**:
     ```bash
     python Code/task/train_and_solve.py
     ```
     Dit opent een Pygame-venster waarin de agent een labyrint probeert op te lossen. Je ziet de animatie van het pad en eventuele statusmeldingen in de terminal.

   - **Live training uitvoeren**:
     ```bash
     python Code/task/live_training_viewer.py
     ```
     Start de trainingslus met visualisatie. Je krijgt een Pygame-venster met de actuele positie van de agent, plus trainingsstatistieken in de console.

   - **Labyrint-generatie of alternatieve run**:
     ```bash
     python Code/task/maze_maker.py
     ```
     Voert de standaardlogica uit voor het genereren en oplossen van een labyrint. Ook hier verschijnt een Pygame-venster met de doolhofvisualisatie.

### Vereisten voor lokale uitvoering

- Een werkende Pygame-vensteromgeving (bijv. macOS/Windows of Linux met een display/server). In headless omgevingen moet je een virtuele display gebruiken (zoals Xvfb) om de vensters te tonen.
- Python 3 en de pakketten uit `requirements.txt`.


## Doel en aanpak

- Verkennen van algoritmen en AI-technieken om labyrinten op te lossen (bijvoorbeeld zoekalgoritmen of reinforcement learning).

- Experimenteren met verschillende strategieën en parameters om de prestaties van de agent te verbeteren.

## Auteurs

Dit project is gemaakt door Ward, Jarno en Geal. Samen onderzoeken we hoe we een labyrint-oplossende AI kunnen ontwikkelen.
