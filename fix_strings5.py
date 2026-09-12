with open('app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

text = text.replace('</resources>', """
    <string name="about">About</string>
    <string name="extensions">Extensions</string>
    <string name="share">Share</string>
    <string name="social">Social</string>
</resources>""")

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)
print("Added missing strings!")
