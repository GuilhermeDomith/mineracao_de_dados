import pandas as pd
import numpy as np
import bs4, requests, re, nltk, pickle
from unicodedata import normalize
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import  cosine_similarity


with open('tfidf_vectorizer', 'rb') as f:
    vectorizer = pickle.load(f)
    
df_words = pd.read_csv('data/df_words_tfidf.csv')
df_gizmodo = pd.read_csv('data/noticias_gizmodo.csv')

stemmer = None
stopwords = None


def _processar_texto(texto):
    global stemmer, stopwords

    if texto is None or not texto:
        return ''

    if stopwords is None:
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords = normalize('NFKD', ' '.join(stopwords)).encode('ASCII', 'ignore').decode().split()

    if stemmer is None:
        stemmer = nltk.stem.RSLPStemmer()

    # Trasnformação do texto em minúsculo e remoção de termo
    texto = str(texto).lower()

    # Removendo acentuação
    texto = normalize('NFKD', texto).encode('ASCII', 'ignore').decode()

    # Removendo Pontuação, stopwords, palavras com número e aplicando stemming
    texto = ' '.join([stemmer.stem(c) for c in nltk.word_tokenize(texto) 
                    if (c not in punctuation) and (c not in stopwords) and not (re.match('.*[\d_].*', c)) ])

    return texto


def obter_noticias_similares(texto_pesquisa=''):
    texto = _processar_texto(texto_pesquisa)
    df_texto = pd.DataFrame({'doc': [texto]})
    
    df_words_pesquisa = pd.DataFrame(
                            vectorizer.transform(df_texto['doc']).todense(),
                            columns=vectorizer.get_feature_names()
                        )
    
    df_words_pesquisa = df_words.append(df_words_pesquisa, ignore_index=True, sort=False)
    
    # Obtém a similaridade das palavras
    sim = cosine_similarity(df_words_pesquisa)
    
    # Obtém as similaridades dá última coluna, referente ao texto pesquisado
    coluna_pesquisa = pd.Series(sim[-1])
    
    return obter_lista_noticias_dict( 
                df_gizmodo.loc[ coluna_pesquisa.sort_values(ascending=False)[1:].index ],
                n_noticias=10
            )


def obter_lista_noticias_dict(df=df_gizmodo, n_noticias=5):
    return df.iloc[:n_noticias].to_dict(orient='records')
