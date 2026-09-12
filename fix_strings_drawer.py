import re

with open('app/src/main/res/values/strings_drawer.xml', 'r') as f:
    text = f.read()

text = re.sub(r'<string name="library">.*?</string>', '', text)
text = re.sub(r'<string name="about_app">.*?</string>', '', text)
text = re.sub(r'<string name="help_support">.*?</string>', '', text)
text = re.sub(r'<string name="login">.*?</string>', '', text)
text = re.sub(r'<string name="logout">.*?</string>', '', text)
text = re.sub(r'<string name="logout_confirm">.*?</string>', '', text)

with open('app/src/main/res/values/strings_drawer.xml', 'w') as f:
    f.write(text)

with open('app/src/main/res/values/strings_bottom_nav.xml', 'r') as f:
    text = f.read()
    
text = re.sub(r'<string name="movies">.*?</string>', '', text)
text = re.sub(r'<string name="series">.*?</string>', '', text)
text = re.sub(r'<string name="anime">.*?</string>', '', text)

with open('app/src/main/res/values/strings_bottom_nav.xml', 'w') as f:
    f.write(text)
    
print("Removed duplicate strings from extra files.")
