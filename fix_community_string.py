with open("app/src/main/res/values/strings.xml", "r") as f:
    content = f.read()
content = content.replace("<string name=\"community\">CineStream Community</string>", "<string name=\"community\">Community</string>")
with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(content)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content_ar = f.read()
content_ar = content_ar.replace("<string name=\"community\">مجتمع CineStream</string>", "<string name=\"community\">المجتمع</string>")
with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(content_ar)
