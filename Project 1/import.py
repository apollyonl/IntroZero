import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://fedglbab:1RTzmSrJiG9GzKOjYJPJtUSiXs1EWgN2@drona.db.elephantsql.com:5432/fedglbab')#os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if(isbn != 'isbn'):
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
        
if __name__ == "__main__":
    main()