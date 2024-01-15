# FastWave

<img src="imgs/FastWave - Cover.png" alt="FastWave logo">

### Build UIs faster, with h2o-wave and fastapi.

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

H2O Wave is a software stack for building beautiful, low-latency, realtime, browser-based applications and dashboards entirely in Python/R without using HTML, Javascript, or CSS.

H2O Wave excels at capturing information from multiple sources and broadcasting them live over the web, letting you build and deploy realtime analytics with dramatically less effort.

Combining the best, FastWave provides H2O Wave support in FastAPI.

### Installation
Install locally using 
```sh
$ pip install git+https://github.com/arnavdas88/fastwave.git
```

### Usage
Starting with the very basic fastapi server,

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    return {"description": "The Index Page!!!"}

@app.get("/hello")
async def hello():
    return {"description": "The Hello World Page!!!"}
```

Can be modified as ,

```python
from fastapi import FastAPI, WebSocket
from h2o_wave import Q
from fastwave import wave, wave_collector

app = FastAPI()

@app.get("/")
async def index():
    return {"description": "The Index Page!!!"}

@app.get("/hello")
async def hello():
    return {"description": "The Hello World Page!!!"}

@app.get("/ui_1/{title}")
@wave
async def ui_1(title: str, sock: WebSocket, q: Q):
    # ... H2O Wave UI Code ...
    await q.page.save()


@app.get("/ui_2")
@wave
async def ui_2(q: Q):
    # ... H2O Wave UI Code ...
    await q.page.save()

wave_collector(app)
```

And it will render the `ui_1` and `ui_2` in the respective endpoint.

### Structure


A practical working implementation of FastWave, looks like,
<img src="imgs/FastWave - Code FastAPI Wave.png" alt="FastWave FastAPI & Wave Segments">

The Schema follows,
<img src="imgs/FastWave - Code Example.png" alt="FastWave Code Schema">

How FastWave works?
<img src="imgs/FastWave - Working.png" alt="How FastWave Works?">

### License
FastWave is licensed under the MIT License.