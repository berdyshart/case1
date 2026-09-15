from dataclasses import asdict
import json
import click
from application.use_cases import analyzeBatch, analyzeText
from domain.types import Analysis_Result


def analysisResultToDict(result: Analysis_Result) -> dict:
  # Преобразует результат анализа в словарь для вывода в JSON.
  resultData = asdict(result)
  resultData['language'] = result.language.name
  resultData['polarity'] = result.polarity.value
  return resultData

# Превращает функцию в основную группу команд.
# Нужна, чтобы можно было добавлять разные команды.
@click.group()
def cli():
  # Создаёт основную группу команд CLI.
  pass

@cli.command()
# Декоратор, который добавляет к команде параметр --text.
@click.option('--text', help='Текст для анализа')
@click.option(
  '--file', 'inputFile', type=click.File('r', encoding='utf-8'),
  help='Файл с одним текстом'
)
@click.option(
  '--batch-file', 'batchFile', type=click.File('r', encoding='utf-8'),
  help='JSON-файл со списком текстов'
)
def analyze(text, inputFile, batchFile):
  # Анализирует текст из выбранного пользователем источника.
  sources = sum(1 for el in [text, inputFile, batchFile] if el is not None)

  if sources != 1:
    raise click.UsageError('Укажите ровно один параметр: --text, --file или --batch-file.')

  if text is not None:
    result = analyzeText(text)
    outputData = analysisResultToDict(result)
    # Преобразуем словарь в строку формата JSON.
    outputJSON = json.dumps(outputData, ensure_ascii=False, indent=2)
    click.echo(outputJSON)

  elif inputFile is not None:
    textFromFile = inputFile.read()
    result = analyzeText(textFromFile)
    outputData = analysisResultToDict(result)
    outputJSON = json.dumps(outputData, ensure_ascii=False, indent=2)
    click.echo(outputJSON)

  elif batchFile is not None:
    # Преобразует данные из формата JSON в объекты Python.
    texts = json.load(batchFile)

    if not isinstance(texts, list) or not all(isinstance(text, str) for text in texts):
      raise click.UsageError('Пакетный файл должен содержать JSON-массив строк.')

    results = analyzeBatch(texts)
    outputData = [analysisResultToDict(res) for res in results]
    outputJSON = json.dumps(outputData, ensure_ascii=False, indent=2)

    click.echo(outputJSON)


if __name__ == '__main__':
  cli()
