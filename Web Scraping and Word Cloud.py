'''
CoyneSLab4a.py
CSC 272 Spring 2022
Author: Steven C Coyne
Date: 04/14/2022

Lab 4: Natural Language Processing

Description: Demonstrates web scraping and word cloud generation using various
NLP libraries. Displays and saves an image of the word cloud.

Problem Statement (adapted from Deitel & Deitel pg. 511):

12.1 (Web Scraping with the Requests and Beautiful Soup Libraries)

Use the requests library to download the www.python.org home page’s content. 
This is called web scraping. Then use the Beautiful Soup library to extract 
only the text from the page. Eliminate the stop words in the resulting text, 
then use the wordcloud module to create a word cloud based on the text.
'''

import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from wordcloud import WordCloud

def main():
	'''Scrapes a specified website, cleans the text, and displays a word cloud 
	based on the page's word frequency information.'''
	url = 'https://www.python.org'
	text = scrape_site(url)
	processed_text = remove_stops(text)
	generate_wordcloud(processed_text)

def scrape_site(url):
	'''Obtains the text of the designated website, removing various tags'''
	response = requests.get(url) #get website contents
	soup = BeautifulSoup(response.content, 'html5lib')
	text = soup.get_text(strip=True) #remove tags
	return text

def remove_stops(text):
	'''Removes stopwords from the input text.'''
	stops = stopwords.words('english')
	#I used a simple join since I found it easier to make word clouds from a 
	#string than other data like blobs or a dictionary of words and frequencies
	processed_text = ' '.join([word for word in text.split() if word not in stops])
	return processed_text

def generate_wordcloud(processed_text):
	'''Creates a word cloud from the input text, displaying it on screen and
	saving it to disk as well. It is recommended to remove stop words first.'''

	#I arbirarily set various settings to produce a cloud of my liking
	wordcloud = WordCloud(width=800, height=400, colormap='hsv', min_word_length=2,
	min_font_size=10, background_color='white', include_numbers=False)
	wordcloud = wordcloud.generate(processed_text)
	#display the plot in ipython/etc
	plt.imshow(wordcloud)
	plt.axis('off')
	plt.show()
	#save plot to disk
	wordcloud = wordcloud.to_file('PythonWordCloud.png')

main()

'''
Output:

(A plot representing word frequency data from https://www.python.org)

(No output to command line)
'''