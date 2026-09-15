with open("app/src/main/res/values/strings.xml", "r") as f:
    content = f.read()

if "name=\"done\"" not in content:
    content = content.replace("</resources>", "    <string name=\"done\">Done</string>\n</resources>")

with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(content)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content_ar = f.read()

if "name=\"done\"" not in content_ar:
    content_ar = content_ar.replace("</resources>", "    <string name=\"done\">تم</string>\n</resources>")

with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(content_ar)
