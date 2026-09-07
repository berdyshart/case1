import string

def isEmptyText(text: str) -> bool:
  """
  Function to check if the incoming text is entirely empty
  """
  return not text or not text.strip()

def isEmptyWord(word: str) -> bool:
    """
    Function to check if a specific word is empty
    """
    return not word or not word.strip(string.punctuation + "«»—…“”")