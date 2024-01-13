import time, datetime
from h2o_wave import site, ui, Q, main, app
from h2o_lightwave import data
import psutil
import speedtest # speedtest-cli

from fastapi import FastAPI
from fastwave import wave, wave_collector

app = FastAPI()

def bytes_to_mb(b):
    b /= 8 # b is in bits, not byte
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return int(b / MB)

@app.get("/")
@wave
async def show_cyan_dashboard(q: Q):

    cpu_card = q.page.add('cpu_stats', ui.small_series_stat_card(
        box='1 1 2 2',
        title='CPU',
        value='={{usage}}%',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$red',
    ))

    core_card = q.page.add('cpu_cores', ui.small_series_stat_card(
        box='3 1 2 2',
        title='CPU Cores',
        value='={{usage}}',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$purple',
    ))

    mem_card = q.page.add('mem_stats', ui.small_series_stat_card(
        box='1 3 2 2',
        title='Memory',
        value='={{usage}}%',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$blue',
    ))

    battery_card = q.page.add('battery_stats', ui.small_series_stat_card(
        box='3 3 2 2',
        title='Battery',
        value='={{usage}} %',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$pink',
    ))

    temp_card = q.page.add('temp_stats', ui.small_series_stat_card(
        box='3 5 2 2',
        title='Heat',
        value='={{usage}} °C',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$yellow',
    ))

    boot_card = q.page.add('boot_stats', ui.small_series_stat_card(
        box='3 7 2 2',
        title='Last Boot',
        value='={{usage}}',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$cyan',
    ))

    speed_test = speedtest.Speedtest(secure=True)
    download_speed = bytes_to_mb(speed_test.download())

    download_card = q.page.add('download_speed', ui.small_series_stat_card(
        box='1 5 2 2',
        title='Download speed',
        value=str(download_speed) + " MB",
        data=dict(download_speed=0.0),
        plot_data=data('tick speed', -15),
        plot_category='tick',
        plot_value='speed',
        plot_zero_value=0,
        plot_color='$orange',

    ))

    upload_speed = bytes_to_mb(speed_test.upload())
    upload_card = q.page.add('upload_speed', ui.small_series_stat_card(
        box='1 7 2 2',
        title='Upload speed',
        value=str(upload_speed) + " MB",
        data=dict(upload_speed=0.0),
        plot_data=data('tick speed', -15),
        plot_category='tick',
        plot_value='speed',
        plot_zero_value=0,
        plot_color='$green',

    ))

    tick = 0
    while True:
        tick += 1

        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_card.data.usage = cpu_usage
        cpu_card.plot_data[-1] = [str(tick), cpu_usage]

        mem_usage = psutil.virtual_memory().percent
        mem_card.data.usage = mem_usage
        mem_card.plot_data[-1] = [str(tick), mem_usage]

        cpu_count = psutil.cpu_count()
        core_card.data.usage = cpu_count
        core_card.plot_data[-1] = [str(tick), cpu_count]

        battery_values = psutil.sensors_battery()
        if battery_values:
            battery_level = f"{battery_values.percent:.2f}"
            battery_card.data.usage = battery_level
            battery_card.plot_data[-1] = [str(tick), battery_values.percent]
        else:
            battery_level = f"{0.0:.2f}"
            battery_card.data.usage = battery_level
            battery_card.plot_data[-1] = [str(tick), 0.0]

        temperature_values = psutil.sensors_temperatures()
        # current_temp =temperature_values['k10temp'][0].current
        current_temp = list(temperature_values.values())[0][0].current
        temp_card.data.usage = current_temp
        temp_card.plot_data[-1] = [str(tick), current_temp]

        boot_time = psutil.boot_time()
        bt = (datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"))
        boot_card.data.usage = bt
        boot_card.plot_data[-1] = [str(tick), boot_time]
        
        if tick % 10 == 0:
            download_speed = bytes_to_mb(speed_test.download())
            download_card.data.usage = str(download_speed)
            download_card.value = str(download_speed) + " MB/s"
            download_card.plot_data[-1] = [str(tick), str(download_speed)]
            upload_speed = bytes_to_mb(speed_test.upload())
            upload_card.data.usage = upload_speed
            upload_card.plot_data[-1] = [str(tick), upload_speed]

        await q.page.save()
        time.sleep(1)

wave_collector(app)