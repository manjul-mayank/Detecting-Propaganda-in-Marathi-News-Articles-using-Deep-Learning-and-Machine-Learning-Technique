from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import urljoin

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.set_page_load_timeout(60)
    return driver

def get_article_links(driver, max_pages=150):
    base_url = "https://www.lokmat.com/latestnews/page/"
    all_links = set()
    consecutive_empty = 0

    for page in range(1, max_pages + 1):
        try:
            url = f"{base_url}{page}/"
            print(f"\n📄 Processing page {page}: {url}")
            
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.infinite-content"))
            )
            time.sleep(10)  # Allow JavaScript to execute

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Primary selector with fallbacks
            articles = soup.select("""
                body > section.infinite-content > section > figure > figcaption > h2 > a:nth-child(2),
                figure.news-listing a.news-title,
                section.latest-news a[href*="/news/"],
                div.news-item h2 a
            """)
            
            page_links = {
                urljoin("https://www.lokmat.com", a["href"])
                for a in articles 
                if a.get("href") 
                and not a["href"].startswith(('javascript:', 'mailto:', 'tel:'))
                and not a["href"].endswith(('.jpg', '.png', '.pdf'))
            }

            if not page_links:
                consecutive_empty += 1
                print(f"⚠️ No links found on page {page} (Attempt {consecutive_empty}/3)")
                if consecutive_empty >= 3:
                    break
                continue
                
            consecutive_empty = 0
            new_links = page_links - all_links
            all_links.update(new_links)
            
            print(f"🔗 Found {len(new_links)} new articles (Total: {len(all_links)})")
            print("Sample:", list(new_links)[:1])

        except Exception as e:
            print(f"⚠️ Error processing page {page}: {str(e)}")
            continue

    return sorted(all_links)

def extract_article_content(driver, url):
    print(f"\n📰 Scraping: {url}")
    article_data = {
        "title": "",
        "url": url,
        "content": "",
        "error": None
    }

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article, #articlePage"))
        )
        time.sleep(10)  # Allow content to load
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Title extraction with multiple fallbacks
        title_selectors = [
            "#articlePage > section.infinite-article > article > h1",
            "article h1",
            "h1.heading",
            ".article-title"
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                article_data["title"] = title_elem.get_text(strip=True)
                break
        else:
            article_data["title"] = "Title not found"

        # Content extraction
        content_selectors = [
            "#articlePage > section.infinite-article > article > div.article-content > div.article-contentText",
            "article .article-body",
            ".article-content",
            "[itemprop='articleBody']"
        ]
        
        content_text = []
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                paragraphs = content_div.select("p")
                content_text = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                if content_text:
                    break
        
        article_data["content"] = "\n".join(content_text) if content_text else "Content not found"
        
        # Special handling for photo articles
        if "/photos/" in url or "/gallery/" in url:
            photo_captions = soup.select("figure.photo-article figcaption p")
            if photo_captions:
                article_data["content"] = "\n".join([p.get_text(strip=True) for p in photo_captions])

    except Exception as e:
        article_data["error"] = f"Scraping error: {str(e)}"
        print(f"⚠️ Error scraping article: {str(e)}")

    print(f"✅ Extracted: {article_data['title'][:60]}...")
    return article_data

def main():
    driver = setup_driver()
    try:
        print("🔍 Starting article collection...")
        article_links = get_article_links(driver, max_pages=150)
        print(f"\n✅ Collected {len(article_links)} articles to scrape")

        with open("lokmat_articles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "URL", "Content", "Error"])
            
            for i, link in enumerate(article_links, 1):
                article = extract_article_content(driver, link)
                writer.writerow([
                    article["title"],
                    article["url"],
                    article["content"],
                    article.get("error", "")
                ])
                
                # Progress reporting
                if i % 10 == 0:
                    print(f"\n📊 Progress: {i}/{len(article_links)} articles processed")
                    
    finally:
        driver.quit()
        print("\n🚀 Scraping complete! Results saved to lokmat_articles.csv")

if __name__ == "__main__":
    main()