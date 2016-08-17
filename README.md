# Wagtail GAE

This project is an experiment to see if we are able to run Wagtail CMS 
on Google App Engine using Djangae to provide database backend.

## Progress so far

- [x] `wagtail start mysite` produces a Wagtail and Djangae scaffold compatible project.
- [x] most (but not all!) of the migrations work and can be applied
- [x] Wagtail now works with simulated ContentTypes from Djangae
- [x] You can run `./manage.py runserver` and most of the Admin and public facing things look like they're working...

## TODO

- [ ] Fix three migrations that don't work at the moment: 
 - [ ] wagtaildocs 0006
 - [ ] wagtailimages 0004
 - [ ] wagtailimages 0012
- [ ] Catch all join queries and replace them with something Djangae can do
- [ ] Auth: need replacing Django's auth with gauth, because Permissions and Groups that Wagtail uses break lots of stuff :(
- [ ] Search: haven't looked yet into what needs happen for search to work
- [ ] Check images: do they work now? Do we need to update something to make them work with CSG?
- [ ] Run Wagtail test suite 

# How to start developing Wagtail-GAE?

There could be a better way to setup your local environment, but I've done it this way so far:

1. Clone this project to your local machine
2. Start a Wagtail project for development:
- You need to do `wagtail start mysite`, but `wagtail` needs to point to 
 `wagtail/bin/wagtail.py` that you just cloned.
- Run `./install_deps`
- Run migrations, skipping those that are not working yet: 

  ```
  ./manage.py migrate
  ./manage.py migrate wagtaildocs 0006 --fake
  ./manage.py migrate
  ./manage.py migrate wagtailimages 0004 --fake
  ./manage.py migrate
  ./manage.py migrate wagtailimages 0012 --fake
  ./manage.py migrate
  ```
  
3. In your local project, remove `djangae` and `wagtail` from packages, and symlink
your local copies of wagtail-gae and djangae for easier development. 
4. :tada:

# What's the idea?

This is a fork of Wagtail, so ideally, we wanna create tiny commits that will 
be applied easily if we need to rebase to a newer version of Wagtail.
