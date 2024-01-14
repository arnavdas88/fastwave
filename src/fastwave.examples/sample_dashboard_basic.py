# Core python packages
import base64
import os
import pathlib
import re

# Fake Data
from faker import Faker

# FaseAPI
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# H2O Wave
from h2o_wave import Q, data, ui
from synth import FakeCategoricalSeries

from fastwave import wave, wave_collector

# FastAPI boilerplate.
app = FastAPI()

# Fake Data
fake = Faker()

val = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
pc = [2, 2, 2, 3, 4, 4, 4, 6, 5, 6, 6, 7, 7, 10, 12, 11, 9, 7, 7, 7]


@app.get("/toolbar/")
@wave
async def toolbar(q: Q):
    q.page["meta"] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="l",
                # width='1200px',
                width="98vw",
                zones=[
                    ui.zone("header", size="76px"),
                    ui.zone(
                        "main",
                        size="calc(98vh - 152px)",
                        direction=ui.ZoneDirection.ROW,
                        zones=[
                            ui.zone("description", size="40%"),
                            ui.zone(
                                "rhs",
                                size="60%",
                                direction=ui.ZoneDirection.COLUMN,
                                zones=[
                                    ui.zone(
                                        "rtop",
                                        size="40%",
                                        direction=ui.ZoneDirection.ROW,
                                        zones=[
                                            ui.zone("rtop_l", size="50%"),
                                            ui.zone("rtop_r", size="50%"),
                                        ],
                                    ),
                                    ui.zone("rbottom", size="60%"),
                                ],
                            ),
                        ],
                    ),
                    ui.zone("footer", size="76px"),
                ],
            )
        ],
    )
    q.page["nav"] = ui.toolbar_card(
        box="header",
        items=[
            ui.command(
                name="new",
                label="New",
                icon="Add",
                items=[
                    ui.command(name="email", label="Email Message", icon="Mail"),
                    ui.command(
                        name="calendar", label="Calendar Event", icon="Calendar"
                    ),
                ],
            ),
            ui.command(name="upload", label="Upload", icon="Upload"),
            ui.command(name="share", label="Share", icon="Share"),
            ui.command(name="download", label="Download", icon="Download"),
        ],
        secondary_items=[
            ui.command(name="tile", caption="Grid View", icon="Tiles"),
            ui.command(name="info", caption="Info", icon="Info"),
        ],
        overflow_items=[
            ui.command(name="move", label="Move to...", icon="MoveToFolder"),
            ui.command(name="copy", label="Copy to...", icon="Copy"),
            ui.command(name="rename", label="Rename", icon="Edit"),
        ],
    )
    q.page["example"] = ui.article_card(
        box="description",
        title="Title",
        items=[
            ui.mini_buttons(
                [
                    ui.mini_button(name="like", label="4", icon="Heart"),
                    ui.mini_button(name="comment", label="2", icon="Blog"),
                    ui.mini_button(name="share", label="1", icon="Relationship"),
                ]
            )
        ],
        content=base64.b64decode(
            "RHVpcyBwb3J0dGl0b3IgdGluY2lkdW50IGp1c3RvIGFjIHNlbXBlci4gVmVzdGlidWx1bSBldCBtb2xlc3RpZSBsZWN0dXMuIFByb2luIHZlbCBlcm9zIGEgZXggY29uZGltZW50dW0gYWxpcXVhbS4KU2VkIGFjY3Vtc2FuIHRlbGx1cyBzaXQgYW1ldCBudWxsYSB1bGxhbWNvcnBlci4gU3VzcGVuZGlzc2UgYmliZW5kdW0gdHJpc3RpcXVlIHNlbSwgcXVpcyBsYWNpbmlhIGV4IHB1bHZpbmFyIHF1aXMuCk5hbSBlbGVtZW50dW0gYWNjdW1zYW4gcG9ydGEuIFNlZCBlZ2V0IGFsaXF1YW0gZWxpdCwgc2VkIGx1Y3R1cyBsb3JlbS4gTnVsbGEgZ3JhdmlkYSBtYWxlc3VhZGEgcHVydXMgZXUgZWxlaWZlbmQuCk1hZWNlbmFzIGluIGFudGUgaW50ZXJkdW0sIGhlbmRyZXJpdCB2ZWxpdCBhdCwgdGVtcHVzIGVyb3MuIE51bGxhbSBjb252YWxsaXMgdGVtcG9yIGxpYmVybyBhdCB2aXZlcnJhLgoKIyMgSGVhZGluZyAyCgpEdWlzIHBvcnR0aXRvciB0aW5jaWR1bnQganVzdG8gYWMgc2VtcGVyLiBWZXN0aWJ1bHVtIGV0IG1vbGVzdGllIGxlY3R1cy4gUHJvaW4gdmVsIGVyb3MgYSBleCBjb25kaW1lbnR1bSBhbGlxdWFtLgpTZWQgYWNjdW1zYW4gdGVsbHVzIHNpdCBhbWV0IG51bGxhIHVsbGFtY29ycGVyLiBTdXNwZW5kaXNzZSBiaWJlbmR1bSB0cmlzdGlxdWUgc2VtLCBxdWlzIGxhY2luaWEgZXggcHVsdmluYXIgcXVpcy4KTmFtIGVsZW1lbnR1bSBhY2N1bXNhbiBwb3J0YS4gU2VkIGVnZXQgYWxpcXVhbSBlbGl0LCBzZWQgbHVjdHVzIGxvcmVtLiBOdWxsYSBncmF2aWRhIG1hbGVzdWFkYSBwdXJ1cyBldSBlbGVpZmVuZC4KTWFlY2VuYXMgaW4gYW50ZSBpbnRlcmR1bSwgaGVuZHJlcml0IHZlbGl0IGF0LCB0ZW1wdXMgZXJvcy4gTnVsbGFtIGNvbnZhbGxpcyB0ZW1wb3IgbGliZXJvIGF0IHZpdmVycmEu"
        ).decode("utf-8"),
    )
    q.page["plot"] = ui.plot_card(
        box="rtop_l",
        title="Line, groups",
        animate=True,
        data=data(
            "month city temperature",
            24,
            rows=[
                ("Jan", "Tokyo", 7),
                ("Jan", "London", 3.9),
                ("Feb", "Tokyo", 6.9),
                ("Feb", "London", 4.2),
                ("Mar", "Tokyo", 9.5),
                ("Mar", "London", 5.7),
                ("Apr", "Tokyo", 14.5),
                ("Apr", "London", 8.5),
                ("May", "Tokyo", 18.4),
                ("May", "London", 11.9),
                ("Jun", "Tokyo", 21.5),
                ("Jun", "London", 15.2),
                ("Jul", "Tokyo", 25.2),
                ("Jul", "London", 17),
                ("Aug", "Tokyo", 26.5),
                ("Aug", "London", 16.6),
                ("Sep", "Tokyo", 23.3),
                ("Sep", "London", 14.2),
                ("Oct", "Tokyo", 18.3),
                ("Oct", "London", 10.3),
                ("Nov", "Tokyo", 13.9),
                ("Nov", "London", 6.6),
                ("Dec", "Tokyo", 9.6),
                ("Dec", "London", 4.8),
            ],
            pack=True,
        ),
        plot=ui.plot(
            [ui.mark(type="line", x="=month", y="=temperature", color="=city", y_min=0)]
        ),
    )
    q.page["stat"] = ui.wide_series_stat_card(
        box="rtop_r",
        title=fake.cryptocurrency_name(),
        value="=${{intl qux minimum_fraction_digits=2 maximum_fraction_digits=2}}",
        aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
        data=dict(qux=val[0], quux=pc[0] / 100),
        plot_category="foo",
        plot_type="interval",
        plot_value="qux",
        plot_color="$red",
        plot_data=data("foo qux", -1 * len(val), rows=list(zip(val, pc)), pack=True),
        plot_zero_value=0,
    )
    q.page["table"] = ui.form_card(
        box="rbottom",
        items=[
            ui.table(
                name="table",
                columns=[
                    ui.table_column(
                        name="text", label="Table multiple selection", min_width="300px"
                    )
                ],
                rows=[
                    ui.table_row(name="row1", cells=["Row 1"]),
                    ui.table_row(name="row2", cells=["Row 2"]),
                    ui.table_row(name="row3", cells=["Row 3"]),
                    ui.table_row(name="row4", cells=["Row 4"]),
                    ui.table_row(name="row5", cells=["Row 5"]),
                ],
                values=["row2", "row4"],
            ),
            ui.button(name="show_inputs", label="Submit", primary=True),
        ],
    )

    await q.page.save()


wave_collector(app)
