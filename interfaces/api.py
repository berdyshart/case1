from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from application.use_cases import analyze_batch, analyze_text
from domain.types import Analysis_Result

MAX_TEXT_LENGTH = 100_000
MAX_BATCH_SIZE = 100

app = FastAPI(title='Text Analysis API')

class Analysis_Request(BaseModel):
  text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)

  @field_validator('text')
  @classmethod
  def validateText(cls, text: str) -> str:
    # Проверяет, что текст содержит непробельные символы.
    if not text.strip():
      raise ValueError('Текст не должен быть пустым')
    return text

class Batch_Request(BaseModel):
  texts: list[str] = Field(min_length=1, max_length=MAX_BATCH_SIZE)

  @field_validator('texts')
  @classmethod
  def validateTexts(cls, texts: list[str]) -> list[str]:
    # Проверяет содержимое и длину каждого текста в списке.
    for text in texts:
      if not text.strip():
        raise ValueError('Текст не должен быть пустым')
      if len(text) > MAX_TEXT_LENGTH:
        raise ValueError('Слишком длинный текст')

    return texts

class Text_Stats_Response(BaseModel):
  sentenceCount: int
  wordCount: int
  syllableCount: int
  avgSentenceLength: float
  avgWordSyllables: float

class Analysis_Response(BaseModel):
  language: str
  fleschIndex: float
  fleschKincaid: float
  interpretation: str
  polarity: str
  subjectivity: float
  lexicalDiversity: float
  rareWordDensity: float
  stats: Text_Stats_Response

def toAnalysisResponse(result: Analysis_Result) -> Analysis_Response:
  # Преобразует внутренний результат анализа в модель ответа API.
  return Analysis_Response(
    language=result.language.name,
    fleschIndex=result.fleschIndex,
    fleschKincaid=result.fleschKincaid,
    interpretation=result.interpretation,
    polarity=result.polarity.value,
    subjectivity=result.subjectivity,
    lexicalDiversity=result.lexicalDiversity,
    rareWordDensity=result.rareWordDensity,
    stats=Text_Stats_Response(
      sentenceCount=result.stats.sentenceCount,
      wordCount=result.stats.wordCount,
      syllableCount=result.stats.syllableCount,
      avgSentenceLength=result.stats.avgSentenceLength,
      avgWordSyllables=result.stats.avgWordSyllables
    )
  )

@app.post('/analyze', response_model=Analysis_Response)
def analyzeEndpoint(request: Analysis_Request) -> Analysis_Response:
  # Обрабатывает синхронный запрос на анализ одного текста.
  try:
    result = analyze_text(request.text)
    return toAnalysisResponse(result)
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )

@app.post('/analyze-batch', response_model=list[Analysis_Response])
def analyzeBatchEndpoint(request: Batch_Request) -> list[Analysis_Response]:
  # Обрабатывает синхронный запрос на анализ списка текстов.
  try:
    results = analyze_batch(request.texts)
    return [toAnalysisResponse(result) for result in results]
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )
