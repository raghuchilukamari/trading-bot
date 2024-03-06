import re
import pandas as pd

stocks = pd.read_csv('../output/all_stocks.csv', header='infer')
sp500_dow = pd.read_csv('../output/sp500_dow.csv',header=None)
sp500_dow_list = list(sp500_dow.iloc[:,0].values)

def google_query(search_term):
    if "news" not in search_term:
        search_term=search_term+" stock news"
    url=f"https://www.google.com/search?q={search_term}"
    url=re.sub(r"\s","+",url)
    return url

for index, row in stocks.iterrows():
    pass

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
loader = AsyncChromiumLoader(["https://finance.yahoo.com/quote/TGT/news/"])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
print(docs_transformed)