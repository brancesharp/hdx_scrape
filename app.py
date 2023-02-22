from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.title("Web Scrape")

hdx_url = st.text_input("Input URL")

scrape = st.button("Start Web Scrape")

if scrape:
    def getHTMLdocument(url):
        response = requests.get(url)
        return response.text
    url_to_scrape = hdx_url
    html_document = getHTMLdocument(url_to_scrape)
    soup = BeautifulSoup(html_document, 'html.parser')

    links = []

    for link in soup.find_all('a', attrs={'href': re.compile("^/cp_prod/CatNav.aspx")}):
        links.append(link.get('href'))

    url_prefix = 'https://catalog.hardydiagnostics.com/'
    links2 = (url_prefix + pd.Series(links)).to_list()

    prod_title = []
    prod_desc = []

    for link in links2:
        url = link
        web_doc = getHTMLdocument(url)
        soup = BeautifulSoup(web_doc, "html.parser")
        title = soup.find(id='spanShortDesc').get_text()
        description = soup.find(id='spanDetailDesc').get_text()
        prod_title.append(title)
        prod_desc.append(description)

    zipped_df = list(zip(prod_title, prod_desc))
    scrape_df = pd.DataFrame(zipped_df, columns=['Item', 'Description'])

    st.success('Done!')
    st.dataframe(scrape_df)

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(scrape_df)

    st.download_button(
        label="Download as CSV",
        data = csv,
        file_name = 'output.csv',
    )
