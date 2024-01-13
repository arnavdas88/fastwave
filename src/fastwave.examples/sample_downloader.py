from threading import Event

import httpx
from h2o_wave import Q, ui

# FaseAPI
from fastapi import FastAPI

from fastwave import wave, wave_collector

# FastAPI boilerplate.
app = FastAPI()

async def download_file(q: Q):
    # Create a tmp file to store the downloaded contents.
    with open('my_download', 'wb') as tmp_file:
        # Random URL to download a 100MB file.
        url = 'https://ash-speed.hetzner.com/1GB.bin'
        # Get async HTTP client.
        async with httpx.AsyncClient() as client:
            # Stream the response to get periodic download updates.
            async with client.stream('GET', url) as response:
                total = int(response.headers['Content-Length'])
                # Go over received chunks and write them to the file as needed.
                async for chunk in response.aiter_bytes():
                    # Check if cancelled.
                    if q.client.event.is_set():
                        q.page['meta'].dialog.items[0].progress.caption = 'Cancelled'
                        q.page['meta'].dialog.closable = True
                        return 
                    # Write received bytes to a tmp file on disk.
                    tmp_file.write(chunk)
                    # Update the Wave UI.
                    progress_val = response.num_bytes_downloaded / total
                    q.page['meta'].dialog.items[0].progress.value = progress_val
                    await q.page.save()
    await show_notification(q)

async def show_notification(q: Q):
    q.page['meta'].dialog = None
    q.page['meta'].notification_bar = ui.notification_bar(
        name='success_notification',
        text='Job done!',
        type='success',
        events=['dismissed']
    )
    await q.page.save()

@app.get('/toolbar/')
@wave
async def serve(q: Q):
    # Unimportant, draw initial UI.
    if not q.client.initialized:
        q.page['meta'] = ui.meta_card(box='')
        q.page['form'] = ui.form_card(box='1 1 2 1', items=[
            ui.button(name='download_file', label='Download file'),
        ])
        q.client.initialized = True
    
    # Handle start job button click.
    if q.args.download_file:
        q.page['meta'].dialog = ui.dialog(title='Download file', blocking=True, items=[
            ui.progress(label='Progress', value=0),
            ui.button(name='cancel', label='Cancel'),
        ])

        q.client.event = Event()
        await download_file(q)

    if q.args.cancel:
        q.client.event.set()
    
    # Unimportant, just handle notification dismissal.
    if q.events.success_notification and q.events.success_notification.dismissed:
        q.page['meta'].notification_bar = None

    await q.page.save()

wave_collector(app)