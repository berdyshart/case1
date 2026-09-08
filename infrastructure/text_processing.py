from string import punctuation
from domain.types import Text_Stats
from domain.interfaces import SyllableCounter

def isEmptyText(text: str) -> bool:
  """
  Function to check if the incoming text is entirely empty
  """
  return not text or not text.strip()

def isEmptyWord(word: str) -> bool:
    """
    Function to check if a specific word is empty
    """
    return not word or not word.strip(punctuation + "«»—…“”")

def splitSentences(text: str) -> list[str]:
    """
    Function to split text into sentences
    """
    if isEmptyText(text):
        return []
    
    cleaned_text = text.replace('!', '.').replace('?', '.')
    sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
    
    return sentences if sentences else [text.strip()]

def countSentences(text: str) -> int:
    """
    Function to return the total number of sentences in the text
    """
    return len(splitSentences(text))

def splitWords(text: str) -> list[str]:
    """
    Function to split text into cleaned words without punctuation
    """
    if isEmptyText(text):
        return []
        
    text_clean = text.lower()

    to_remove = (punctuation + "«»—…“”").replace("'", "").replace("-", "")
    for char in to_remove:
        text_clean = text_clean.replace(char, " ")
        
    return [w for w in text_clean.split() if w and not isEmptyWord(w)]

def countWords(text: str) -> int:
    """
    Function to return the total number of words in the text
    """
    return len(splitWords(text))

def avgSentenceLength(text: str) -> float:
    """
    Function to calculate the average sentence length (in words)
    """
    sentences_count = countSentences(text)
    words_count = countWords(text)
    
    if sentences_count == 0:
        return 0.0
    return words_count / sentences_count

def avgWordLengthInChars(text: str) -> float:
    """
    Function to calculate the average word length (in characters)
    """
    words = splitWords(text)
    if not words:
        return 0.0
    
    total_chars = sum(len(w) for w in words)
    return total_chars / len(words)

def computeStats(text: str, syllableCounter: SyllableCounter) -> Text_Stats:
    """
    Function to compute text stats
    """
    words = splitWords(text)
    sentences = splitSentences(text)
    
    w_count = len(words)
    s_count = len(sentences)
    
    total_syllables = sum(syllableCounter(text)) if w_count > 0 else 0
    avg_sent_len = (w_count / s_count) if s_count > 0 else 0.0
    avg_word_syl = (total_syllables / w_count) if w_count > 0 else 0.0
    
    return Text_Stats(
        sentenceCount=s_count,
        wordCount=w_count,
        syllableCount=total_syllables,
        avgSentenceLength=avg_sent_len,
        avgWordSyllables=avg_word_syl
    )