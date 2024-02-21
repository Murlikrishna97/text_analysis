import os
import nltk
from nltk.corpus import cmudict, stopwords
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')

cmu_dict = cmudict.dict()

df = pd.DataFrame(columns=[
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
    'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
    'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
    'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
])

def load_custom_stopwords(folder_path):
    custom_stopwords = set()

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='latin-1') as file:
                stopwords_in_file = file.read().splitlines()
                stopwords_in_file = [(words.split()[0]).lower() for words in stopwords_in_file]
                custom_stopwords.update(stopwords_in_file)

    return custom_stopwords


def clean_text(text, custom_stopwords=None):
    stop_words = set(stopwords.words('english'))

    if custom_stopwords is not None:
        stop_words.update(custom_stopwords)

    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() or word.isalpha()]
    words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)
    return cleaned_text

def positive_negative_function(positive_negative_folder):
    positive_negative_dict = {}
    for filename in os.listdir(positive_negative_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(positive_negative_folder, filename)
            with open(file_path, 'r', encoding='latin-1') as file:
                positive_negative_in_file = file.read().splitlines()
                positive_negative_in_file = [(words.split()[0]).lower() for words in positive_negative_in_file]
                if "positive" in filename:
                    positive_negative_dict["positive"] = positive_negative_in_file
                elif "negative" in filename:
                    positive_negative_dict["negative"] = positive_negative_in_file
    return positive_negative_dict


def read_text_content(text_folder_path):
    with open(file_path_text, "r", encoding='latin-1') as file:
        sample_text = file.readlines()
        sample_text = "".join(sample_text)
    return sample_text


def calculate_sentiment_scores(text, positive_negative_dict):
    words = word_tokenize(text)
    # words = [word.lower() for word in words if word.isalnum() or word.isalpha()]
    positive_score = sum(1 for word in words if word in positive_negative_dict['positive'])
    negative_score = sum(1 for word in words if word in positive_negative_dict['negative'])

    # Calculate Polarity Score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # Calculate Subjectivity Score
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score



# def syllable_count(word):
#     """Count the number of syllables in a word."""
#     # d = cmudict.dict()
#     if word.lower() in cmu_dict:
#         return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
#     else:
#         return 1

def syllable_count(word):
    """Count the number of syllables in a word."""
    if word.lower() in cmu_dict:
        # Handle exceptions for words ending with "es" or "ed"
        if word.lower().endswith(('es', 'ed')) and len(cmu_dict[word.lower()]) > 1:
            return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()][:-1]])
        else:
            return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        # If the word is not found in the CMU Pronouncing Dictionary, return a default count of 1
        return 1

def calculate_readability_scores(cleaned_text):
    sentences = sent_tokenize(cleaned_text)
    words = word_tokenize(cleaned_text)

    avg_sentence_length = len(words) / len(sentences)

    # Identify complex words and calculate the Percentage of Complex Words
    complex_words = [word for word in words if syllable_count(word) > 2]
    percentage_complex_words = (len(complex_words) / len(words)) * 100

    # Calculate Fog Index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate Average Number of Words Per Sentence
    avg_words_per_sentence = len(words) / len(sentences)

    # Count Complex Word, Word Count, and Syllables Per Word
    count_complex_words = len(complex_words)
    word_count = len(words)
    syllables_per_word = sum(syllable_count(word) for word in words) / word_count

    # Identify and count Personal Pronouns
    personal_pronouns = ['I', 'we', 'my', 'ours', 'us']
    count_personal_pronouns = sum(1 for word in words if word.lower() in personal_pronouns)

    # Calculate Average Word Length
    avg_word_length = sum(len(word) for word in words) / word_count

    return (
        avg_sentence_length, percentage_complex_words, fog_index,
        avg_words_per_sentence, count_complex_words, word_count,
        syllables_per_word, count_personal_pronouns, avg_word_length
    )

def get_url_url_id():
    xlsx_file_path = 'Input.xlsx'
    df_url = pd.read_excel(xlsx_file_path)
    my_dict = dict(zip(df_url['URL_ID'], df_url['URL']))
    return my_dict

if __name__ == "__main__":
    custom_stopwords_folder = 'StopWords'
    custom_stopwords = load_custom_stopwords(custom_stopwords_folder)
    text_folder_path = "content"
    url_dict = get_url_url_id()

    for filename in os.listdir(text_folder_path):
        if filename.endswith(".txt"):
            file_path_text = os.path.join(text_folder_path, filename)

        url_id = filename.split(".")[0]
        url = url_dict[url_id]

        content = read_text_content(file_path_text)
        cleaned_text = clean_text(content, custom_stopwords)

        positive_negative_folder = "MasterDictionary"
        positive_negative_dict = positive_negative_function(positive_negative_folder)

        positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(cleaned_text,
                                                                                                        positive_negative_dict)

        (
            avg_sentence_length, percentage_complex_words, fog_index,
            avg_words_per_sentence, count_complex_words, word_count,
            syllables_per_word, count_personal_pronouns, avg_word_length
        ) = calculate_readability_scores(cleaned_text)

        data_dict = {
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': positive_score,
            'NEGATIVE SCORE': negative_score,
            'POLARITY SCORE': round(polarity_score, 3),
            'SUBJECTIVITY SCORE': round(subjectivity_score, 3),
            'AVG SENTENCE LENGTH': round(avg_sentence_length, 3),
            'PERCENTAGE OF COMPLEX WORDS': round(percentage_complex_words, 3),
            'FOG INDEX': round(fog_index, 3),
            'AVG NUMBER OF WORDS PER SENTENCE': round(avg_words_per_sentence, 3),
            'COMPLEX WORD COUNT': count_complex_words,
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': round(syllables_per_word, 3),
            'PERSONAL PRONOUNS': count_personal_pronouns,
            'AVG WORD LENGTH': round(avg_word_length, 3)
        }
        df = df.append(data_dict, ignore_index=True)

    output_file = 'Output Data Structure.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Data exported to {output_file}")
