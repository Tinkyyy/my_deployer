__author__ = "belgue_s"
__doc__ = "This service can retrieve information about the Docker containers on the host"

import flask
from flask import Flask, jsonify
import psutil
import cpuinfo
import shutil


def build_app() -> flask.app.Flask:
    """This function will return a Flask APP instance"""
    application = Flask("checker")
    application.debug = False

    return application


app: Flask = build_app()
app.config['JSON_SORT_KEYS'] = False


def get_cpu_information() -> dict:
    """This function retrieve every system information"""
    cores = {}
    for index, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores[f'Core {index}'] = f"{percentage}%"

    cpu = cpuinfo.get_cpu_info()
    total, used, free = shutil.disk_usage("/")

    data: dict = {
        'CPU': {
            'Brand': cpu['brand_raw'],
            'Arch': cpu['arch_string_raw'],
            'Advertised Speed': cpu['hz_advertised_friendly'],
            'Current Speed': cpu['hz_actual_friendly'],

            'Performances': {
                'Physical cores': psutil.cpu_count(logical=False),
                'Total cores:': psutil.cpu_count(logical=True),
                'Cores Usage': cores,
                'Total CPU Usage': f"{psutil.cpu_percent()}%",
            },
        },

        'Memory': {
            'Max Frequency:': f"{psutil.cpu_freq().max:.2f} Mhz",
            'Min Frequency:': f"{psutil.cpu_freq().min:.2f} Mhz",
            'Current Frequency': f"{psutil.cpu_freq().current:.2f}Mhz",
        },

        'Storage': {
            'Total': total // (2 ** 30),
            'Used': used // (2 ** 30),
            'Free': free // (2 ** 30)
        },
    }

    return data


@app.errorhandler(404)
def page_not_found(_):
    """404 route"""
    return flask.redirect("/api/system")


@app.route("/")
def starting_url():
    """Starting route"""
    return flask.redirect("/api/system")


@app.route('/api/system', methods=['GET'])
def system_route():
    """System route"""
    return jsonify(get_cpu_information()), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
