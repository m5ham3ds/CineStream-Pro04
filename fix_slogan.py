import re
with open("app/src/main/res/values/strings.xml", "r") as f:
    content = f.read()

content = re.sub(r'<string name="slogan2">.*?</string>', '<string name="slogan2">Movies. Series. Anime Endless entertainment.</string>', content, flags=re.DOTALL)

with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(content)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content_ar = f.read()

content_ar = re.sub(r'<string name="slogan2">.*?</string>', '<string name="slogan2">أفلام. مسلسلات. أنمي ترفيه لا ينتهي.</string>', content_ar, flags=re.DOTALL)

with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(content_ar)
