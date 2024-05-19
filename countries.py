import pandas as pd
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Reads the CSV file 
df = pd.read_csv('./proj3/static/countries/countries.csv')

#Function to reset game
def reset_game():
    global country_name, wrong_guesses, random_row, message #declares the variables as global variables
    random_row = df.sample() #selects a random (country) row from the CSV 
    country_name = random_row['Country'].values[0] #extracts the value of the 'Country' column then assigns it to 'country_name'
    wrong_guesses = 0 #Counts the number of wrong guesses (0=default)
    message = ""  #Message("---empty---"=default)

#Route for the main URL
@app.route('/')
def index():
    reset_game() #Calls for the reset function
    random_column_name = random.choice(df.columns) #Selects a random column name from the DataFrame
    return render_template('index.html', country=random_row.to_dict(), #Renders the index.html
                           country_name=country_name, 
                           random_column_name=random_column_name, 
                           wrong_guesses=0)

#Route for the results URL
@app.route('/results', methods=['POST'])
def results():
    guess = request.form.get('guess') #Retrieves the value of the form field named 'guess' from the request form
    action = request.form.get('action') #Retrieves the value of the form field named 'action' from the request form

    if action in ['skip', 'play_again']: #checks if the value of 'action' is either 'skip' or 'play_again'
        reset_game() #If it is one of the two, it resets the game
        random_column_name = random.choice(df.columns)
        return render_template('index.html', country=random_row.to_dict(), 
                               country_name=country_name, 
                               random_column_name=random_column_name, 
                               wrong_guesses=0)

    global message #Declares the variable 'message' as global
    if guess.lower() != country_name.lower(): #checks if the lowercase version of the user's guess does not match the lowercase version of the actual country name
        wrong_guesses = int(request.form.get('wrong_guesses')) + 1 #retrieves the value of 'wrong_guesses' then 1 is added in the 'wrong_guesses'
        message = "Incorrect guess. Please try again." #Message if answer in incorrect
        reveal_info = "" #Initializes the variable 
        if wrong_guesses == 2: #Reveals the continents where the country is from
            reveal_info = "Continent: " + random_row['Continent'].values[0]
        elif wrong_guesses == 4: #Reveals the capital of the country
            reveal_info = "Capital: " + random_row['Capital'].values[0]
        elif wrong_guesses == 6:#Reveals the flag of the country
            reveal_info = "Flag: " + random_row['Flag'].values[0]
        elif wrong_guesses >= 8: #When 'wrong_guesses' reaches 8, the game is over
            message = "You've run out of guesses. The correct answer was " + country_name
        remaining_guesses = 8 - wrong_guesses  # Calculates remaining guesses
        return render_template('index.html', country=random_row.to_dict(), 
                               country_name=country_name, 
                               message=message, 
                               reveal_info=reveal_info, 
                               wrong_guesses=wrong_guesses,
                               remaining_guesses=remaining_guesses,
                               correct_guess=False)  # Pass correct_guess as False for incorrect guess
    else:
        reset_game() #Resets game
        random_column_name = random.choice(df.columns) #Selects a random column name from the DataFrame
        return render_template('index.html', country=random_row.to_dict(), #Renders the index.html template
                               country_name=country_name, 
                               message="You've guessed the correct answer!", #Message indicating that the guess is wrong
                               random_column_name=random_column_name, 
                               wrong_guesses=0,
                               remaining_guesses=8,
                               correct_guess=True)  #Boolean value indicating that the guess was correct

if __name__ == '__main__':
    app.run(debug=True) #Ensures that the Flask application defined in the script is run
    