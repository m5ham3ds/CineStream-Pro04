import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

target = """            }
        }
        
extractingEmbedUrl?.let { url ->"""

replace = """            }
        }
    }
}
        
extractingEmbedUrl?.let { url ->"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

