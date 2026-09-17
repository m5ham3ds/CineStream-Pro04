import re
with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "r") as f: c = f.read()
c = re.sub(r'(\s+\})+\n@Composable\nfun RowScope\.ContentTypeCard', '\n    }\n}\n@Composable\nfun RowScope.ContentTypeCard', c)
with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "w") as f: f.write(c)
