# Text Analysis from Web Articles

This repository contains a Python program designed to extract textual data articles from given URLs and perform text analysis to compute various variables as specified in the assignment.

## 1. Objective:

The objective of this assignment is to extract textual data articles from the given URLs and perform text analysis to compute variables such as positive score, negative score, polarity score, subjectivity score, etc.

## 2. Data Extraction:

### Input:
The input data is provided in an Excel file named `Input.xlsx`. For each article in the input file, the program extracts the article title and text from the corresponding URL. The extracted articles are saved in text files with the URL_ID as the file name.

### Approach:
Python programming is utilized for data crawling and extraction. The program utilizes libraries such as BeautifulSoup, Selenium, or Scrapy for web scraping to ensure the extraction of only the article text without including website headers, footers, or any other irrelevant content.

## 3. Data Analysis:

For each extracted article, the program performs textual analysis to compute variables specified below. The textual analysis is conducted using Python programming.

Sure, here's the updated section including all the specified variables:

## 4. Variables:

The program computes the following variables during text analysis:

1. **POSITIVE SCORE**
2. **NEGATIVE SCORE**
3. **POLARITY SCORE**
4. **SUBJECTIVITY SCORE**
5. **AVG SENTENCE LENGTH**
6. **PERCENTAGE OF COMPLEX WORDS**
7. **FOG INDEX**
8. **AVG NUMBER OF WORDS PER SENTENCE**
9. **COMPLEX WORD COUNT**
10. **WORD COUNT**
11. **SYLLABLE PER WORD**
12. **PERSONAL PRONOUNS**
13. **AVG WORD LENGTH**

The definition and calculation methodology for each of these variables can be found in the "Text Analysis.docx" file. The program computes these variables for each extracted article and saves the results in the output file as specified in the "Output Data Structure.xlsx" file.

## 5. Output Data Structure:

The output data structure consists of the following variables:
1. All input variables from `Input.xlsx`.
2. Additional variables computed during text analysis.

The output is provided in either CSV or Excel format as specified in the "Output Data Structure.xlsx" file.
