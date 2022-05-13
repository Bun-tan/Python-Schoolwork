'''
CoyneSLab6a.py
CSC 272 Spring 2022
Author: Steven C Coyne
Date: 04/25/2022

Lab 6: Database Management Systems

Description: Demonstrates various SQL commands in Python with sqlite3

Problem Statement (adapted from Deitel & Deitel pg. 799):

17.1 (Books Database) 

Perform each of the following tasks on the books database from Section 17.2:

a) Select all authors’ last names from the authors table in descending order.
b) Select all book titles from the titles table in ascending order.
c) Use an INNER JOIN to select all the books for a specific author. Include the
title,copyright year and ISBN. Order the information alphabetically by title.
d) Insert a new author into the authors table.
e) Insert a new title for an author. Remember that the book must have an entry
in the author_ISBN table and an entry in the titles table. 
'''

import sqlite3
import pandas as pd

#connect to the database
connection = sqlite3.connect('books.db')

#perform several queries
print('a) Select all authors’ last names from the authors table in descending '
	+ 'order:\n')
df = pd.read_sql("""SELECT last \
				FROM authors \
				ORDER BY last DESC""", connection)
print(df)

print('\nb) Select all book titles from the titles table in ascending order:\n')
df = pd.read_sql("""SELECT title \
				FROM titles \
				ORDER BY title ASC""", connection)
print(df)

#query a particular author (I chose Abbey Deitel)
print('\nc) Select all the books for a specific author (Abbey Deitel). '
	+ 'Include the title, copyright year and ISBN. Order the information '
	+ 'alphabetically by title:\n')
df = pd.read_sql("""SELECT title, copyright, titles.isbn \
				FROM titles \
				INNER JOIN author_ISBN \
					ON titles.isbn = author_ISBN.isbn \
				INNER JOIN authors \
					ON authors.id = author_ISBN.id \
				WHERE first='Abbey' AND last='Deitel' \
				ORDER BY title ASC""", connection)
print(df)

#establish cursor for insert operations
cursor = connection.cursor()

#inserting a new author and book. I chose a programming book from another course
print('\nd) Insert a new author into the authors table.\n')
cursor = cursor.execute("""INSERT INTO authors (first, last) \
				VALUES ('Y. Daniel','Liang')""")

#confirm insertion and report
df = pd.read_sql("""SELECT * \
				FROM authors \
				WHERE first='Y. Daniel' AND last='Liang'""", connection, index_col=['id'])
print('Displaying new author:\n')
print(df)

print('\ne) Insert a new title for an author.\n')
cursor = cursor.execute("""INSERT INTO titles (isbn, title, edition, copyright) \
				VALUES ('0136519962', \
				'Introduction to Java Programming and Data Structures', \
				12,'2020')""")
cursor = cursor.execute("""INSERT INTO author_ISBN (id,isbn) \
				VALUES (6,'0136519962')""")

#confirm insertion and report
df = pd.read_sql("""SELECT title, copyright, titles.isbn \
				FROM titles \
				INNER JOIN author_ISBN \
					ON titles.isbn = author_ISBN.isbn \
				INNER JOIN authors \
					ON authors.id = author_ISBN.id \
				WHERE first='Y. Daniel' AND last='Liang'""", connection)
print('Displaying new title:\n')
print(df)

#disconnect from the database
connection.close()

'''
Output:

a) Select all authors’ last names from the authors table in descending order:

     last
0    Wald
1   Quirk
2  Deitel
3  Deitel
4  Deitel

b) Select all book titles from the titles table in ascending order:

                              title
0         Android 6 for Programmers
1            Android How to Program
2                  C How to Program
3                C++ How to Program
4     Internet & WWW How to Program
5     Intro to Python for CS and DS
6               Java How to Program
7  Visual Basic 2012 How to Program
8          Visual C# How to Program
9         Visual C++ How to Program

c) Select all the books for a specific author (Abbey Deitel). Include the title, copyright year and ISBN. Order the information alphabetically by title:

                              title copyright        isbn
0     Internet & WWW How to Program      2012  0132151006
1  Visual Basic 2012 How to Program      2014  0133406954

d) Insert a new author into the authors table.

Displaying new author:

        first   last
id
6   Y. Daniel  Liang

e) Insert a new title for an author.

Displaying new title:

                                               title copyright        isbn
0  Introduction to Java Programming and Data Stru...      2020  0136519962
'''