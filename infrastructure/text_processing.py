from string import punctuation

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