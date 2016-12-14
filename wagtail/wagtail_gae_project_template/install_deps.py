#!/usr/bin/env python

import os
import subprocess
import shutil
import stat
import platform
import argparse
import atexit

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen

REQUIREMENTS = [ "pip", "git" ]

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS_FILE = os.path.join(PROJECT_DIR, "requirements.txt")
TARGET_DIR = os.path.join(PROJECT_DIR, "sitepackages")
BACKUP_DIR = os.path.join(PROJECT_DIR, "sitepackages.backup")

APPENGINE_TARGET_DIR = os.path.join(TARGET_DIR, "google_appengine")

APPENGINE_SDK_VERSION = "1.9.40"
APPENGINE_SDK_FILENAME = "google_appengine_%s.zip" % APPENGINE_SDK_VERSION

# Google move versions from 'featured' to 'deprecated' when they bring out new releases
FEATURED_SDK_REPO = "https://storage.googleapis.com/appengine-sdks/featured/"
DEPRECATED_SDK_REPO = "https://storage.googleapis.com/appengine-sdks/deprecated/%s/" % APPENGINE_SDK_VERSION.replace('.o', '')


def install_app_engine_sdk():
    # First try and get it from the 'featured' folder
    sdk_file = urlopen(FEATURED_SDK_REPO + APPENGINE_SDK_FILENAME)
    if sdk_file.getcode() == 404:
        #Failing that, 'deprecated'
        sdk_file = urlopen(DEPRECATED_SDK_REPO + APPENGINE_SDK_FILENAME)

    # Handle other errors
    if sdk_file.getcode() >= 299:
        raise Exception('App Engine SDK could not be found. {} returned code {}.'.format(
            sdk_file.geturl(), sdk_file.getcode()))

    zipfile = ZipFile(StringIO(sdk_file.read()))
    zipfile.extractall(TARGET_DIR)

    # Make sure the dev_appserver and appcfg are executable
    for module in ("dev_appserver.py", "appcfg.py"):
        app = os.path.join(APPENGINE_TARGET_DIR, module)
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC)


def run_pip_install():
    args = ["pip", "install", "-r", REQUIREMENTS_FILE, "-t", TARGET_DIR, "-I", "-U"]
    p = subprocess.Popen(args)
    p.wait()


def symlink_editable_lib(package_name):
    # Find local sitepackages/ path and path to installed package in environment for each editable dependency
    local_path = os.path.join(TARGET_DIR, package_name)
    try:
        module = __import__(package_name)
        env_path = os.path.dirname(module.__file__)
    except ImportError:
        raise Exception("{0} not installed. Have you installed {0} into your virtualenv via "
                        "`setup.py develop`?".format(package_name))

    print("Creating symbolic link:\n  {} ->\n  {}".format(local_path, env_path))

    # Remove package distribution installed into sitepackages/ via pip
    if os.path.islink(local_path):
        os.remove(local_path)
    else:
        shutil.rmtree(local_path)

    # Create symbolic link to lib
    os.symlink(env_path, local_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Install wagtail-gae dependencies into local sitepackages/ directory along with the '
                    'Google AppEngine SDK.'
    )
    parser.add_argument(
        'editable_libs',
        nargs='*',
        help='Attempt to create symlink installs in sitepackages/ for the given package names. Installs a symlink in '
             'sitepackages/ to where package is installed in the currently active virtualenv. Assumes package was '
             'installed via pip -e (setuptools in \'develop\' mode).'
    )
    command_args = parser.parse_args()

    # Make sure the user has everything they need
    where = 'which'
    if platform.system() == 'Windows':
        where = 'where'

    for command in REQUIREMENTS:
        try:
            subprocess.check_output([where, command])
        except subprocess.CalledProcessError:
            raise RuntimeError("You must install the '%s' command" % command)

    # Ensure local sitepackages/ dir exists
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # Make a sitepackages/ backup so we can rollback at any time
    print("Creating sitepackages/ backup...")
    shutil.copytree(TARGET_DIR, BACKUP_DIR)

    # Register exit function that restores previous state if script fails or removes the
    # backup directory if script succeeds
    success = False

    @atexit.register
    def cleanup():
        if success:
            shutil.rmtree(BACKUP_DIR)
        else:
            print("Attempting to restore previous sitepackages/ state from backup...")
            shutil.rmtree(TARGET_DIR)
            shutil.move(BACKUP_DIR, TARGET_DIR)

    if not os.path.exists(APPENGINE_TARGET_DIR):
        print('Downloading the AppEngine SDK...')
        install_app_engine_sdk()
    else:
        print('Not updating SDK as it exists. Remove {} and re-run to get the latest SDK'.format(APPENGINE_TARGET_DIR))

    print("Running pip...")
    run_pip_install()

    # Install symlinks for editable packages supplied with --editable option
    if command_args.editable_libs:
        for package_name in command_args.editable_libs:
            print("Installing symlinks for editable lib: {}".format(package_name))
            symlink_editable_lib(package_name)

    # Record successful run before quiting and invoking cleanup function to destroy sitepackages/ backup
    success = True
