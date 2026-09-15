import re
with open("app/src/main/res/values/strings.xml", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Movies. Series. Anime\nEndless entertainment.", r"Movies. Series. Anime\nEndless entertainment.")

with open("app/src/main/res/values/strings.xml", "w", encoding="utf-8") as f:
    f.write(content)
