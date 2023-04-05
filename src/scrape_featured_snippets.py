import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

df_kw = pd.read_csv('../data/input/kw.csv', header = None)
df_kw = df_kw.rename(columns = {0: 'kw'})

def scrape_featured_snippets(row):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    header = {
        'User-Agent': user_agent
    }

    url = 'https://www.google.co.jp/search'
    kw = row['kw']
    req = requests.get(url, params={'q': kw}, headers=header)

    soup = BeautifulSoup(req.text, 'html.parser')

    print('kw:' + kw)
    
    try:
        scraped_featured_snippets_text = soup.select_one('block-component div[class="wDYxhc"]').text
        scraped_featured_snippets_url = soup.select_one('block-component div[class="yuRUbf"] a').get('href').split('#:~:text=')[0]

        time.sleep(1)
        return pd.Series([scraped_featured_snippets_text, scraped_featured_snippets_url])
    except:
        print('強調スニペットなし')

        time.sleep(1)
        return pd.Series([''])

df_kw[['scraped_featured_snippets_text', 'scraped_featured_snippets_url']] = df_kw.apply(scrape_featured_snippets, axis=1)

df_kw.to_csv('../data/output/result.csv', encoding='utf_8_sig', index=None)