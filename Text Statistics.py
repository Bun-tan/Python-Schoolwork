'''
File: CoyneSProject2.py
Class: CSC 272 Spring 2022
Author: Steven C Coyne
Date: 03/16/2022

Option 2: Text Analysis (Based on Deitel & Deitel 9.12, pg. 351)

Problem Statement

Write a script that reads the text from the file, then displays statistics 
about it, including the total word count, the total character count, the 
average word length, the average sentence length, a word distribution of 
the words frequencies, and the top 10 longest words.


This was originally done with a file containing the text of Frankenstein.
'''

import re
import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

def main():
	'''Analyzes a text file and displays statistics about the content in 
	terms of characters, words, and sentences.'''

	#obtain text file to process
	filename = 'FrankensteinCleaned.txt'
	raw_text, file_found = get_file(filename)

	if file_found:
		#count characters, excluding newlines
		char_count = character_count(raw_text)

		#split text into sentences and store them along with length of each
		sentences = get_sentences(raw_text)
		sentence_lengths = [len(sentence.split()) for sentence in sentences]

		#remove punctuation and other symbols
		cleaned_text = clean_text(raw_text)
		#split text into tokens
		tokenized_text = tokenize_text(cleaned_text)

		#obtain word data from the processed and tokenized text
		words, occurances = np.unique(tokenized_text, return_counts=True)
		word_lengths = [len(word) for word in words]

		#add data to dataframe for analysis and plotting purposes
		df = pd.DataFrame({'Words': words, 'Occurances': occurances, 
			'Length': word_lengths})

		#display statistics
		print(f'Information about the text in {filename}:')
		print()
		print(f'Word count: {sum(occurances)}')
		print(f'Character count: {char_count}')
		print('Average word length: '
			+ f'{statistics.mean(word_lengths):.2f} characters')
		print('Average sentence length: '
			+ f'{statistics.mean(sentence_lengths):.2f} words')
		print()
		print('Top ten longest words in the text:')
		print()
		#loop to print the longest words, chosen over pandas display 
		#methods to minimize formatting syntax
		for word in df.sort_values('Length', ascending=False)['Words'][:10]:
			print(word)
		print()


		print('Generating a graph of word distributions...')
		#display word frequency chart
		#configured to display a readable list of 50. 
		title = f'Word Frequencies in {filename} (top 50 shown)'
		sorted_df = df.sort_values('Occurances', ascending=False)
		chart = sorted_df[:50].plot.bar(y='Occurances')
		chart.set_title(title)
		chart.set_xticklabels(sorted_df['Words'][:50], size=7)
		plt.show()

def get_file(filename):
	'''Obtains designated file or reports an issue if not found'''
	raw_text = ''
	file_found = False
	try:
		with open(filename, 'r') as file:
			raw_text = file.read()
			file_found = True
	except FileNotFoundError:
		print(f'Could not find the file "{filename}." Please place it in the'
			+ ' same directory as this program.')
	return (raw_text, file_found)

def character_count(raw_text):
	'''Counts characters in the provided string, ignoring newlines.'''
	char_count = len(re.sub(r'[\n]', '', raw_text))
	return char_count

def get_sentences(raw_text):
	'''Splits text by sentence, using common terminal punctuation.'''
	sentences = re.split(r'[.!?]+', raw_text)
	return sentences

def clean_text(raw_text):
	'''Removes case, punctuation, and misc symbols.'''
	lowercase_text = raw_text.lower()
	#one may remove '-' from regular expression to split hyphenated words 
	#like "self-interest." Microsoft Word and Google Docs consider these one 
	#word for counting purposes, so I have chosen to do so as well.
	processed_text = re.sub(r"[^a-z'-]", " ", lowercase_text)
	return processed_text

def tokenize_text(cleaned_text):
	'''Splits text into individual words on whitespace.'''
	tokenized_text = cleaned_text.split()
	return tokenized_text

main()

'''
Output:

Information about the text in FrankensteinCleaned.txt:

Word count: 75176
Character count: 411672
Average word length: 7.36 characters
Average sentence length: 22.27 words

Top ten longest words in the text:

characteristically
self-satisfaction
half-extinguished
indiscriminately
impracticability
soul-inspiriting
perpendicularity
presence-chamber
fellow-creatures
self-accusations

Generating a graph of word distributions...

#after removing the file:

Could not find the file "FrankensteinCleaned.txt." Please place it in the 
same directory as this program.
'''