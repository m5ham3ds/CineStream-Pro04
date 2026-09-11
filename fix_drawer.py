import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

# I will find each NavigationDrawerItem block and replace its onClick.
def replacer(match):
    # This regex is too hard, let's just write the whole block manually.
    pass

