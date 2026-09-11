import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

def repl(match):
    # This regex is too hard to get right. 
    pass
