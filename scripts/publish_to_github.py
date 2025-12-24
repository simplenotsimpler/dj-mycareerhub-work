"""
Script: publish_to_github
Purpose: publish the static part of your Django site to GitHub Pages via Django Distill
Details: Publishes to top level <user>.github.io or <organization>.github.io site. Other repos will make a subsite and will not correctly resolve static & media urls. Originally developed in dj-mycareerhub-distill repo.
-- Create a repo with the corresponding name.
-- Set your DISTILL_DIR to the docs folder of this site, e.g. <user>.github.io/docs, so you do not overwrite the .git folder and other files in the repo.
-- Set your publishing source to the branch option & select the /docs folder.
"""

import os
import sys
import shutil

# check that virtual environment activated before try import Django
"""
  Sources:
  https://www.geeksforgeeks.org/python/determining-if-python-is-running-in-a-virtualenv/
  https://stackoverflow.com/questions/1871549/how-to-determine-if-python-is-running-inside-a-virtualenv
  https://allanderek.github.io/posts/import-placement/
  https://www.codecademy.com/article/python-exit-commands-quit-exit-sys-exit-os-exit-and-keyboard-shortcuts
"""
if sys.base_prefix != sys.prefix:
    from django.core.management import call_command
    from django.conf import settings
    import django
else:
    print("Virtual env not activated. Please activate before running.\nQuiting...")
    quit()


sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 2)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mch_site.settings")
django.setup()

# get the output dir from settings
OUTPUT_DIR = getattr(settings, 'DISTILL_DIR', None)
STATIC_SITE_REPO_DIR = getattr(settings, 'STATIC_SITE_REPO_DIR', None)
LICENSE_FILE = '../documentation/portfolio_docs/LICENSE'
README_FILE = '../documentation/portfolio_docs/README.md'

# called based on signature in https://github.com/meeb/django-distill/blob/master/django_distill/management/commands/distill-local.py
call_command("distill-local", OUTPUT_DIR,
             collectstatic="collectstatic", force="force")


# https://stackabuse.com/bytes/handling-yes-no-user-input-in-python/
copy_docs = input(
    "\nDo you want to copy the LICENSE and README to the Static Site Repo Directory? (yes/no): ")

if copy_docs.lower() in ["yes", "y"]:
    # copy license
    # https://builtin.com/data-science/copy-a-file-with-python
    try:
        shutil.copy(LICENSE_FILE, STATIC_SITE_REPO_DIR)

        # copy portfolio README
        shutil.copy(README_FILE,
                    STATIC_SITE_REPO_DIR)

        print("\nPublished portfolio, license & README to GitHub pages repo.")
    except:
        print("Sorry, the license and/or README file does not exist.")

else:
    print("\nPublished portfolio to GitHub pages repo.")

print("\nNext step: commit & push changes from the repo.\n")
