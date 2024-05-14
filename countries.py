import pandas as pd
import random
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', template_folder='templates')

# Read the CSV file into a DataFrame
df = pd.read_csv('./proj3/static/countries/countries.csv', delimiter=';', encoding='latin1')  # Specify the delimiter and encoding

# Initialize wrong guess counter and country_name variable
wrong_guesses = 0
country_name = ""
random_row = None  # Define random_row globally

def reset_game():
    global country_name, wrong_guesses, random_row
    # Get a random row from the DataFrame
    random_row = df.sample()
    # Get the country name from the random row
    country_name = random_row['Country'].values[0]
    # Reset wrong guess counter
    wrong_guesses = 0

# Pass the random column name, country data, and filenames to your template
@app.route('/')
def index():
    global wrong_guesses, random_row, country_name
    reset_game()  # Reset the game for a new round
    random_column_name = random.choice(df.columns)
    return render_template('index.html', country=random_row.to_dict(), country_name=country_name, random_column_name=random_column_name, wrong_guesses=wrong_guesses)

@app.route('/results', methods=['POST'])
def results():
    global wrong_guesses, country_name, random_row
    guess = request.form.get('guess')
    action = request.form.get('action')

    if action == 'skip':
        reset_game()  # Reset the game for a new round
        random_column_name = random.choice(df.columns)
        return render_template('index.html', country=random_row.to_dict(), country_name=country_name, random_column_name=random_column_name, wrong_guesses=wrong_guesses)

    if guess.lower() != country_name.lower():
        wrong_guesses += 1  # Increment wrong guess counter
        message = "Incorrect guess. Please try again."
        
        # Determine what information to reveal based on wrong guess count
        reveal_info = ""
        if wrong_guesses == 2:
            reveal_info = "Continent: " + random_row['Continent'].values[0]
        elif wrong_guesses == 4:
            reveal_info = "Capital: " + random_row['Capital'].values[0]
        elif wrong_guesses == 6:
            reveal_info = "Flag: " + random_row['Flag'].values[0]
        elif wrong_guesses >= 8:  # If more than 6 wrong guesses, show the correct answer
            message = "You've run out of guesses. The correct answer was " + country_name
        return render_template('index.html', country=random_row.to_dict(), country_name=country_name, message=message, reveal_info=reveal_info, wrong_guesses=wrong_guesses)
    else:
        reset_game()  # Reset the game for a new round
        random_column_name = random.choice(df.columns)
        return render_template('index.html', country=random_row.to_dict(), country_name=country_name, message="You've guessed the correct answer!", random_column_name=random_column_name, wrong_guesses=wrong_guesses)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
