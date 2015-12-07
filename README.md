# AC Karma Sports FFA

![Build Status](https://circleci.com/gh/blueshiftedtech/ac-karma-sports-ffa.svg?style=shield&circle-token=796af2be83a851917163ffea6df2e3de41b40f62)

### Running Locally.

#### External Dependencies

 - [Python 3.5](https://www.python.org/)
 - [Node 5.1](https://nodejs.org/en/)
 - [Postgres 9.4](http://postgresapp.com/)
 - [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

With all these installed, we can move on to setting up the project.

#### Project Dependencies

First, we'll do some non-project specific setup. If you don't have gulp installed globally, you'll want to do so. If you have done this once before on any project, you can skip this step.

```sh
npm install --global gulp
```

Next, we'll want to set up a postgres database. This can be done quite simply.

```sh
createdb ackarma
```

Now we'll clone the project. Assuming you've set up SSH for git/github, it'll look something like this:

```sh
cd $PROJECTS_DIR
git clone git@github.com:blueshiftedtech/ac-karma-sports-ffa.git
cd ac-karma-sports-ffa
```

Now, we should probably set up our python virtualenv. I'm assuming you have virtualenvwrapper installed here. If you don't, a quick `pip install virtualenvwrapper` will install virtualenv and virtualenvwrapper for you.

```sh
mkvirtualenv ackarma --python=python3
```

If you see (ackarma) appended to your shell prompt, you'll know it worked correctly.

Once that's done, we'll be in the working directory for the project, now we can start installing our project dependencies.

```sh
npm install
pip install -r requirements.txt
```

We'll also need to set up our secrets, I've included a sample .env file which you can activate by doing:

```sh
cp .sample-env .env
```

Finally, you'll want to migrate the database, by running:

```sh
python manage.py migrate
```

And we're finally done!

#### Running the Project

We'll run two commands here. I keep them in two different tabs, personally.

Running gulp to compile SASS into CSS, and whatever else I add to it in the future. (probably JS concatenation and minification.) This will watch for file changes and reload, but on certain classes of syntax errors you'll need to manually kick it back off.

```sh
gulp
```

And Running the django debug server:

```sh
python manage.py runserver
```

#### Running tests.

Just run:

```sh
python manage.py test
```
