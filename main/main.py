from flask import Flask, render_template, request, session, redirect, url_for

from json_reader import JsonReader
from history import History

app = Flask(__name__)
reader = JsonReader
# f"http://api.weatherapi.com/v1/current.json?key&q=Brno"
api_key = "68870090a3624a80ba2104715242309"
base_url = f"http://api.weatherapi.com/v1/current.json"


reader = JsonReader(base_url, api_key)

history = History()
app.secret_key = "VerySecretKey123@!#"

@app.route("/", methods = ['POST', 'GET'])
def main_page(weather_data = reader.cityWeather("Moscow")):
    # Create main page from template. Pass data to this page.
    if 'city' in session:
        city = session['city']
    else:
        city = 'Moscow'


    if request.method == 'GET':

        try:
            weather_data = reader.cityWeather(city)
            temp, condition = reader.TempData()
            if 'current' not in weather_data:
                raise ValueError("Not Valid")
            history.addRecord(city + ": " + str(temp) + " °C - " + str(weather_data["current"]["condition"]["text"]))
        except Exception as e:
            return redirect(url_for('exception'))

    if request.method == 'POST':
        city = request.form['txt_city']
        session['city'] = city
        try:
             weather_data = reader.cityWeather(city)
             if 'current' not in weather_data:
                 raise ValueError("Not Valid")
        except Exception as e:
            session.pop('city', None)
            return redirect(url_for('exception'))

        condition = reader.TempData()

    return render_template('main.html', data=weather_data, Wcity=city, Wcond=condition)

@app.route("/history")
def history_page(history_data=None):
    if request.method == 'GET':
        history_data = history.getHistory()
    return render_template('history.html', data=history_data)

@app.route("/whenException")
def exception():
    session.pop('city', None)
    return render_template("ExceptionSite.html")

if __name__ == '__main__':
    app.run(debug=True)