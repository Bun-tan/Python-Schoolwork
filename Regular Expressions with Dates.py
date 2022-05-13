'''
File: CoyneSRegEx.py
Class: CSC 272 Spring 2022
Author: Steven C Coyne
Date: 03/25/2022

Description: Uses regular expressions to find dates in a text file and 
convert them to another format. Outputs the converted dates to another file. 
Displays messages about the process to the user.

Problem Statement:

(Regular Expressions: Munging Dates) Dates are stored and displayed in 
several common formats. Four common formats are:

042555
04/25/1955
April 25, 1955
mm-dd-yyyy

Use regular expressions to search a string containing dates, find substrings 
that match these formats and munge them into the format dd MonthName, yyyy. 
The original string should have one date in each format

Read the text from a text file into your python program, munge the date 
formats by replacing with the consistent style. Write the text back out to a 
file named CleanedDateLASTNAME.txt

Author comments:

I stopped short of adding things like leap years or managing the number of 
days in each month. I was a little unsure how to handle a yy -> yyyy 
conversion so I chose to use XXyy, for example XX99 for what might be 1999.
'''

import re

def main():
	'''Obtains text from a file and converts various types of dates found to 
	the format dd MonthName, yyyy, writing the dates to another file'''

	#obtain text from file
	in_filename = 'RawDateCOYNE.txt'
	raw_text, file_found = get_file(in_filename)

	if file_found:
		
		#reference for what the resulting string will look like
		#(it is various forms of the date Python was released)
		#raw_text = '022091\n02/20/1991\nFebruary 20, 1991\n02-20-1991\n'

		#define patterns for regex
		#mmddyy:
		pattern1 = r'(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])(\d{2})'
		#mm/dd/yyyy:
		pattern2 = r'(0[1-9]|1[012])\/(0[1-9]|[12][0-9]|3[01])\/(\d{4})'
		#monthName dd, yyyy:
		pattern3 = r'(January|February|March|April|May|June|July|August|September|October|November|December) (0[1-9]|[12][0-9]|3[01]), (\d{4})'
		#mm-dd-yyyy:
		pattern4 = r'(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])-(\d{4})'

		date_patterns = (pattern1, pattern2, pattern3, pattern4)
	
		print('Original text in file:\n')
		print(raw_text + '\n')

		#extract dates using compatible patterns	
		date_list = []
		#check whole string for each of the patterns
		for pattern in date_patterns:
			#will be a list of tuples like [('02', '20', '91')]. Each tuple
			#is a match and each string in the tuple is from a regex group
			result = re.findall(pattern, raw_text)
			if result: #i.e., if matches are found
				#allows for multiple matches/tuples, although there are no 
				#such cases in our demo file
				for date in result: 
					date_list.append(date)

		#convert dates with custom function (see convert_date for more info)
		converted_dates = []
		for date in date_list:
			#each date variable here is a tuple from findall's results
			#convert_date turns each tuple into a single string
			converted_dates.append(convert_date(date))
		
		#display converted dates
		print('Extracted and converted dates:\n')
		for converted_date in converted_dates:
			print(f"{converted_date}")

		#create and populate output file
		out_filename = 'CleanedDateCOYNE.txt'
		with open(out_filename, mode='w') as out_file:
			for converted_date in converted_dates:
				out_file.write(converted_date + '\n')
			print('\nThe same information has been written to the file '
				+ f'"{out_filename}"')

def get_file(filename):
	'''Obtains designated file or reports an issue if not found'''
	raw_text = ''
	file_found = False
	try:
		with open(filename, 'r') as file:
			raw_text = file.read().rstrip() #one string, no final \n
			file_found = True
	except FileNotFoundError:
		print(f'Could not find the file "{filename}." Please place it in the'
			+ ' same directory as this program.')
	return (raw_text, file_found)
	
def convert_date(date):
	'''Changes submitted dates to the format dd MonthName, yyyy'''
	#takes a tuple of three regex group items as an argument
	#returns a single string, an edited form of the input tuple contents
	month, day, year = date
	months_dict = {'01':'January', '02':'February', '03':'March', 
			'04':'April', '05':'May', '06':'June', '07':'July', 
			'08':'August', '09':'September', '10':'October', 
			'11':'November', '12':'December'}
	if re.fullmatch(r'\d\d', month):
		month = months_dict[month] #convert from number to month name
	if re.fullmatch(r'\d\d', year):
		#century data is missing from the mmddyy format. '19' would work if we
		#"know" the data we have, but XX prevents e.g. 1930/2030 issues
		year = 'XX' + year
	converted_date = f"{day} {month}, {year}"
	#verify that the output conforms to what we want
	output_pattern = r'^(0[1-9]|[12][0-9]|3[01]) (January|February|March|April|May|June|July|August|September|October|November|December), (XX\d\d$|\d{4}$)'
	if re.match(output_pattern, converted_date):
		return converted_date
	else:
		print('**Invalid or unsupported input for date conversion**')
		return 'Invalid'

main()

'''
Output:

Original text in file:

022091
02/20/1991
February 20, 1991
02-20-1991

Extracted and converted dates:

20 February, XX91
20 February, 1991
20 February, 1991
20 February, 1991

The same information has been written to the file "CleanedDateCOYNE.txt"

Case with missing input file:

Could not find the file "RawDateCOYNE.txt." Please place it in the same 
directory as this program.
'''