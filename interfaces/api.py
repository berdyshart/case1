from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from application.use_cases import analyzeBatch, analyzeText
from domain.types import AnalysisResult

MAX_TEXT_LENGTH = 100_000
MAX_BATCH_SIZE = 100

WEB_PAGE_PATH = Path(__file__).parent / 'web' / 'index.html'

app = FastAPI(title='Text Analysis API')


@app.get('/', include_in_schema=False)
def webPage() -> FileResponse:
  # Возвращает веб-страницу для тестирования API.
  return FileResponse(WEB_PAGE_PATH)


class AnalysisRequest(BaseModel):
  text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)

  @field_validator('text')
  @classmethod
  def validateText(cls, text: str) -> str:
    # Проверяет, что текст содержит непробельные символы.
    if not text.strip():
      raise ValueError('Текст не должен быть пустым')
    return text


class BatchRequest(BaseModel):
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


class TextStatsResponse(BaseModel):
  sentenceCount: int
  wordCount: int
  syllableCount: int
  avgSentenceLength: float
  avgWordSyllables: float


class AnalysisResponse(BaseModel):
  language: str
  fleschIndex: float
  fleschKincaid: float
  interpretation: str
  polarity: str
  subjectivity: float
  lexicalDiversity: float
  rareWordDensity: float
  stats: TextStatsResponse


def toAnalysisResponse(result: AnalysisResult) -> AnalysisResponse:
  # Преобразует внутренний результат анализа в модель ответа API.
  return AnalysisResponse(
    language=result.language.name,
    fleschIndex=result.fleschIndex,
    fleschKincaid=result.fleschKincaid,
    interpretation=result.interpretation,
    polarity=result.polarity.value,
    subjectivity=result.subjectivity,
    lexicalDiversity=result.lexicalDiversity,
    rareWordDensity=result.rareWordDensity,
    stats=TextStatsResponse(
      sentenceCount=result.stats.sentenceCount,
      wordCount=result.stats.wordCount,
      syllableCount=result.stats.syllableCount,
      avgSentenceLength=result.stats.avgSentenceLength,
      avgWordSyllables=result.stats.avgWordSyllables
    )
  )


@app.post('/analyze', response_model=AnalysisResponse)
def analyzeEndpoint(request: AnalysisRequest) -> AnalysisResponse:
  # Обрабатывает синхронный запрос на анализ одного текста.
  try:
    result = analyzeText(request.text)
    return toAnalysisResponse(result)
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )


@app.post('/analyze-batch', response_model=list[AnalysisResponse])
def analyzeBatchEndpoint(request: BatchRequest) -> list[AnalysisResponse]:
  # Обрабатывает синхронный запрос на анализ списка текстов.
  try:
    results = analyzeBatch(request.texts)
    return [toAnalysisResponse(result) for result in results]
  except ValueError as e:
    raise HTTPException(
      status_code=400,
      detail=str(e)
    )
