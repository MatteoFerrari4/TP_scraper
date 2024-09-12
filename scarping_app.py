import streamlit as st
import pandas as pd
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from re import search
from traceback import print_exc
from io import BytesIO

# Variabile globale per contare le recensioni saltate
skipped_reviews = 0

async def find_review_title(soup):
    """Extract the review title from the HTML content."""
    tag = 'h2'
    attributes = {'class': 'typography_heading-s__f7029 typography_appearance-default__AAY17'}
    element = soup.find(tag, attrs=attributes)
    if element:
        return element.get_text().strip()
    return None

async def find_review_body(soup):
    """Extract the review body from the HTML content."""
    tag = 'p'
    attributes = {'class': 'typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn'}
    element = soup.find(tag, attrs=attributes)
    if element:
        return element.get_text().strip()
    return None

async def find_review_date(soup):
    """Extract the review date from the HTML content."""
    tag = 'div'
    attributes = {'class': 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH'}
    element = soup.find(tag, attrs=attributes)
    if element:
        return element.get_text().strip()
    return None

async def find_review_rating(soup):
    """Extract the review rating from the HTML content."""
    tag = 'div'
    attributes = {'class': 'star-rating_starRating__4rrcf star-rating_medium__iN6Ty'}
    element = soup.find(tag, attrs=attributes)
    if element:
        img = element.find('img')
        if img and 'Rated' in img['alt']:
            rating = search(r'Rated (\d+) out of 5 stars', img['alt'])
            if rating:
                return int(rating.group(1))
    return None

async def find_reviewer_name(soup):
    """Extract the reviewer's name from the HTML content."""
    tag = 'span'
    attributes = {'class': 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17'}
    element = soup.find(tag, attrs=attributes)
    if element:
        return element.get_text().strip()
    return None

async def extract_review_details(soup):
    """Extract details from the review page."""
    try:
        title = await find_review_title(soup)
        body = await find_review_body(soup)
        date = await find_review_date(soup)
        rating = await find_review_rating(soup)
        reviewer = await find_reviewer_name(soup)

        if None in [title, body, date, rating, reviewer]:
            global skipped_reviews
            skipped_reviews += 1
            return None

        return [title, body, date, rating, reviewer]

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None

async def extract_reviews_from_page(soup):
    """Extract all reviews from the page."""
    review_section_class = 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl'
    review_elements = soup.find_all('article', class_=review_section_class)
    
    all_reviews = []
    for element in review_elements:
        review_details = await extract_review_details(element)
        if review_details:
            all_reviews.append(review_details)
    
    return all_reviews

async def fetch_page(session, url):
    """Fetch a single page asynchronously."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            return await extract_reviews_from_page(soup)
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return []

async def scrape_reviews(base_url, max_pages=10):
    """Scrape reviews concurrently using asyncio."""
    all_reviews = []
    async with ClientSession() as session:
        tasks = []
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}&page={page}"
            tasks.append(fetch_page(session, page_url))
            await asyncio.sleep(0.1)  # Wait 0.1 seconds between requests

        pages_reviews = await asyncio.gather(*tasks)
        for reviews in pages_reviews:
            all_reviews.extend(reviews)
    
    return all_reviews

def scrape_reviews_sync(base_url, max_pages=10):
    """Esegui la funzione di scraping in modalità sincrona per Streamlit."""
    return asyncio.run(scrape_reviews(base_url, max_pages))

# Utility function to export DataFrame to Excel format
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()  # Use close() instead of save()
    processed_data = output.getvalue()
    return processed_data

# Interfaccia Streamlit
st.title("Trustpilot Review Scraper")

# Input URL Trustpilot
url = st.text_input("Inserisci l'URL della pagina Trustpilot (es. https://www.trustpilot.com/review/www.mooney.it?languages=all):")

# Numero di pagine da analizzare
num_pages = st.number_input("Numero di pagine da scaricare", min_value=1, max_value=100, value=10)

# Avvia lo scraping quando l'utente clicca su "Scarica"
if st.button("Scarica Recensioni"):
    if url:
        # Esegui lo scraping delle recensioni
        reviews = scrape_reviews_sync(url, num_pages)

        # Controlla se ci sono recensioni trovate
        if not reviews:
            st.error("Nessuna recensione trovata.")
        else:
            # Crea un DataFrame con le recensioni
            reviews_df = pd.DataFrame(reviews, columns=['Title', 'Body', 'Date', 'Rating', 'Reviewer'])

            # Prepara il file Excel per il download
            excel_data = to_excel(reviews_df)

            # Offri un link per scaricare il file con le recensioni
            st.download_button(label="Scarica il file con le recensioni",
                               data=excel_data,
                               file_name='reviews_output.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        st.error("Inserisci un URL valido di Trustpilot")