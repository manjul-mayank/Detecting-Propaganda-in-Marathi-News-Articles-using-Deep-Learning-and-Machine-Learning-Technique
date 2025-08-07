from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def extract_articles_from_archive(driver, archive_url, seen_urls):
    driver.get(archive_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    articles = soup.select('article')  # select all articles
    data = []

    for article in articles:
        try:
            title_tag = article.select_one('div.np-archive-post-content-wrapper > header > h2 > a')
            paragraph_tag = article.select_one('div.np-archive-post-content-wrapper > div > p')

            if title_tag and paragraph_tag:
                url = title_tag['href']
                
                # Skip if we've already seen this URL
                if url in seen_urls:
                    continue
                
                seen_urls.add(url)  # Mark this URL as seen
                
                title = title_tag.get_text(strip=True)
                paragraph = paragraph_tag.get_text(strip=True)
                data.append({
                    'title': title,
                    'url': url,
                    'paragraph': paragraph
                })
        except Exception as e:
            print(f"❌ Error extracting article: {str(e)}")
            continue

    return data

def main():
    driver = setup_driver()
    seen_urls = set()  # Track URLs we've already processed
    
    try:
        archive_url = "https://marathi.factcrescendo.com/archives/"
        articles = extract_articles_from_archive(driver, archive_url, seen_urls)

        with open("factcrescendo_articles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "URL", "Paragraph"])

            for article in articles:
                writer.writerow([article['title'], article['url'], article['paragraph']])
                print(f"✅ Saved: {article['title'][:50]}...")

        print(f"\nTotal unique articles saved: {len(articles)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()