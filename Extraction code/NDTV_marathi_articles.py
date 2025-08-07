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

def get_article_links(driver, start_url, start_page=1, end_page=20):
    driver.get(start_url)
    links = set()
    
    for page_num in range(start_page, end_page + 1):
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.select('section.latest-news-sec article a')

        for a in articles:
            href = a.get("href")
            if href and href.startswith("/"):
                full_url = "https://www.lokmat.com" + href
                links.add(full_url)

        print(f"📄 Page {page_num}: Collected {len(links)} article links")

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > section.infinite-content > div.paginationNav > a"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            next_button.click()
        except:
            print("🚫 No more pages.")
            break

    return list(links)

def extract_article_content(driver, url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Headline
    try:
        headline = soup.select_one("#articlePage > main > div.leftwrapper > section > article > h1").get_text(strip=True)
    except:
        headline = "Headline not found"

    # Subheadline
    try:
        subheadline = soup.select_one("#articlePage > main > div.leftwrapper > section > article > h2:nth-child(5)").get_text(strip=True)
    except:
        subheadline = ""

    # Paragraphs 1–20
    paragraphs = []
    paragraph_selectors = [f"p:nth-child({i})" for i in range(1, 21)]

    for sel in paragraph_selectors:
        try:
            text = soup.select_one(f"#articlePage > main > div.leftwrapper > section > article > div.article-content > div.article-contentText > {sel}")
            if text:
                paragraphs.append(text.get_text(strip=True))
        except:
            continue

    content = "\n".join(paragraphs)
    return {
        "title": headline,
        "subtitle": subheadline,
        "url": url,
        "content": content if content else "⚠️ Content not found"
    }

def main():
    driver = setup_driver()
    try:
        base_url = "https://www.lokmat.com/latestnews/"
        article_links = get_article_links(driver, base_url, start_page=1, end_page=20)

        with open("lokmat_articles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Subtitle", "URL", "Content"])

            for i, link in enumerate(article_links, 1):
                try:
                    print(f"\n📰 Processing article {i}/{len(article_links)}: {link}")
                    article = extract_article_content(driver, link)
                    writer.writerow([article["title"], article["subtitle"], article["url"], article["content"]])
                    print(f"✅ Saved: {article['title'][:50]}...")
                except Exception as e:
                    print(f"❌ Failed: {link}: {str(e)}")
                    writer.writerow(["ERROR", "", link, str(e)])
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
