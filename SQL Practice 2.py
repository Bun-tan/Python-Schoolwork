'''
CoyneSLab6b.py
CSC 272 Spring 2022
Author: Steven C Coyne
Date: 04/25/2022

Lab 6: Database Management Systems

Description: Demonstrates various SQL commands in Python

Problem Statement (adapted from Deitel & Deitel pg. 799):

17.3 (Contacts Database) 

Study the books.sql script provided in the ch17 examples folder’s sql subfolder.
Save the script as addressbook.sql and modify it to create a single table named 
contacts. The table should contain an auto-incremented id column and text columns
for a person’s first name, last name and phone number. Insert contacts into the 
database, query the database to list all the contacts and contacts with a 
specific last name, update a contact and delete a contact. 
'''

import sqlite3
import pandas as pd

#connect to the database
connection = sqlite3.connect('addressbook.db')

#establish cursor for insert/update/delete operations
cursor = connection.cursor()

#Insert contacts into the database
cursor = cursor.execute("""INSERT INTO contacts (first, last, phone) \
				VALUES ('Steven','Coyne', '(609) 555-8213')""")
cursor = cursor.execute("""INSERT INTO contacts (first, last, phone) \
				VALUES ('Ronlad','Coyne', '(856) 555-5309')""")

#query the database to list all the contacts
print('All contacts in the database:\n')
df = pd.read_sql("""SELECT * \
				FROM contacts""", connection, index_col=['id'])
print(df)

#query the database to list all the contacts with a specific last name
print('\nAll contacts in the database with last name "Deitel":\n')
df = pd.read_sql("""SELECT * \
				FROM contacts \
				WHERE last LIKE 'Deitel'""", connection, \
				index_col=['id'])
print(df)

#update a contact
print('\nFixing misspelled first name:\n')
cursor = cursor.execute("""UPDATE contacts SET first='Ronald' \
				WHERE first='Ronlad' AND Last='Coyne'""")
#display updated data
df = pd.read_sql("""SELECT * \
				FROM contacts \
				WHERE first='Ronald' AND Last='Coyne'""", connection, \
				index_col=['id'])
print(df)

#delete a contact
print('\nRemoving "Steven Coyne":\n')
cursor = cursor.execute("""DELETE FROM contacts \
				WHERE first='Steven' AND Last='Coyne'""")
#confirm deletion
print('All contacts in the database:\n')
df = pd.read_sql("""SELECT * \
				FROM contacts""", connection, index_col=['id'])
print(df)

'''
Output:

All contacts in the database:

        first    last           phone
id
1        Paul  Deitel  (856) 555-2022
2      Harvey  Deitel  (856) 555-2020
3       Abbey  Deitel  (609) 555-5981
4         Dan   Quirk  (609) 555-1092
5   Alexander    Wald  (856) 555-0188
6      Steven   Coyne  (609) 555-8213
7      Ronlad   Coyne  (856) 555-5309

All contacts in the database with last name "Deitel":

     first    last           phone
id
1     Paul  Deitel  (856) 555-2022
2   Harvey  Deitel  (856) 555-2020
3    Abbey  Deitel  (609) 555-5981

Fixing misspelled first name:

   first   last           phone
id
7  Ronald  Coyne  (856) 555-5309

Removing "Steven Coyne":

All contacts in the database:

        first    last           phone
id
1        Paul  Deitel  (856) 555-2022
2      Harvey  Deitel  (856) 555-2020
3       Abbey  Deitel  (609) 555-5981
4         Dan   Quirk  (609) 555-1092
5   Alexander    Wald  (856) 555-0188
7      Ronald   Coyne  (856) 555-5309
'''