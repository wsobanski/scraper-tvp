## status projektu
- ✅ Dokumentacja
- ✅ Link scraper 
- ✅ Content scraper
- ✅ pickle ➡ csv 
- 🚫 Content processor
- 🚫 Dokumentacja (eng)

## TLDR - Uproszczona instrukcja

Kod służy do pobrania artykułów z witryny `tvp.info.pl`. W celu wykonania kodu należy z poziomu terminala wywołać poniższe komendy.

### przygotowanie środowiska:

```bash
conda create -n scraper-env python=3.11
conda activate scraper-env
pip install -r requirements.txt
```

### pobranie metadanych:

```bash
python scraper_tvp_links.py --domain=polska --start_page=1 --end_page=10
```

### pobranie zawartości artykułów:

```bash
python scraper_tvp_content.py --n_workers=2 --n_batches=2 --batch_size=16
```
Pobraną zawartość można znaleźć w folderze:
```bash
project/obtained_content
```
___
___

## Cel projektu

Celem projektu było pobranie dużej ilości danych tekstowych w celu dostarczenia danych treningowych dla modelu językowego, którego celem miało być generowanie streszczenia tekstu.

Wybór padł na witrynę `tvp.info.pl` z dość prostego powodu - oferuje dostęp do danych archiwalnych z lat 2006 - 2023 w sposób nieodpłatny. Dane postanowiono zgromadzić wykorzystując do tego techniki web scrapingu. Projekt obejmuje proces przygotowania kodu potrzebnego do pozyskania danych w sposób zautomatyzowany i efektywny.  

Ostatecznie udało się pozyskać ponad 250 tysięcy arykułów z różnych domen: sport, biznes, polska, świat, społeczeństwo i wiele innych. 

---
## Struktura repo

```
📦 scraper-tvp
┣📂 articles metadata połączone metadane
┃ ┗ 📜 joined_metadata_files.csv
┣📂obtained content #logi wykonania scrpaera i finalny plik
┃ ┣ 📜 full_results.csv
┃ ┗ 📜 logs.json
┣📂 results #pobrane metadane w osobnych plikach
┃ ┗ 📜 results_domain_start-page-last-page.csv
┣📂 src #kod
┃ ┣ 📜 scraper_tvp_content.py
┃ ┣ 📜 scraper_tvp_links.py 
┃ ┗ 📜 text_processing.py (TODO)
```
Kod został podzielony na moduły tworzące (przynajmniej w teorii) logiczny układ.  
Role poszczególnych modułów są następujące:
- [utils](#funkcje-pomocnicze) - zawiera funkcje pomocnicze
- [links scraper](#links-scraper) - to plik wykonywalny służący do pobrania linków do artyułów z określonej ilości stron z danej domeny.
- [links scraper](#content-scraper) - plik wykonywalny służący do pobierania treści artykułów

📂 `results` zawiera metadane pobrane przez `scraper_links_tvp.py` w postaci pliku `.csv`.

📂 `articles_metadata` zawiera plik, który jest wynikiem połączenia plików z folderu `results`. Przechowywany jest w nim plik, z którego `scraper_tvp_content.py` wczytuje metadane dotyczące artykułów i pobiera ich zawartość.

📂 `obtained_content` zawiera plik `.csv`, który zawiera dotychczasowo pobrane treści artykułów wraz z ich metadanymi. Z tego folderu pobierane są ostateczne dane. W każdym wywołaniu kodu `scraper_tvp_content.py` plik jest wczytywany, a następnie każdy `batch` jest dopisywany do pliku. Dodatkowo w tym folderze umieszczono plik `logs.json`, który zawiera informacje o postępie pobierania danych. Każde kolejne wywołanie funkcji zacznie pobieranie zawartości artykułów w miejscu, które zapisane zostało w pliku logów.



---
### content scraper

Zadaniem programu `scraper_tvp_content.py` jest pobranie treści artykułów z danych linków.

Program przygotowuje plik z metadanymi artykułów - scala wiele plików w jeden a następnie je wczytuje i pobiera zawartość linków. Dane pobierane są równolegle przy wykorzystaniu zadanej przez użytkownika ilości procesów.

W celu uniknięcia utraty danych na wskutek potencjalnej awarii lub niepowodzenia w pobraniu danych program pobiera dane w seriach o określonej z góry wielkości. Każde kolejne wywołanie funkcji nie wpływa na dotychczasowo pobrane dane, gdyz funkcja jedynie dopisuje nowe rekordy do pliku.

Po pobraniu każdej serii program odczekuje losową ilość czasu. Prawdopodobieństwo odczekiwania przez dłuższy czas jest mniejsze niż odczekiwanie przez krótki okres czasu.

Pobrane dane zapisywane są do pliku z roszerzeniem `.csv`. Przy kolejnym wywołaniu funkcja z pliku `logs.json` wczytuje stan ostatniego wykonania i zaczyna pobierać dane od tego miejsca. 

---
### links scraper

Program `scrper_tvp_links.py` pobiera linki do artykułów z danej domeny ze stron o numerach zadeklarowanych przez użytkownika. Linki wraz z tytułem oraz leadem artykułu zapisywane są do pliku z roszerzeniem `.csv`. Pobrane dane wczytywane są następnie przez moduł `scraper_tvp_content.py` i przez niego pobierane są zawartości artykułów.

---
### utils 

Moduł pomocniczy zawiera różne funkcje związane z wykonywaniem kodu.

---

## Przepływ danych

Poniżej przedstawiono schematyczny przepływ danych. `link_scraper.py` wysyła zapytanie do strony i zwraca linki do artykułów, które następnie są zapisywane do pliku `.csv`. Każde wywołanie programu tworzy nowy plik. Wszystkie pliki są następnie łączone w jeden, który wczytywany jest przez `content_scraper.py`. Scraper ponownie łączy się ze stroną (tym razem za pośrednictwem linku do artykułów) i w rezultacie zwraca plik z pobranymi danymi. Dodatkowo generowany jest plik z logami, który weryfikowany jest przy każdym kolejnym wywołaniu funkcji.

![przepływ danych](dataflow.png)


## Przykładowe użycie

### Przygotowanie środowiska

W celu przygotowania środowiska należy wykonać poniższe komendy w terminalu:

```bash
conda create -n scraper-env python=3.11
conda activate scraper-env
pip install -r requirements.txt
```

### pobieranie linków do artykułów

Moduł `scrper_tvp_links.py` wywoływany jest z kilkoma parametrami. Są one ustawiane w momencie uruchamiania programu w terminalu.

* `domain` - sekcja, z której mają zostać pobrane linki. Dostępne (i przetestowane) opcje to biznes, polska, swiat, spoleczenstwo, sport oraz kultura.
* `start_page` - numer strony, od którego program ma zacząć pobierać linki
* `end_page` - numer ostatniej strony do pobrania

Pobrane metadane przechowywane są w pliku  `results_<domena>_<strona-startowa>-<strona-koncowa>.csv` i zawierają informacje o linku do artykułu, tytule oraz leadzie.

Wykonanie programu odbywa się w terminalu poprzez wywołanie z poziomu folderu `src` komend:

```bash
python scraper_tvp_links.py --domain=polska --start_page=1 --end_page=4
```

![przykładowe wykonanie kodu](demo_links.gif)

---
### pobieranie zawartości linków (pełnych artykułów)

Program `scraper_tvp_content.py` również uruchamiany jest z kilkoma parametrami:

* `n_workers` odpowiada za ilość procesów, przy użyciu których wykonywany będzie kod. Domyślnie ustawiona jest ona na ilość dostępnych rdzeni. 
* `batch_size` odpowiada za ilość pobieranych linków w jednym wykonaniu. Każdy `batch` tworzy zadaną ilość procesów, które istnieją do końca pobierania danej serii.
* `n_batches` odpowiada za ilość serii do pobrania.

Przykładowo, przy `batch_size = 64`, `n_batches = 4` i `n_workers = 4` w jednym wywołaniu programu zostanie pobrana zawartość 256 artykułów przy wykorzystaniu 4 procesów.  

Opis poszczególnych parametrów można wyświetlić następująco:

```bash
python scraper_tvp_content.py --help
```

W celu wykonania programu należy z poziomu folderu `src` wykonać komendę:

```bash
python scraper_tvp_content.py --n_workers=2 --n_batches=2 --batch_size=16
```

![[demo_content.gif]]

---
## Dostęp do danych

Pozyskane dane zostały opublikowane na platformie `Hugging Face`. Można je pobrać [stąd](https://huggingface.co/datasets/WiktorS/polish-news), bądź wczytać bezpośrednio z poziomu kodu wykorzystując do tego API platformy :

```bash
pip install datasets
```

```python
from datasets import load_dataset

dataset = load_dataset("WiktorS/polish-news")
```
