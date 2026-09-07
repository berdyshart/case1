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

