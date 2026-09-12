with open('app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

missing = """    <string name="library">Library</string>
    <string name="about_app">About App</string>
    <string name="help_support">Help and Support</string>
    <string name="login">Log In</string>
    <string name="logout">Log Out</string>
    <string name="logout_confirm">Are you sure you want to log out?</string>
    <string name="yes">Yes</string>
    <string name="no">No</string>
    <string name="movies">Movies</string>
    <string name="series">Series</string>
    <string name="anime">Anime</string>
"""

text = text.replace('</resources>', missing + '</resources>')

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)

with open('app/src/main/res/values/strings_drawer.xml', 'w') as f:
    f.write('<resources></resources>')

with open('app/src/main/res/values/strings_bottom_nav.xml', 'w') as f:
    f.write('<resources></resources>')
    
print("Added all missing strings to strings.xml")
