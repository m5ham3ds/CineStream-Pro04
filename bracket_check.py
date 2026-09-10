with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    text = f.read()

count = 0
for i, c in enumerate(text):
    if c == '{': count += 1
    if c == '}': count -= 1

print("Bracket balance:", count)
