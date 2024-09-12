import streamlit as st
import pandas as pd
from io import BytesIO
from collections import Counter
from nltk.corpus import stopwords
from nltk import download
from spacy.lang.en import English
from spacy.lang.it import Italian

# Download stopwords for NLTK
download('stopwords')

# Load spaCy models for English and Italian
nlp_en = English()
nlp_it = Italian()

# Combine stopwords from NLTK for both languages
nltk_stopwords = set(stopwords.words('english')) | set(stopwords.words('italian'))

# Combine stopwords from spaCy for both languages
spacy_stopwords = nlp_en.Defaults.stop_words | nlp_it.Defaults.stop_words

# Final set of stopwords (combining both NLTK and spaCy)
STOPWORDS = nltk_stopwords | spacy_stopwords

def clean_and_tokenize_spacy(text, nlp):
    """Tokenize text using spaCy, remove non-alphabetic tokens and stopwords."""
    doc = nlp(text.lower())
    filtered_words = [token.text for token in doc if token.text.isalpha() and token.text not in STOPWORDS]
    return filtered_words

def count_unique_words_in_reviews(df):
    """Process reviews and count unique words."""
    word_counter = Counter()

    # Iterate through each review and process text
    for index, row in df.iterrows():
        # Combine the title and body of the review
        text = f"{row['Title']} {row['Body']}"
        
        # Tokenize the text using spaCy and remove stopwords
        unique_words_in_review = set(clean_and_tokenize_spacy(text, nlp_en))
        
        # Update global word counter
        word_counter.update(unique_words_in_review)

    # Convert the counter into a DataFrame for sorting and display
    word_counts_df = pd.DataFrame(word_counter.items(), columns=['Word', 'Count']).sort_values(by='Count', ascending=False)
    
    return word_counts_df

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()  # Usa close() invece di save()
    processed_data = output.getvalue()
    return processed_data

# Interfaccia Streamlit
st.title("Analisi del Conteggio delle Parole nelle Recensioni")

# Upload del file Excel
uploaded_file = st.file_uploader("Carica il file Excel con le recensioni", type=["xlsx"])

if uploaded_file is not None:
    # Leggi il file e processa i dati
    df = pd.read_excel(uploaded_file)
    st.write("Ecco le prime righe del file caricato:")
    st.dataframe(df.head())

    # Avvia l'analisi quando l'utente clicca su "Analizza"
    if st.button("Analizza Conteggio Parole"):
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
