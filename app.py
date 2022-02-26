#!/usr/bin/env python3

try:
    from flask import Flask, request, render_template
except:
    print(
        "Can not import flask, try pip3 install flask or consult your package manager"
    )

import argparse
import json
import threading
import sys
from tuner import Tuner
from rs232 import RS232Handler


app = Flask(
    __name__, static_url_path="", static_folder="html", template_folder="templates"
)


@app.route("/api/v1.0/status")
def status():
    status = {}
    tuner.set_data(tty.rxdata)
    status["frequency"] = tuner.get_frequency()
    status["port"] = tuner.get_antenna()
    status["capacitance"] = tuner.get_capacitance()
    status["inductance"] = tuner.get_inductance()
    status["power"] = float(tuner.get_power())
    status["vswr"] = float(tuner.get_vswr())
    status["auto"] = tuner.is_auto()
    status["bypass"] = tuner.is_bypass()
    js = json.dumps(status)
    return js


@app.route("/api/v1.0/set")
def set():

    port = request.args.get("port")
    mode = request.args.get("mode")
    delta = False
    if port is None:
        port = 0
    else:
        port = int(port)
    if port > 0 and port < 4:
        tty.serial_tx_handler(tuner.set_antenna(int(port)))
        delta = True
    if mode is not None:
        if mode == "bypass":
            delta = True
            tty.serial_tx_handler(tuner.set_bypass())
        elif mode == "auto":
            tty.serial_tx_handler(tuner.set_auto())
    if delta:
        return "{'result': 'ok'}"
    else:
        return {"result": "fail"}


@app.route("/")
def start():
    host_str = f"{args.url_host}:{args.port}"
    return render_template("index.template", host=host_str)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url_host",
        action="store",
        help="host or IP used to reach this app",
        dest="url_host",
        default=None,
    )
    parser.add_argument(
        "--port",
        action="store",
        help="Listening Port Number",
        dest="port",
        default=10000,
    )
    parser.add_argument(
        "--tty",
        action="store",
        help="TTY or COM port",
        dest="ttyport",
        default="/dev/ttyUSB0",
    )

    args = parser.parse_args()
    tty = RS232Handler()
    sp = tty.open_serial(args.ttyport)
    if sp != None:
        th = threading.Thread(name="serial_rx_handler", target=tty.serial_rx_handler)
        th.start()

    tuner = Tuner(tty.rxdata)
    app.run(host="0.0.0.0", port=args.port)
