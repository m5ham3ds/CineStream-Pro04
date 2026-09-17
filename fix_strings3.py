import re

def ensure_string(filepath, key, value):
    with open(filepath, "r") as f:
        c = f.read()
    
    if f'<string name="{key}">' not in c:
        c = c.replace("</resources>", f'    <string name="{key}">{value}</string>\n</resources>')
        with open(filepath, "w") as f:
            f.write(c)

ensure_string("app/src/main/res/values/strings.xml", "today", "Today")
ensure_string("app/src/main/res/values-ar/strings.xml", "today", "اليوم")

