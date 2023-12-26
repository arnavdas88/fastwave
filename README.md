# FastWave
Build UIs faster, with h2o-wave and fastapi.

# Installation

Install locally using 
```sh
$ pip3 install -e .
```

# Usage
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

We start with importing the necessary modules from h2o wave and fastwave,
```diff
+ from h2o_wave import Q, ui
from fastapi import FastAPI
+ from faker import Faker
+ from fastwave import H2O_WaveUI, HandleAsync

app = FastAPI()

@app.get("/")
async def index():
    return {"description": "The Index Page!!!"}

@app.get("/hello")
async def hello():
    return {"description": "The Hello World Page!!!"}
```

Now we can build our wave ui inside any of the routed `async` function. 
```diff
from h2o_wave import Q, ui
from fastapi import FastAPI
from faker import Faker
from fastwave import H2O_WaveUI, HandleAsync

app = FastAPI()

+ fake = Faker()

@app.get("/")
async def index():
    return {"description": "The Index Page!!!"}

@app.get("/hello")
- async def hello():
-     return {"description": "The Hello World Page!!!"}
+ async def hello(q:Q):
+     # The header shown on all the app's pages
+     q.page['header'] = ui.header_card(
+         box='1 1 5 1', title='Hello Wave',
+         subtitle='Hello World example', 
+         icon='WavingHand', color='card'
+     )
+ 
+     # The main card of the app
+     q.page['main'] = ui.form_card(
+         box='1 2 5 4',
+         items=[
+             ui.text(content=fake.paragraph(nb_sentences=5, variable_nb_sentences=False)) for _ in range(10)
+         ]
+     )
+ 
+     # Save the page
+     await q.page.save()
```

Now we can add our `@H2O_WaveUI` decorator to represent that the async function `hello()` will return a `HandleAsync` from H2O Wave, instead of a regular PyDantic class.
```diff
from h2o_wave import Q, ui
from fastapi import FastAPI
from faker import Faker
from fastwave import H2O_WaveUI, HandleAsync

app = FastAPI()

fake = Faker()

@app.get("/")
async def index():
    return {"description": "The Index Page!!!"}

@app.get("/hello")
+ @H2O_WaveUI(app, name="hello")
async def hello(q:Q):
    # The header shown on all the app's pages
    q.page['header'] = ui.header_card(
        box='1 1 5 1', title='Hello Wave',
        subtitle='Hello World example', 
        icon='WavingHand', color='card'
    )

    # The main card of the app
    q.page['main'] = ui.form_card(
        box='1 2 5 4',
        items=[
            ui.text(content=fake.paragraph(nb_sentences=5, variable_nb_sentences=False)) for _ in range(10)
        ]
    )

    # Save the page
    await q.page.save()
```

