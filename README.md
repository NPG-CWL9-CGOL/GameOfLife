# Game Of Life

 To repozytorium do aplikacji symulującej tzw. *Grę w życie* stworzoną w 1970 przez matematyka **Johna Hortona Conwaya**. Należy ona do klasy automatów komórkowych, czyli modeli dyskretnych realizowanych zazwyczaj na siatce komórek
mogących przyjmować skończoną ilość stanów. Innymi słowy, jest to "0 player game". Gra polega na sprawdzeniu określonych wcześniej instrukcji warunkowych dla każdego pola planszy, powtarzanych w każdym kroku czasowym. Wynalazek Conwaya 
zyskał szczególną popularność ze względu na to, jak z zaledwie 2 prostych reguł i kilku pikseli na planszy można uzyskiwać bardzo złożone układy, zamieniając prostą siatke w "tetniące życiem" środowisko.
## Zasady gry 

  Każda komórka posiada jedynie dwa stany: **ON** ("żywa") i **OFF** ("martwa"). Za komórki sąsiadujące uznajemy 8 najbliższych pól wokół komórki.

  Wyróżniamy 2 podstawowe zasady Gry w życie:
  1. Narodziny (*zasada B3*): Jeśli martwa komórka ma dokładnie 3 żywych sąsiadów, w następnej turze sama stanie się żywa.
  2. Przetrwanie (*zasada S23*): Żywa komórka pozostaje żywa gdy w danej turze ma dokładnie 2 lub 3 żywych sąsiadów, w przeciwnym wypadku umiera.

## Instrukcja uruchomienia
1. Pobierz i przejdź do repozytorium

```bash
  git clone https://github.com/NPG-CWL9-CGOL/GameOfLife.git
  cd GameOfLife
```

2. Uruchom skrypt tworzący wirtualne środowisko Pythona i pobierający potrzebne biblioteki

```bash
#Linux/MacOS
  source scripts/activate.sh
#Windows
  .\scripts\activate.bat
```

3. Otwórz aplikacje

```bash
#Linux/MacOS
  python3 main.py
#Windows
  python main.py
```

### Autorzy

Zespół projektowy w składzie: **Dawid Tomasik**, **Filip Ściurka**, **Szymon Ślazyk**, **Mateusz Urbański**, **Jakub Ukalski**.

Projekt został zrealizowany w ramach laboratoriów z przedmiotu Narzędzia Pracy Grupowej dla kierunku Automatyka i Robotyka na **Akademii Górniczo Hutniczej w Krakowie**. 
    
