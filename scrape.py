'''Goodreads web scraper'''
import re
import csv
import requests
from bs4 import BeautifulSoup


# Genres to collect books about
genres = ['Fiction','Business','Science','History',"Children-s",'Horror','Thriller','Sports',
'Psychology','Travel']


# Collect books for each genre.
for genre in genres:
    genre_books =[]
    # Collect books from pages; each page contains 50 books.
    NUMBER_OF_PAGES = 20
    for page in range(0,NUMBER_OF_PAGES):
        source = requests.get(f"https://www.goodreads.com/shelf/show/{genre}?page={page}").text

        # Scrape the source
        soup = BeautifulSoup(source, 'lxml')

        # Collect all book in the page in a container
        books_container = soup.find_all('div',class_='left')

        # Collect each book from the container
        for book in books_container:
            # Extract book title.
            title = book.find('a', class_='bookTitle').text.lower()
            title = re.sub('[^A-Za-z0-9\s]',"",title)
            # Extract book author.
            author = book.find('a', class_='authorName').text.lower()
            # Extract meta data.
            meta_data = book.find('span', class_='greyText smallText').text
            # Strip white-spaces from metadata, and split values when encounter "—".
            stripped_meta_data = "".join(meta_data.split()).split("—")
            # Extract avrage rating from meta data.
            avg_rating = re.sub("[a-zA-z]","",stripped_meta_data[0])
            # Extract total rating from meta data.
            rating = re.sub("[a-zA-z,]","",stripped_meta_data[1])
            # Extract published year from meta data.
            year = re.sub("[a-zA-z]","",stripped_meta_data[2])


            # Add book to the genre books
            genre_books.append([title,author,avg_rating,rating,year,genre.lower()])

    all_books.append(genre_books)

    # Write the collect genre books into a csv file
    with open(f"{genre.lower()}.csv","w", newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(genre_books)