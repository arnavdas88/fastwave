from fastapi import APIRouter, FastAPI
from h2o_wave import Q, ui

from fastwave import wave, wave_collector

app = FastAPI()
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/hello/", tags=["users"])
@wave
async def hello(q: Q):
    # The header shown on all the app's pages
    q.page["header"] = ui.header_card(
        box="1 1 5 1",
        title="Hello Wave",
        subtitle="Hello World example",
        icon="WavingHand",
        color="card",
    )

    # The main card of the app
    q.page["main"] = ui.form_card(
        box="1 2 5 4",
        items=[
            ui.text(content="The quick brown fox jumps over the lazy dog")
            for _ in range(10)
        ],
    )

    # Save the page
    await q.page.save()


app.include_router(router)
wave_collector(app)
