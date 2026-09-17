import re
with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "r") as f: c = f.read()
c = re.sub(r'(\s+\})+\n@Composable\nfun FeatureCard', '\n    }\n}\n@Composable\nfun FeatureCard', c)
with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "w") as f: f.write(c)
