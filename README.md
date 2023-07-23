## TLDR - Quick start

The code can be used to download articles from `tvp.info.pl`. To execute the code, call the following commands from the terminal.

### Environment setup:

```bash
conda create -n scraper-env python=3.11
conda activate scraper-env
pip install -r requirements.txt
```
Please execute these commands directly from the `src` folder:

### Download metadata:

```bash
python scraper_tvp_links.py --domain=polska --start_page=1 --end_page=10
```

### Download articles contents:

```bash
python scraper_tvp_content.py --n_workers=2 --n_batches=2 --batch_size=16
```
The downloaded content can be found in a folder:
```bash
project/obtained_content
```
___

## Goal of the project

The aim of the project was to retrieve a large amount of textual data in order to provide training data for a language model whose goal was to generate text summaries.

The choice fell on the website `tvp.info.pl` for a fairly simple reason - it offers free access to archival data from 2006 to 2023. It was decided to gather the data using web scraping techniques. The project involves the process of preparing the necessary code to retrieve the data in an automated and efficient manner.

In the end, over 250,000 articles from various domains were successfully acquired: sports, business, Poland, world, society, and many others.

---

## Repo structure

```
📦 scraper-tvp
┣📂 articles metadata - joined metadata
┃ ┗ 📜 joined_metadata_files.csv
┣📂obtained content - logs and full contents
┃ ┣ 📜 full_results.csv
┃ ┗ 📜 logs.json
┣📂 results - metadata in separate files
┃ ┗ 📜 results_domain_start-page-last-page.csv
┗📂 src - code
  ┣ 📜 scraper_tvp_content.py
  ┣ 📜 scraper_tvp_links.py
  ┣ 📜 utils.py
  ┗ 📜 text_processing.py (TODO)
```

The code has been divided into modules that create (at least in theory) a logical structure.
The roles of individual modules are as follows:
- [utils](#funkcje-pomocnicze) - contains utility functions,
- [links scraper](#links-scraper) - an executable file used to retrieve links to articles from a specified number of pages within a given domain,
- [content scraper](#content-scraper) - an executable file used to retrieve the content of articles.

📂 `results` contains metadata obtained by `scraper_links_tvp.py` in a `.csv` file format.

📂 `articles_metadata` contains a file that is the result of merging files from the `results` folder. It stores a file from which `scraper_tvp_content.py` reads metadata about articles and retrieves their content.

📂 `obtained_content` contains a `.csv` file that includes the previously obtained article content along with their metadata. The final data is retrieved from this folder. In each execution of the `scraper_tvp_content.py` code, the file is loaded, and each batch is appended to the file. Additionally, a `logs.json` file is placed in this folder, which contains information about the progress of the data retrieval. Each subsequent function call will resume the retrieval of article content from the position saved in the log file.

---

### 📜 content_scraper

The task of the `scraper_tvp_content.py` program is to retrieve the content of articles from the provided links.

The program prepares a file containing the metadata of the articles. It combines multiple files into one and then reads and retrieves the content from the links. The data retrieval is done in parallel using the number of processes specified by the user.

To prevent data loss in case of potential failures or unsuccessful data retrieval, the program fetches data in batches of a predetermined size. Each subsequent function call does not affect the previously retrieved data, as the function only appends new records to the file.

After retrieving each batch, the program waits for a random period of time. The probability of waiting for a longer time is lower than waiting for a shorter period.

The retrieved data is saved in a file with the `.csv` extension. Upon the next function call, the program reads the state of the last execution from the `logs.json` file and resumes data retrieval from that point.

---

### 📜 links_scraper

The program `scraper_tvp_links.py` retrieves links to articles from a specified domain from pages with numbers declared by the user. The links, along with the article title and lead, are saved in a file with the `.csv` extension. The retrieved data is then loaded by the `scraper_tvp_content.py` module, which retrieves the content of the articles using those links.

---

### 📜 utils 

The utility module contains various functions related to code execution.

---

## Data flow

Below is a schematic data flow. `link_scraper.py` sends a request to the webpage and returns the links to the articles, which are then saved to a `.csv` file. Each program execution creates a new file. All the files are later merged into one, which is then loaded by `content_scraper.py`. The scraper connects to the webpage again (this time using the article links) and returns a file with the retrieved data. Additionally, a log file is generated, which is checked with each subsequent function call.

![dataflow](https://github.com/WiktorSob/scraper-tvp/assets/94312553/60ca5c69-e353-4b83-b774-5fe526be9dc6)


## Full demo

### 1. Environment setup

To prepare the environment, please execute the following commands in the terminal:

```bash
conda create -n scraper-env python=3.11
conda activate scraper-env
pip install -r requirements.txt
```

### 2. Obtaining links to articles

The module `scrper_tvp_links.py` is called with several parameters. They are set at the moment of running the program in the terminal.

* `domain` - the section from which the links are to be extracted. Available (and tested) options are biznes, polska, swiat, spoleczenstwo, sport, and kultura.
* `start_page` - the page number from which the program should start retrieving links.
* `end_page` - the last page number to be fetched.

The retrieved metadata is stored in a file named `results_<domain>_<start-page>-<end-page>.csv`, which contains information about the articles' link, title, and lead.

The program is executed in the terminal by invoking the following commands from the `src` folder:

```bash
python scraper_tvp_links.py --domain=polska --start_page=1 --end_page=4
```

![demo_links](https://github.com/WiktorSob/scraper-tvp/assets/94312553/c2f23a3c-26f5-47d5-afd5-32d77505719a)

---

### 3. Obtaining contents of articles

The program `scraper_tvp_content.py` is also executed with several parameters:

* `n_workers` controls the number of processes used to execute the code. By default, it is set to the number of available CPU cores.
* `batch_size` determines the number of links fetched in one execution. Each batch creates a specified number of processes that exist until the completion of downloading a given series.
* `n_batches` defines the number of series to be downloaded.

For example, with `batch_size=64`, `n_batches=4`, and `n_workers=4`, a total of 256 articles will be downloaded in one program invocation using 4 processes.

You can display the description of each parameter as follows:

```bash
python scraper_tvp_content.py --help
```

To execute the program, you need to run the following command from the `src` folder:

```bash
python scraper_tvp_content.py --n_workers=2 --n_batches=2 --batch_size=16
```

![demo_content](https://github.com/WiktorSob/scraper-tvp/assets/94312553/eaa8fa87-8cb6-448c-b0c1-919b942e447b)

---

## Data access 

All obtained data has been published to `Hugging Face 🤗` platform. You can download the dataset [here](https://huggingface.co/datasets/WiktorS/polish-news), or load it directly using datasets API:

```bash
pip install datasets
```

```python
from datasets import load_dataset

dataset = load_dataset("WiktorS/polish-news")
```

---
