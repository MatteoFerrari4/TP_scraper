import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Carica i moduli che hai caricato
from scarping_app import scrape_reviews_sync  # Funzione di scraping sincrona
from word_count_app import count_unique_words_in_reviews, to_excel  # Funzione di conteggio parole


# Menu di navigazione con l'aggiunta della Home
menu = ["Home", "Scraping Recensioni Trustpilot", "Analisi Conteggio Parole"]
choice = st.sidebar.selectbox("Seleziona un'opzione", menu)

# Verifica se è il primo caricamento
if 'first_load' not in st.session_state:
    st.session_state.first_load = True
    st.rerun()  # Forza il refresh

# Se il refresh è già avvenuto, disattiva il flag
if st.session_state.first_load:
    st.session_state.first_load = False

# Landing Page (README)
if choice == "Home":
    st.title("Trustpilot Review Scraper & Word Count")
    st.subheader("Benvenuti nell'applicazione per la raccolta e l'analisi delle recensioni di Trustpilot")
    st.markdown("""
    ### README for Trustpilot Review Scraper and Word Count Program (Streamlit Version)

    ## Introduction
    This README explains how to use the **Trustpilot Review Scraper** and the **Unique Word Count Program**, provided as part of a **Streamlit web application**. These tools are designed to work together to collect customer reviews from **Trustpilot** and analyze the unique words in those reviews. The entire process is streamlined into two easy steps, which can be accessed through the application’s interface.

    ## Workflow Overview
    1. **Step 1: Scraping Reviews from Trustpilot**
       - Use the **Scraping Recensioni Trustpilot** section in the app to scrape reviews from a Trustpilot company page.
       - The reviews are saved in an Excel file that contains columns for the review title, body, date, rating, and reviewer name.
    
    2. **Step 2: Counting Unique Words from Reviews**
       - Use the **Analisi Conteggio Parole** section in the app to analyze the Excel file generated from Step 1.
       - The program combines the title and body of each review, removes common stopwords, and generates a new Excel file that lists the unique words along with their frequency across all reviews.

    ## Troubleshooting
    - **No Reviews Found**: Ensure the Trustpilot URL is correct.
    - **Network Issues**: Verify your internet connection.

    ## Prerequisites
    - No installation of external libraries is required. Simply upload your files in the app.

    ### Example Outputs
    - Scraped Reviews (`mooney_reviews.xlsx`)
    - Word Count (`word_counts.xlsx`)
    """)
    
# Sezione per lo scraping delle recensioni
elif choice == "Scraping Recensioni Trustpilot":
    st.subheader("Scraping delle Recensioni")

    # Input URL Trustpilot
    url = st.text_input("Inserisci URL della pagina Trustpilot", key="scraping_url")
    
    # Numero di pagine da analizzare
    num_pages = st.number_input("Numero di pagine da scaricare", min_value=1, max_value=100, value=10, key="scraping_num_pages")
    
    # Nome del file output
    file_name = st.text_input("Nome del file Excel per salvare le recensioni", "reviews_output", key="scraping_file_name")
    
    # Avvia lo scraping quando l'utente clicca su "Scarica"
    if st.button("Scarica Recensioni", key="scraping_button"):
        if url:
            output_file = f"{file_name}.xlsx"
            reviews = scrape_reviews_sync(url, num_pages)  # Usa la funzione sincrona per lo scraping

            # Controlla se ci sono recensioni trovate
            if not reviews:
                st.error("Nessuna recensione trovata.")
            else:
                # Crea un DataFrame e salva le recensioni in Excel
                reviews_df = pd.DataFrame(reviews, columns=['Title', 'Body', 'Date', 'Rating', 'Reviewer'])
                reviews_df.to_excel(output_file, index=False)
                st.success(f"Recensioni scaricate e salvate in {output_file}")
        else:
            st.error("Inserisci un URL valido di Trustpilot")

# Sezione per l'analisi del conteggio parole
elif choice == "Analisi Conteggio Parole":
    st.subheader("Analisi del Conteggio delle Parole")

    # Upload del file Excel
    uploaded_file = st.file_uploader("Carica il file Excel con le recensioni", type=["xlsx"], key="wordcount_file_upload")
    
    if uploaded_file is not None:
        # Leggi il file e processa i dati
        df = pd.read_excel(uploaded_file)
        st.write("Ecco le prime righe del file caricato:")
        st.dataframe(df.head())
        
        # Avvia l'analisi quando l'utente clicca su "Analizza"
        if st.button("Analizza Conteggio Parole", key="wordcount_button"):
            word_counts_df = count_unique_words_in_reviews(df)

            # Mostra i risultati
            st.write("Conteggio delle parole uniche:")
            st.dataframe(word_counts_df)

            # Prepara il file Excel per il download
            excel_data = to_excel(word_counts_df)

            # Offri un link per scaricare il file con il conteggio delle parole
            st.download_button(label="Scarica il file con il conteggio delle parole",
                               data=excel_data,
                               file_name='word_counts.xlsx',
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")