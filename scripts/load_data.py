'''
    Menu algorithm adapted from the following. Originally developed in menu-app repos.
    https://python-forum.io/thread-9200.html
    https://www.reddit.com/r/learnpython/comments/zk8kld/can_you_use_a_dictionary_to_pick_a_function_to_run/
'''

'''
  Load data based on following. Originally developed in dj-mycareerhub-work repo.
  https://www.google.com/search?q=django+load+fixtures+programmatically&sca_esv=125e8b9873143113&udm=14&ei=wiQ7ab-qB-mkptQP9JjBmAE&oq=django+load+fixtures+&gs_lp=Ehlnd3Mtd2l6LW1vZGVsZXNzLXdlYi1vbmx5IhVkamFuZ28gbG9hZCBmaXh0dXJlcyAqAggBMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBRAAGO8FSMBXUMYcWM1HcA54AZABAJgBdqAB_giqAQQxMy4yuAEByAEA-AEBmAIdoAKRCsICChAAGEcY1gQYsAPCAgoQABiABBiKBRhDwgIHEAAYgAQYDcICCBAAGAUYHhgNwgIIEAAYCBgeGA3CAgYQABgeGA2YAwDiAwUSATEgQIgGAZAGCJIHBDI3LjKgB5FPsgcEMTMuMrgHzAnCBwgwLjkuMTkuMcgHaIAIAQ&sclient=gws-wiz-modeless-web-only

  https://stackoverflow.com/questions/887627/programmatically-using-djangos-loaddata

  https://docs.djangoproject.com/en/5.2/ref/django-admin/#running-management-commands-from-your-code
  example usage: https://pytest-django.readthedocs.io/en/latest/database.html

  https://stackoverflow.com/questions/15556499/django-db-settings-improperly-configured-error
'''


# Source - https://stackoverflow.com/questions/15556499/django-db-settings-improperly-configured-error
# Posted by MagTun, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-13, License - CC BY-SA 4.0

import os
import django
from django.core.management import call_command
import shutil
import sys

# Source - https://stackoverflow.com/questions/62461013/using-django-settings-module-in-a-script-in-subfolder
# Posted by revliscano, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-23, License - CC BY-SA 4.0
"""Yes, the problem arose when you changed the script location because then the root directory was not in the sys.path list anymore. You just need to append the root directory to the aforementioned list in order to be able to load the settings.py file of your project. 

If you have the script now in myrepo/useful_tools/import_filenames/populator.py, then you will need to go back three folders down in your folders tree to be back in your root directory. For this purpose, we can do a couple of tricks using the os module. """

sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 2)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mch_site.settings")
django.setup()


def load_lookup_tables():
    print("loading lookup tables...")
    # python manage.py loaddata lookup_tables.json
    call_command("loaddata", "lookup_tables.json")


def load_core_sample_data():
    print("loading core sample data...")
    call_command("loaddata", "sample_data_0_core.json")


def load_resumes_sample_data():
    print("loading resumes sample data...")
    call_command("loaddata", "sample_data_1_resumes.json")


def load_portfolio_sample_media():
    # creates the media folder (if needed), continues if directory exists, and overwrites files. this is okay since this is for sample data.
    print("creating media folder (if needed) & copying sample media")
    shutil.copytree("sample_media", "media", dirs_exist_ok=True)


def load_portfolio_sample_data():
    print("loading portfolio sample data...")
    call_command("loaddata", "sample_data_2_portfolio.json")


def load_all():
    load_lookup_tables()
    load_core_sample_data()
    load_resumes_sample_data()
    load_portfolio_sample_media()
    load_portfolio_sample_data()


def goodbye():
    print("Goodbye")


menu = {
    "A": {"description": "Load lookup tables", "action": load_lookup_tables},
    "B": {"description": "Load core sample data", "action": load_core_sample_data},
    "C": {"description": "Load resumes sample data", "action": load_resumes_sample_data},
    "D": {"description": "Load portfolio sample media", "action": load_portfolio_sample_media},
    "E": {"description": "Load portfolio sample data", "action": load_portfolio_sample_data},
    "F": {"description": "Load all of the above", "action": load_all},
    "Q": {"description": "quit", "action": None}
}


def display_menu():
    print('\nMenu:')
    for option, details in menu.items():
        print(f"{option} : {details['description']}"
              )


while True:
    display_menu()
    option = input("Select an option: ").upper()
    if option in menu.keys():
        print(f"You have chosen {menu[option]['description']}")
        if option == 'Q':
            goodbye()
            break
        menu[option]['action']()
    else:
        # need in else. otherwise, this gets called regardless
        print('Sorry, that option is not available, please make another selection')
