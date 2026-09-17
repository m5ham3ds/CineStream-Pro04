with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f: c = f.read()

# Add 1 brace before private fun formatTime
import re
c = re.sub(r'(\s+\})+\nprivate fun formatTime', '\n    }\n}\n}\nprivate fun formatTime', c)

# Remove 1 brace from the end
c = c[::-1].replace("}", "", 1)[::-1]

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f: f.write(c)

