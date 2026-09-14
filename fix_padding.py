import re

def fix_padding(filepath):
    with open(filepath, "r") as f:
        text = f.read()
        
    text = text.replace(".padding(bottom = 16.dp, start = 8.dp)", ".padding(start = 8.dp, bottom = 16.dp)")
    text = text.replace(".padding(bottom = 16.dp, end = 8.dp)", ".padding(end = 8.dp, bottom = 16.dp)")
    
    with open(filepath, "w") as f:
        f.write(text)

fix_padding("app/src/main/java/com/example/ui/components/SharedUI.kt")
fix_padding("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt")
