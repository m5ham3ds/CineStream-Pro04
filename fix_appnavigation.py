import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

pattern = r"(<IconButton.*?Icon\(.*?Icons\.Default\.Menu.*?\).*?<\/IconButton>.*?Spacer.*?Box.*?contentAlignment = Alignment.Center.*?\{.*?\})?"
# I will use a different approach. The user wants the name in the header to be dynamic, but wait, the profile picture and menu icon are on the right and left, and my code put the title in the middle. Let's see what else they meant by "original style". I will remove the avatar and replace with the text maybe? Let me check the original file content.
