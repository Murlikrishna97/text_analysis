import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_article_content(url_id, url):
    try:
        response = requests.get(url)
        content_list = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            header_tag = soup.find('h1')
            if header_tag is not None:
                header_tag = header_tag.get_text(strip=True)
                content_list.append(header_tag)
                print("Header available", end=" ")
            article_tag = soup.find('article')
            if article_tag:

                paragraphs = article_tag.find_all(['p', 'ol'])

                for tag in paragraphs:
                    if tag.name == 'p':
                        content_list.append(tag.get_text())
                    elif tag.name == 'ol':
                        list_items = tag.find_all('li')
                        for item in list_items:
                            content_list.append(item.get_text())

                content_list = [text.replace('\xa0', '') for text in content_list]
                content_string = "\n".join(content_list)

                with open(f"./content/{url_id}.txt", 'w', encoding='utf-8') as file:
                    file.write(content_string)

                print(f"Content written to '{url_id}.txt' successfully.")

            else:
                print(f"Article tag not found for {url_id}.")
        else:
            print(f"Failed to retrieve content for {url_id}. Status code: {response.status_code}")
    except Exception as e:
        print("Exception Raised : ", e)

# url = "https://insights.blackcoffer.com/covid-19-environmental-impact-for-the-future/"
# url_id = "blackassign00011"
# scrape_article_content(url_id, url)

xlsx_file_path = 'Input.xlsx'
df = pd.read_excel(xlsx_file_path)

for index, row in df.iterrows():
    for column, value in list(row.items()):
        if column == 'URL_ID':
            url_id = value
        elif column == 'URL':
            url = value

    scrape_article_content(url_id, url)

# 36 and 49
