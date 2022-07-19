import random
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time


def update_data(seconds, file_name, div_id):
    with app.app_context():
        while True:
            time.sleep(seconds)
            turbo.push(turbo.replace(
                render_template(file_name), div_id))


def update_current_speed():
    update_data(10, 'current_speed.html', 'current_speed')


def update_current_station():
    update_data(180, 'current_station.html', 'current_station')


app = Flask(__name__)

turbo = Turbo(app)


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_current_speed).start()
    threading.Thread(target=update_current_station).start()


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_current_speed():
    current_speed = int(random.random() * 180 * 10) / 10
    return {'current_speed': current_speed}


stations = ['Adampol', 'Babica Kolonia', 'Cedrowskie Pole', 'Daniel', 'Dańdówka', 'Elbląg Miasto', 'Elektrownia Łagisza', 'Fabianów', 'Feliksowo', 'Gajówka',
            'Jabłonna Łęczycka', 'Kaczynos', 'Laliki', 'Machnacz Wschód', 'Nadolice Małe', 'Pakosław', 'Sadowiec', 'Tarczyn Wąskotorowy', 'Walim Dolny', 'Wałbrzych Fabryczny']


@app.context_processor
def inject_current_station():
    current_station = random.choice(stations)
    return {'current_station': current_station}


if __name__ == "__main__":
    app.run()
