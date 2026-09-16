with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

if c.endswith("}\n"):
    c = c[:-2]

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

