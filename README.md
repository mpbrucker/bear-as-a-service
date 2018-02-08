# Bear Trivia
## Created by Isa Blancett and Matt Brucker

Bear Trivia is a revolutionary new way to play trivia! Start a game of trivia with the bear, and he will ask you questions - send your answers via text, and earn points! Bear Trivia™ - it's fast, it's fun, and it's free.


## Getting Set Up (client only)

This requires a running Bear server, and a [Twilio ⟶ MQTT Gateway](https://github.com/olin-build/twilio-mqtt-gateway).

You should also have a Twilio phone number, and the credentials for
The Bear server and Twilio gateway.

## Local Install

Make sure you're running Python 3.6.

### Postgres Setup

Running Bear Trivia requires a running PostgreSQL server. Bear Trivia is designed to work with PostgreSQL 9.6, but earlier versions may work as well. Follow the instructions [here](https://wiki.postgresql.org/wiki/Detailed_installation_guides) to install PostgreSQL. Next, create the database:

`createdb trivia`

Now, create a user and grant privileges on the database:

```
$ sudo -u postgres psql
CREATE USER bearclient WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "trivia" to my_username;
```

Choose a password for `my_password`, and copy that value as `POSTGRES_KEY` in `envrc.template`.

### Environment Setup

Copy `envrc.template` to `.envrc`. On Linux/macOS: `cp envrc.template .envrc`.

Replace the strings in `.envrc` by your Twilio and MQTT credentials and phone number.

Execute: `source .envrc`

### Running the App

To install dependencies, run:

`pip3 install -r requirements.text`

Or, if you're using pipenv:

`pipenv install`

Start the Bear Trivia controller.

`python bear_controller.py`

Or, if you're using pipenv:

`pipenv run python bear_controller.py`

## Remote (Heroku) Install

To deploy this app remotely, you'll need a Heroku account; get one [here](https://signup.heroku.com/). Next, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) (Linux only). Run `heroku login` with the credentials you created, and run `heroku apps:create app-name`, where `app-name` is a unique name for your app.

### Remote Setup

In your app directory, run the following:

```
$ heroku git:remote -a app-name
$ git push heroku master
```

### Environment Variable Setup

In order to run the app remotely, you need to setup the environment variables in Heroku. You can do this by running `heroku config:set VAR_NAME=value` for every environment variable in `envrc.template`, *except* `DB_PASSWORD` (we will get a different database password once we set that up). Alternatively, you can input them in your app's Settings tab on the Heroku Dashboard.

### Heroku PosgreSQL Setup

To setup a basic PostgreSQL database in Heroku, run `heroku addons:create heroku-postgresql:hobby-dev`. That's all you need to do for setup: Heroku automatically creates a new environment variable `DATABASE_URL` when you create the PostgreSQL database, which contains the server, port, username, and password.

### Deployment

Once everything has been set up, run `git push heroku master` to push the app to Heroku.


## Acknowledgements

Based on Oliver Steele's [bear-as-a-service](https://github.com/olinlibrary/bear-as-a-service) project. All MQTT gateway and Twilio command code is based on the original bear-as-a-service project. Local install instructions, architecture diagram, and tests were also adapted from the original project's install instructions. The Heroku deployment instructions are also adapted from the [Olin Web Deployment Toolbox](https://toolboxes.olin.build/heroku/).

## LICENSE

MIT
