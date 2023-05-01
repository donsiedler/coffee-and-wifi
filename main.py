import csv
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired()])
    opening_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=[
        "☕️",
        "☕️☕️",
        "☕️☕️☕️",
        "☕️☕️☕️☕️",
        "☕️☕️☕️☕️☕️",
    ], validators=[DataRequired()])
    wifi_strength = SelectField("Wifi Strength Rating", choices=[
        "✘",
        "💪",
        "💪💪",
        "💪💪💪",
        "💪💪💪💪",
        "💪💪💪💪💪",
    ], validators=[DataRequired()])
    power_sockets = SelectField("Power Socket Availability", choices=[
        "✘",
        "🔌",
        "🔌🔌",
        "🔌🔌🔌",
        "🔌🔌🔌🔌",
        "🔌🔌🔌🔌🔌",
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        name = form.data["cafe"]
        location = form.data["location"]
        opening_time = form.data["opening_time"]
        closing_time = form.data["closing_time"]
        coffee_rating = form.data["coffee_rating"]
        wifi_strength = form.data["wifi_strength"]
        power_sockets = form.data["power_sockets"]

        with open("cafe-data.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow((name, location, opening_time, closing_time, coffee_rating, wifi_strength, power_sockets))
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
