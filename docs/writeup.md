# Bear Trivia Writeup
## Isa Blancett, Matt Brucker


### Reflection



### Practice Area Writeup


**Matt:** Deployment

In order to learn more about deployment, my main goal was to actually deploy the app so it can run on Heroku as opposed to on a laptop, since I knew basically nothing about deployment going into the project. I started by following the instructions on the Web Deployment toolbox to get Heroku up and running. Next, I added the environment variables from our project to the Heroku environment. Then, I started a PostgreSQL instance in Heroku and added code in the app to connect to the database. After that, it only needed minor changes in order to get the app running fully in the cloud. The actual codebase changes I had to make were pretty minor; the main change is in the bear controller, where I added a check to see if the Heroku environment variable for the database existed, and to connect to the Heroku Postgres instance instead of a local one if it does exist. I also added a Procfile and a runtime.txt to enable it to run in Heroku. I also did a writeup in our README as I went through the process in order to document the steps a user would take to do the same setup I did.
