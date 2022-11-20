from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('about.html', title = 'Долбаёб введи имя', text = 'Долбаёб введи имя')

@app.route('/valek')
def about():
    return render_template('about.html', name = 'Ваше имя : Алкаш вася', title = "Алкаш Вася", text = db.discount('Алкаш Вася')[0]['Цена со скидкой'])


if __name__ == "__main__":
    app.run(debug=True)