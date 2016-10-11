## SmartCushion API

Python API for handling user requests from Smart Cushion

### About SmartCushion

![SmartCushion Prototype](https://s3-us-west-2.amazonaws.com/smart-chair/IMG_20161009_184210939.jpg "SmartCushion Prototype")

SmartCushion turns any chair into a smart chair. It tracks how long you've been sitting and reminds you to get up and stretch. If you start to slouch, it buzzes and reminds you to correct your posture!

### Setup

Clone github repository:

```
$ git clone https://github.com/bfortuner/smart_chair.git
```

Setup virtualenv:
```
$ sudo easy_install pip
$ sudo pip install virtualenv
$ virtualenv smartchairenv
$ . smartchairenv/bin/activate
```

Now install the required modules:
```
$ cd smart_chair
$ pip install -r requirements.txt
```

Create required ENV variables (add to ~/.bash_profile or ~/.zshrc)
```
export SMART_CHAIR_APP_SECRET_KEY=''
export SMART_CHAIR_DATABASE_URI=''
export SMART_CHAIR_CONFIG='TestConfig'
```
*Email admins for keys

Create or Reset the Shared Devo Database
```
$ python create_db.py
```

Now you can launch the app:
```
$ python application.py
```
And point your browser to http://0.0.0.0:5000


### Deployment

Deploy to Heroku:
```
$ git add --all
$ git commit -m 'My Commit Message'
$ git push heroku master
```

Helpful Heroku Commands
```
$ git push -f heroku master  #Override everything in the Heroku Repo with your local changes
$ git push heroku mydevbranch:master  #Deploy your development branch changes to Heroku
$ heroku run bash  #ssh into dyno
$ heroku pg:psql --app smartchairapp DATABASE  #login to postgres db
```
