# FastWave

<img src="imgs/FastWave - Cover.png" alt="FastWave logo">

### Build UIs faster, with h2o-wave and fastapi.

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

H2O Wave is a software stack for building beautiful, low-latency, realtime, browser-based applications and dashboards entirely in Python/R without using HTML, Javascript, or CSS.

H2O Wave excels at capturing information from multiple sources and broadcasting them live over the web, letting you build and deploy realtime analytics with dramatically less effort.

__FastWave, bridges the gap, bringing H2O Wave support to the FastAPI world.__

### Todo List: Planning the next in Wave

- [x] Implement decorator-based setup
- [x] Provide illustrative examples
- [x] Enable accessing path parameters when using FastWave
- [ ] Enable accessing query parameters when using FastWave
- [ ] Enable accessing request parameters when using FastWave
- [ ] Documentation
- [ ] Unit Tests
- [ ] Dockerized Enviornment

### Installation : Ride the Wave Locally
Install the FastWave experience locally with a simple command:
```sh
$ pip install git+https://github.com/arnavdas88/fastwave.git
```

### Usage : Catch the Wave in Your Code
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

Upgrade your code coolness:

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

### Structure : The FastWave Blueprint

A practical FastWave implementation looks like a work of art, with FastAPI and Wave segments elegantly intertwined:

<img src="imgs/FastWave - Code FastAPI Wave.png" alt="FastWave FastAPI & Wave Segments" width="63%">

The code schema follows a logical and clean structure:

<img src="imgs/FastWave - Code Example.png" alt="FastWave Code Schema">

### How FastWave Works: Behind the Scenes
Wondering what's happening behind the curtain? FastWave orchestrates the magic:

The @wave decorator is the secret sauce. It registers a separate but unique rendering handle to FastAPI, capturing the essence of H2O Wave. It also registers the original H2O Wave handle in a global registry.

When wave_collector is called at the end, it unleashes the magic. It registers all the H2O Wave handles from the global registry to FastAPI, bringing the UIs to life.

<img src="imgs/FastWave - Working.png" alt="How FastWave Works?">

### Example : A Fast Wave

```python
# H2O Imports
from h2o_lightwave import ui, data, Q
# FastAPI Imports
from fastapi import FastAPI, WebSocket
# FastWave
from fastwave import wave, wave_collector

# Initializing the FastAPI server
app = FastAPI()

# Define a global variable `bean_count` to
# be rendered
global bean_count
bean_count = 0

@app.get("/{name}")
@wave
async def show_cyan_dashboard(name:str, sock:WebSocket, q: Q):
    global bean_count
    # Was the 'increment' button clicked?
    if q.args.increment:
        bean_count += 1

    # Display a form on the page
    q.page['beans'] = ui.form_card(
        box='1 1 5 2',
        items=[
            ui.text_xl(f'{name} Beans!'),
            ui.button(name='increment', label=f'{name} has {bean_count} beans'),
        ],
    )
    # Save the page
    await q.page.save()

# Make sure to collect the `WaveFunc` using
# this command. This will register the original
# ui renderer
wave_collector(app)
```

<img src="imgs/FastWave - Minimalist Example Render.png" alt="FastWave Minimalist Render Example">

### Contributing : Dive In

We welcome contributions from the community! To contribute to FastWave, follow the guidelines in the [Contribution](CONTRIBUTING.md) Guide. Your contributions help make FastWave even more awesome! 🚀

### License : FastWave is All Yours
FastWave is licensed under the MIT License, giving you the freedom to ride the code wave however you like. 🏄‍♂️