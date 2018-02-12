# Bear Trivia Writeup
## Isa Blancett, Matt Brucker


### Reflection

**What went well?**
We are proud of our ability to scope the project.  We decided on a project and deliverable that was reasonable for our time commitments and we found tools early on to aid the process.  Finding the Trivia database saved us a lot of time.  Integrating our separate codes went pretty seamlessly.  Another plus of our process is that we met for no longer than 1 hour at a time, multiple times a week, to check-in, clear up any blocks, and go over next steps.

**What could have gone better?**
We were very excited about the project so the first things we did involved straight-up coding, instead of looking at what would benefit our learning goals.  Since functionality had an earlier due date, we focused on that, rather than proof of diving into our areas of focus.  We also regret not talking to Oliver earlier about code quality tools, architecture, and databases.  We definitely put off refining these areas until the end of the project because they were the areas we were most unsure of.

**What did we learn?**
Matt learned a lot about deployment, especially with Heroku, and since he documented it well, Isa was able to use his documentation to aid deployment for another project.  Isa became more familiar with JSON and HTTP Requests, while Matt learned more about databases.  We both became a lot more comfortable building on existing projects to create our own program.

### Practice Area Writeup


**Matt:** Deployment

In order to learn more about deployment, my main goal was to actually deploy the app so it can run on Heroku as opposed to on a laptop, since I knew basically nothing about deployment going into the project. I started by following the instructions on the Web Deployment toolbox to get Heroku up and running. Next, I added the environment variables from our project to the Heroku environment. Then, I started a PostgreSQL instance in Heroku and added code in the app to connect to the database. After that, it only needed minor changes in order to get the app running fully in the cloud. The actual codebase changes I had to make were pretty minor; the main change is in the bear controller, where I added a check to see if the Heroku environment variable for the database existed, and to connect to the Heroku Postgres instance instead of a local one if it does exist. I also added a Procfile and a runtime.txt to enable it to run in Heroku. I also did a writeup in our README as I went through the process in order to document the steps a user would take to do the same setup I did.

**Isa** Code Quality
