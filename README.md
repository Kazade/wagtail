# Wagtail GAE

This project is an experiment to see if we are able to run Wagtail CMS 
on Google App Engine using Djangae to provide database backend.

## Progress so far

- [x] `wagtail start mysite` produces a Wagtail and Djangae scaffold compatible project.
- [x] most (but not all!) of the migrations work and can be applied
- [x] Wagtail now works with simulated ContentTypes from Djangae
- [x] You can run `./manage.py runserver` and most of the Admin and public facing things look like they're working...

## TODO

[Look at Issues](https://github.com/potatolondon/wagtail-gae/issues) 

# How to start developing Wagtail-GAE?

There could be a better way to setup your local environment, but I've done it this way so far:

1. Clone this project to your local machine
2. Create a virtualenv in your preferred way (either directly via `virtualenv` or via `virtualenv-wrapper`.
3. Activate the virtualenv.

The virtualenv will serve as the environment of a test project, a django application that will run wagtail-gae.

4. Run `./setup.py develop` in wagtail-gae project root. This will install wagtail-gae into your virtualenv but instead of copying the source files into your virtualenv's `sitepackages` directory will install a symlink to current directory. This means changes to wagtail-gae will have immediate effect when you use wagtail in your virtualenv.
5. Run `npm install` to install the wagtail admin frontend dependencies.
6. Run `npm run build` to build frontend assets.
7. `cd` out of `wagtail-gae` and create a directory under your workspace for a test project.
8. Inside the new directory for the test project and with the virtualenv activated, run `wagaetail start [test-site-name]`. This will create a basic wagtail/djangae application structure.
9. `cd` into `[test-site-name]` and run `./install_deps --wagae-develop`. This will create and populate the local `sitepackages/` in your test project including the AppEngine SDK. `--wagae-develop` symlinks
10. Run migrations, skipping those that are not working yet:
  ```
  ./manage.py migrate
  ./manage.py migrate wagtaildocs 0006 --fake
  ./manage.py migrate
  ./manage.py migrate wagtailimages 0004 --fake
  ./manage.py migrate
  ./manage.py migrate wagtailimages 0012 --fake
  ./manage.py migrate
  ```

# What's the idea?

This is a fork of Wagtail, so ideally, we wanna create tiny commits that will 
be applied easily if we need to rebase to a newer version of Wagtail.
