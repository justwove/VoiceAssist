import spacy
from rake_nltk import Rake
from spacy.lang.fr.stop_words import STOP_WORDS

def keywords_extractor(text_path):
    # Charger le modèle français de Spacy
    nlp = spacy.load('fr_core_news_sm')

    # Définir le texte des sous-titres
    with open(text_path, 'r') as file:
        text = file.read()

    # Tokenisation et suppression des stopwords
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text.lower() not in STOP_WORDS]

    # Recombiner les tokens en un seul texte
    clean_text = ' '.join(tokens)

    # Initialiser l'extracteur de mots clés RAKE
    r = Rake(language='french')#, max_length=1)
    r.extract_keywords_from_text(clean_text)
    keywords = r.get_ranked_phrases()

    with open('keywords.txt', 'w') as file:
        file.write('\n'.join(keywords))