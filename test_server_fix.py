import re
with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    c = f.read()

if "var isMainSite" in c:
    print("Fix applied successfully")
else:
    print("Fix not applied")
