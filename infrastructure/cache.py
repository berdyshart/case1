import json

CACHE_PREFIX = 'text-analysis:'
CACHE_TTL_SECONDS = 3600

def getCachedResult(redisClient, text: str) -> dict | None:
  # Получает сохранённый результат анализа из Redis.
  cacheKey = CACHE_PREFIX + text
  cachedResult = redisClient.get(cacheKey)
  if cachedResult is None:
    return None

  return json.loads(cachedResult)

def setCachedResult(redisClient, text: str, result: dict) -> None:
  # Сохраняет результат анализа в Redis на один час.
  cacheKey = CACHE_PREFIX + text
  serializedResult = json.dumps(result, ensure_ascii=False)

  redisClient.setex(cacheKey, CACHE_TTL_SECONDS, serializedResult)


