# Case-study #2
# Developers:  Ufilin A., Zubareva A., Berdyshev A., Chepeleva M.

import uvicorn

if __name__ == '__main__':
  uvicorn.run(
    'interfaces.api:app',
    host='0.0.0.0',
    port=8000,
    reload=False
  )
