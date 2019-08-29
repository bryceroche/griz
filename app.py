import os
import aiohttp
import asyncio
import uvicorn
import logging
from fastai import *
from fastai.imports import *
from fastai.text import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

logging.basicConfig(format='%(message)s', level=logging.INFO)


export_file_url = 'https://drive.google.com/uc?export=download&id=1GQXmx-yd_z-32wWLGC6zQg_QB_FZJWc0'
export_file_name = 'modelabc70pct.pkl'
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.add_middleware(SessionMiddleware, secret_key="oiuqrtyhkjasfjslsjr")
app.mount('/static', StaticFiles(directory='app/static'))
templates = Jinja2Templates(directory='app/view')


# Check if user logged in
def is_logged_in(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      flash('Unauthorized, Please login', 'danger')
      return redirect(url_for('login'))
  return wrap

async def download_file(url, dest):
  if dest.exists(): return
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      data = await response.read()
      with open(dest, 'wb') as f:
        f.write(data)

async def setup_learner():
  await download_file(export_file_url, path / export_file_name)
  try:
    return load_learner(path, export_file_name)
  except RuntimeError as e:
    if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
      print(e)
      message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
      raise RuntimeError(message)
    else:
      raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
async def homepage(request):
  request.session['logged_in'] = True
  template = "index.html"
  context = {"request": request}
  return templates.TemplateResponse(template, context)

@app.route('/google938d1c782631145d.html')
def google_verify(request):
  template = 'google938d1c782631145d.html'
  context = {"request": request}
  return templates.TemplateResponse(template, context)

@app.route('/predict')
async def predict(request):
  template = 'predict.html'
  context = {"request": request}
  return templates.TemplateResponse(template, context)

@app.route('/analyze', methods=['POST'])
async def analyze(request):
  form_data = await request.form()
  TEXT = form_data['thevalue']
  N_WORDS = 40
  N_SENTENCES = 1
  printtext = ("\n".join(model.predict(TEXT, N_WORDS, temperature=0.75) for _ in range(N_SENTENCES)))
  printtext2 = ("\n".join(model.predict(TEXT, N_WORDS, temperature=0.75) for _ in range(N_SENTENCES)))
  return JSONResponse({'result1': str(printtext), 'result2': str(printtext2)})

if __name__ == '__main__':
  uvicorn.run(app=app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
