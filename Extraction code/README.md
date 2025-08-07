## 🗞️ Web Scraping Scripts for Dataset Collection

This project uses a modular and source-specific web scraping framework to collect Marathi news articles from three major online portals. Each script is tailored to the structure and rendering methods used by the respective websites.

---

### 📄 `LOKMAT_marathi_articles.py`

**Purpose:**  
Scrapes articles from [Lokmat Marathi News](https://www.lokmat.com), one of the most widely read Marathi dailies.

**Key Features:**
- Navigates paginated archive sections for multiple topics.
- Extracts article URLs from thumbnails using CSS selectors.
- Handles dynamic rendering with Selenium's `WebDriverWait`.
- Extracts article title, body text, and publication metadata.
- Includes fallback logic to handle HTML layout variations (e.g., photo gallery pages).
- Cleans and saves data into structured `.csv` format.

**Output Schema:**
- `title`: Article headline
- `content`: Full cleaned article text
- `url`: Article URL
- `source`: Static string: `Lokmat`
- `label`: Manual binary label (`1` = Propaganda)

**Technologies Used:**
- `Selenium`, `BeautifulSoup4`, `pandas`

---

### 📄 `NDTV_marathi_articles.py`

**Purpose:**  
Extracts digital news articles from [NDTV Marathi](https://marathi.ndtv.com), a digital-first news platform.

**Key Features:**
- Crawls paginated topic listings (e.g., politics, Maharashtra).
- Detects and extracts links from dynamic sections using multiple CSS paths.
- Captures text paragraphs and titles with fallback parsing.
- Includes sleep timers and retry logic for robustness.
- Appends output to a central CSV or JSON file for aggregation.

**Output Schema:**
- `title`: Article title
- `content`: Body text extracted paragraph-wise
- `url`: Article URL
- `source`: Static string: `NDTV Marathi`
- `label`: Binary label (`1` = Propaganda)

---

### 📄 `factcrescendo_marathi_factcheck_articles.py`

**Purpose:**  
Scrapes verified factual reports from [FactCrescendo Marathi](https://www.factcrescendo.com/mr/), a known fact-checking organization in India.

**Key Features:**
- Targets only `Fact Check` labeled articles.
- Extracts structured factual claims and refutations.
- Captures publication metadata including tags and timestamps.
- Handles pagination, dynamic page loads, and page timeouts gracefully.
- Filters non-article pages (e.g., videos, advertisements).

**Output Schema:**
- `title`: Fact-check headline
- `content`: Verified claim summary and rebuttal text
- `url`: Source URL
- `source`: Static string: `FactCrescendo`
- `label`: `0` (Factual)

---

### 🛠️ Common Features Across Scripts

- ✅ **Headless Browsing** using `Selenium` with ChromeDriver
- ✅ **Dynamic Waiting** for JavaScript-rendered pages
- ✅ **Retry and Timeout Handling** for resilience
- ✅ **URL Validation** to avoid media files and redirects
- ✅ **Custom Selectors** for complex HTML layouts
- ✅ **Structured CSV Output** with clean encoding

---

### 📁 Folder Structure
```
Extraction code/
├── LOKMAT_marathi_articles.py
├── NDTV_marathi_articles.py
├── factcrescendo_marathi_factcheck_articles.py
└── scraped_data/
├── lokmat.csv
├── ndtv.csv
└── factcrescendo.csv
```
### 📝 Usage

Each script can be run independently:
```bash
python LOKMAT_marathi_articles.py
python NDTV_marathi_articles.py
python factcrescendo_marathi_factcheck_articles.py
```
**🔒 Note: Ensure you have ChromeDriver installed and compatible with your Chrome version. Add error handling if running on remote servers.**
## 📦 Requirements
Install necessary libraries using:
```
pip install -r requirements.txt
selenium
beautifulsoup4
pandas
webdriver-manager
```

