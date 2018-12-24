import pickle, json, nltk, re
import pandas as pd
from string import ascii_lowercase, punctuation
from unicodedata import normalize

vectorizer = None
model_mpl = None
stopwords = None



def remover_acentuacao(texto):
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode()


def processar_texto(texto):
    if texto is None or not texto:
        return ''

    # Trasnformação do texto em minúsculo e remoção de termo
    texto = str(texto).lower()

    # Removendo acentuação
    texto = remover_acentuacao(texto)

    # Removendo Pontuação, stopwords, palavras com número e aplicando stemming
    texto = ' '.join([c for c in nltk.word_tokenize(texto) 
                      if (c not in punctuation) 
                      and (c not in stopwords) 
                      and not (re.match(r'.*[\d_].*', c)) 
                      and len(c) > 2
                     ])

    return texto



def vetorizar_textos(textos):
    tfidf_matrix = vectorizer.transform(textos)    
    df_words = pd.DataFrame(tfidf_matrix.todense(), columns=vectorizer.get_feature_names())
    
    return df_words



def predict_notices(notices):
    
    if isinstance(notices, str):
        notices = [notices]
        
    if isinstance(notices, pd.Series):
        notices = list(notices)
        
    df_notices = pd.DataFrame(notices, columns=['n'])
    df_notices = df_notices['n'].apply(processar_texto)
                              
    df_words_not = vetorizar_textos(df_notices)
    
    predict = model_mpl.predict(df_words_not)
    predict_proba = model_mpl.predict_proba(df_words_not)
    
    return predict, predict_proba

def obter_porcentagem(predict_proba):
    return [(float('%.3f'%p[0]), float('%.3f'%p[1])) for p in predict_proba]


def _inicializar():
    global vectorizer, model_mpl, stopwords

    with open('data/vectorizer', 'rb') as file:
        vectorizer = pickle.load(file)

    with open('data/model', 'rb') as file:
        model_mpl = pickle.load(file)

    with open('data/stopwords.json', 'r') as file:
        stopwords = json.load(file)


_inicializar()