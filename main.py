from nltk.corpus import cmudict, stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


from nltk.corpus import cmudict

# Load CMU Pronouncing Dictionary once
cmu_dict = cmudict.dict()

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



cleaned_text = """We have seen a huge development, developed and dependence of people on technology in recent years."""
words = word_tokenize(cleaned_text)
word_count = len(words)
complex_words = [word for word in words if syllable_count(word) > 2]
syllables_per_word = sum(syllable_count(word) for word in words) / word_count

print(complex_words)
print(syllables_per_word)