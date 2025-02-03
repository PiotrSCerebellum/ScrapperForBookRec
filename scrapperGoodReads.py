import requests
from bs4 import BeautifulSoup
import json

def get_books_from_goodreads(url,amount):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    book_elements = soup.select(".bookTitle")
    book_elements = book_elements[:min(len(book_elements), amount)]
    
    for book in book_elements:
        title = book.text.strip()
        book_url = "https://www.goodreads.com" + book["href"]
        
        # Fetch book details
        book_response = requests.get(book_url, headers=headers)
        if book_response.status_code != 200:
            continue
        
        book_soup = BeautifulSoup(book_response.text, "html.parser")
        blurb_element = book_soup.select_one(".DetailsLayoutRightParagraph__widthConstrained")
        blurb = blurb_element.text.strip() if blurb_element else "No description available."
        
        cover_element = book_soup.select_one("img[class='ResponsiveImage']")
        cover_link = cover_element["src"] if cover_element else ""

        author=book_soup.select_one('[class="ContributorLink__name"]').text

        
        
        books.append({
            "title": title,
            "blurb": blurb,
            "purchaseLink": book_url,
            "fullText": "",
            "author": author,
            "coverLink": cover_link
        })
    
    return books


links=[]
with open('./goodreads_links.txt', 'r', encoding='utf-8') as file:
    for line in file:
       links.append(line)
for link in links:
    print(link)
    books_data = get_books_from_goodreads(url=link,amount=10)
    with open("books.json", "a", encoding="utf-8") as f:
        json.dump(books_data, f, indent=4)
