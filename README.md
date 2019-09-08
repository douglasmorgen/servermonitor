Description of program:
This program runs the magnificent server and a Flask polling app that checks the magnificent server at random intervals between 5 and 15 seconds. It keeps a database of the responses for the last 20 minutes, and periodically deletes any responses older than 20 minutes to save space on disk. The 'update' function within the flask app periodically gets the result from the Magnificent server

Usage:
Before you get started:
1. Make sure you have python3 and pip3 installed
2. Be operating on linux
Steps to run:

1. Unzip file contents
2. Create virtual environment in project root directory. When you are running in your virtual environment you'll see a (env) in front of your command prompt
    ~sauce$ python3 -m venv env
3. Start your virtual environment:
    ~sauce$ source env/bin/activate
4. Install all the dependencies for pip:
    (env)~sauce$ pip3 install -r requirements.txt
PLEASE NOTE: You may have to install an addition requirement: 
(env)~sauce$ pip3 install wheel
then rerun step 4

5. Setup the database (you may want to delete the crud.sqlite file in the root directory as well):
    start a python session:
    (env)~sauce$ python3
    Import the database from the app, drop all tables, create all tables, and exit 
    >>from polling import db
    >>db.drop_all()
    >>db.create_all()
    >>exit()
6. Start magnificent server and Flask app:
    (env)~sauce$ python3 ./magnificent.py
    in new terminal, activate virtual environment and start polling app:
    ~sauce$ source env/bin/activate
    (env)~sauce$ python3 ./polling.py

Your magnificent server and polling app are now running. Usage:
http://localhost:12345/ Location of the Magnificent server. If you stop the Magnificent server, you'll start to get 'non-response' as the resonse code for the polling app
http://localhost:5000/poll : Adds a response and returns the response added in JSON
http://localhost:5000/frontend : displays last 10 polling responses, and a graph summary and table summary of all responses received in the last 5 minutes
http://localhost:5000/show_responses : returns JSON of the all responses received in the last 5 minutes sorted by most recent to oldest

Tests:
Selenium Unit Tests:
(env)~sauce$ python3 ./seleniumtest.py
Tests all polling endpoints in a firefox browser

It checks all 3 urls. Make sure that the firefox gecko driver (https://github.com/mozilla/geckodriver/releases) is installed in your path, either /usr/local/bin or /usr/bin

Flask Unit Tests:
(env)~sauce$ python3 ./flasktest.py
Tests all polling endpoints

Sauce Labs Test
(env)~sauce$ python3 ./saucetest.py
PLEASE NOTE:
I couldn't get Sauce connect to work with the proper tunnel ID (os.environ['CI_TUNNEL_ID'])...I had it connected on my machine but for some reason it didn't find my environment variables properly. 

TO DOS
1. Finish the endpoint http://localhost:5000/frontendapi to return JSON to dynamically populate the last 10 responses table, responses count table, and responses graph instead of manually reloading the page through the header
2. Cache static assets so that only the minimal HTML loads each time
3. Use local assets for chartist.js instead of relying on canvasjs library
4. Deeper unit testing of the flask app, including database connectivity, database insertion, and other database transactions
5. Integrate Sauce Labs Connect into the Selenium tests
