**The URL for the Final Heroku app (Version 2.0) is**: https://mighty-stream-05426.herokuapp.com/ \
The URL for the Heroku app (Version 1.0) is: https://aqueous-castle-25369.herokuapp.com/

# Welcome to Book Bite

We are making this application based on the the idea of creating a web page of book browsing and reviewing
In Sprint 1, the user should be able to sign up by using email, username and password. The user logs in with email and password
Upon landing on the main page, the user has three option: get books recommendations based on themes, search book by title, and view books in favorite list
On the book recommendation page, the user can choose from a drop list of themes. Then the user will get 6 random books based on the chosen theme.
On the search book by title page, the user can type in the book title and hit submit. The result is generated underneath.
On the favorite page, the user can see a list of books he added to the list.
Upon every book title shown on the page, there is a button to let the user explore more information about the book. The page will display basic information about the book such as author, author biography, a summary of the book, the themes of the book, and the page number of the book.
The user can also add the book to favorite list.

## Technology used in this project

The project utilizes the **Flask** framework for Python to run the application.
In addition, we install **requests** to pull API requests, and **dotenv** to pull my API key in the _.env_ file.
The library that we use is **os** to load my API key from _.env_ file.
The API that we use for this project are **Penguin**.  
The web interface is coded with HTML and styled with CSS.
User authentication is handled by **flask-login**, with function like **is_authenticated**, **load_user**, **login_user**, **logout_user**,...
Database model is handled with **FlaskAlchemy** and **PostgreSQL** the database is hosted on Heroku.

## Things to install for the app

Heroku: `sudo curl https://cli-assets.heroku.com/install.sh | sh # install Heroku`

PostgreSQL: `sudo apt install postgresql`
`sudo service postgresql start`
`sudo -u postgres psql # just testing that psql is installed. You should get an interactive prompt. Quit by entering "\q"`
`pip3 install psycopg2-binary`
`pip3 install Flask-SQLAlchemy==2.1`

Python: `pip3 install -r requirements.txt` to install all other packages for this project.
After you install all the dependencies, you need to run `heroku addons:create heroku-postgresql:hobby-dev -a {your-app-name}` to set up the database.
Then you run `heroku config -a {your-app-name}` and set the **DATABASE_URL** in \*.env\_ file to this link. The code already has a function to handle changing the url from "postgres" to "postgresql"

## Linting

The pylintrc file was added to disable "scoped session error" because pylint was giving a false positive error as if our database .add and .commit were not matched to any databases. Since this was obviously false, the error was disabled.
