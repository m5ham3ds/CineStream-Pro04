import re
with open("app/src/main/res/values/strings.xml", "r", encoding="utf-8") as f:
    content = f.read()

new_strings = """
    <string name="download_and_watch">Download &amp; Watch </string>
    <string name="offline_highlight">Offline</string>
    <string name="personalized_prefix">Personalized </string>
    <string name="for_you_highlight">for You</string>
"""

content = content.replace("</resources>", new_strings + "</resources>")

with open("app/src/main/res/values/strings.xml", "w", encoding="utf-8") as f:
    f.write(content)
