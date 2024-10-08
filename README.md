### README for Trustpilot Review Scraper and Word Count Analyzer

---

## Project Overview

This project provides a streamlined solution for scraping reviews from **Trustpilot** and analyzing the unique word count from those reviews. It consists of two main applications:

1. **Trustpilot Review Scraper**: Scrapes reviews from a Trustpilot company page and saves them in an Excel file.
2. **Word Count Analyzer**: Processes the reviews, combines the title and body of each review, removes common stopwords (in English and Italian), and generates an Excel file with the unique words and their frequencies.

Both of these applications have been bundled into a **Streamlit**-based web application for easy use.

---

## Files Included

1. **app.py**: The main Streamlit application that serves as a front-end for both the scraping and word count functionalities.
2. **scraping_app.py**: Contains the logic for scraping reviews from Trustpilot using asynchronous requests.
3. **word_count_app.py**: Processes the reviews and generates a word frequency count, removing stopwords from English and Italian.

---

## Setup Instructions

### Prerequisites

Before running the application, ensure that the following Python packages are installed:

1. **Streamlit** – For the web interface.
2. **pandas** – For manipulating and saving data in Excel files.
3. **aiohttp** – For asynchronous web scraping.
4. **BeautifulSoup4** – For parsing HTML content.
5. **nltk** – For English and Italian stopwords.
6. **spacy** – For advanced tokenization in English and Italian.
7. **openpyxl** – For saving Excel files.
8. **lxml** – For fast HTML parsing.

You can install these dependencies using:

```bash
pip install streamlit pandas aiohttp beautifulsoup4 nltk spacy openpyxl lxml
```

Additionally, download the NLTK stopwords and the necessary spaCy models:

```bash
python -c "import nltk; nltk.download('stopwords')"
python -m spacy download en_core_web_sm
python -m spacy download it_core_news_sm
```

### Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

---

## Usage Instructions

Once the application is running, you will see a web interface with the following sections:

### 1. **Home**

This is the landing page of the application, which provides an overview of the project and explains the two main functionalities:

- **Trustpilot Review Scraper**: Scrape reviews from Trustpilot.
- **Word Count Analyzer**: Analyze word frequencies from the scraped reviews.

### 2. **Scraping Recensioni Trustpilot (Scraping Trustpilot Reviews)**

#### Steps:
1. **Input Trustpilot URL**: Provide the URL of the Trustpilot page you want to scrape reviews from. Example:
   ```
   https://www.trustpilot.com/review/www.mooney.it
   ```

2. **Specify Number of Pages**: Choose how many pages of reviews to scrape (default is 10).

3. **Specify Output File Name**: Choose a name for the Excel file where the reviews will be saved (default is `reviews_output.xlsx`).

4. **Start Scraping**: Click the "Scarica Recensioni" (Download Reviews) button to start the scraping process. The reviews will be saved as an Excel file.

#### Output:
The program will scrape reviews and save them in an Excel file with the following columns:
- `Title`: The title of the review.
- `Body`: The text of the review.
- `Date`: The date the review was posted.
- `Rating`: The rating (1-5 stars) given in the review.
- `Reviewer`: The name of the reviewer.

---

### 3. **Analisi Conteggio Parole (Word Count Analyzer)**

#### Steps:
1. **Upload Excel File**: Upload the Excel file generated by the **Trustpilot Review Scraper**. The file should contain the `Title` and `Body` columns.

2. **Start Analysis**: Click the "Analizza Conteggio Parole" (Analyze Word Count) button. The program will process the reviews, remove stopwords, and generate a list of unique words and their frequencies.

#### Output:
The program will display the unique word count and allow you to download the results as an Excel file (`word_counts.xlsx`). The file will contain:
- `Word`: The unique word found in the reviews.
- `Count`: The frequency of the word across all reviews.

---

## Example Workflow

### Scenario:

1. **Scraping Reviews**:
   - You enter the URL of a Trustpilot page (e.g., `https://www.trustpilot.com/review/www.mooney.it`), choose to scrape 5 pages of reviews, and save the output as `mooney_reviews.xlsx`.

2. **Counting Unique Words**:
   - You upload the `mooney_reviews.xlsx` file and run the word count analysis. The application generates a file called `word_counts.xlsx` that lists all the unique words in the reviews, along with their frequencies.

---

## Troubleshooting

### Common Issues:

- **No Reviews Found**: If no reviews are found, ensure the Trustpilot URL is correct and that the page has published reviews.
- **Invalid File Format**: Ensure the uploaded file for word count analysis contains the `Title` and `Body` columns.
- **Network Issues**: If the scraper fails to fetch reviews, verify your internet connection.

---

## Additional Notes

- **Multilingual Support**: The word count analyzer removes stopwords in both English and Italian, making it suitable for multilingual reviews.
- **Concurrency**: The scraper uses asynchronous requests for faster data collection from multiple pages of Trustpilot reviews.

---

## License

This project is licensed under the MIT License.

---

## Support

If you encounter any issues or have questions about the usage of this project, feel free to contact the developer for assistance.