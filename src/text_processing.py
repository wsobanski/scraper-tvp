
from concurrent.futures import ProcessPoolExecutor
import re
import pandas as pd
import spacy
import pl_core_news_lg
import pickle
from tqdm import tqdm
import logging

nlp = spacy.load('pl_core_news_lg')

str_to_del = ['[WIDEO]',
              '#wieszwiecejPolub nas',
              'Zobacz także.*',
              'Zobacz także ->']

def process_text(sentence):
  doc = nlp(sentence)
  output = []
  for token in doc:
    if not token.is_stop and (token.is_alpha |
                              token.is_digit |
                              token.is_currency |
                              token.is_quote):
      
      output.append(token.lemma_)
      
  return ' '.join(output)

def wrapper(sentence, idx):
    text = process_text(sentence)
    return {'id' : idx,
            'processed_content' : text}
    
def replace_pattern(sentence, pattern):
    return re.sub(pattern, '', sentence)



if __name__ == '__main__':
  
  with open('../obtained_content/full_content.pkl', 'rb') as f:
    data = pickle.load(f) 

  df = pd.DataFrame(data)

  for pattern in str_to_del:
    df['content'] = df['content'].map(lambda x: replace_pattern(x, pattern))
    
  df['idx'] = range(0, df.shape[0])
  
  logging.info('starting processing articles')
  with ProcessPoolExecutor(8) as executor:
    res = list(tqdm(executor.map(wrapper,
                                 df['content'],
                                 df['idx']),
                    total = df.shape[0]))
    
    with open('../clean_content.pkl', 'wb') as f:
      pickle.dump(res, f)
    
  logging.info('starting processing leads')
  with ProcessPoolExecutor(8) as executor:
    res = list(tqdm(executor.map(wrapper,
                                 df['headline'],
                                 df['idx']),
                    total = df.shape[0]))
     
    with open('../clean_headlines.pkl', 'wb') as f:
      pickle.dump(res, f)  