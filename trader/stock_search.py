import pandas as pd
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
pd.set_option('display.max_colwidth', None)
load_dotenv()
tool = TavilySearchResults()

res = tool.invoke({"query": "TGT stock news"})
news = pd.DataFrame(res)
print(news)

# from langchain_community.document_loaders import AsyncChromiumLoader
# from langchain_community.document_transformers import BeautifulSoupTransformer
#
# # Load HTML
# loader = AsyncChromiumLoader(["https://www.google.com/search?q=TGT+stock+news"])
# html = loader.load()
#
# # Transform
# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
#

