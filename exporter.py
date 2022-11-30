import re

import revpimodio2
from prometheus_client import start_http_server, Gauge

rpi = revpimodio2.RevPiModIO(autorefresh=True, monitoring=True)
rpi.handlesignalend()

gauges = dict()


def evf(name):
    def event_handler(io_name: str, io_value):
        gauges[name].set(io_value)

    return event_handler


for device in rpi.device:
    for io in device:
        if not io.export:
            continue

        print(device.position, device.name)

        name = f"{device.name}_{device.position}_{io.name}"
        name = re.sub(r"[^a-zA-Z0-9_:]*", "", name)

        gauges[name] = Gauge(name, io.bmk)
        io.reg_event(evf(name), prefire=True)


start_http_server(8000)

rpi.mainloop()
