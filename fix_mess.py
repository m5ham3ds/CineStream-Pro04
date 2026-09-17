files = [
    "app/src/main/java/com/example/ui/screens/about/AboutScreen.kt",
    "app/src/main/java/com/example/ui/screens/social/SocialScreen.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
]

for fp in files:
    with open(fp, "r") as f:
        c = f.read()
    
    # revert the fix_syntax2.py change
    c = c.replace("        }\n    }\n}", "    }\n}", 1)
    
    # append the missing brace at the end of the file (since auto_brace removed it)
    c += "\n}\n"
    
    with open(fp, "w") as f:
        f.write(c)

# For DetailsScreens.kt
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# I did:
# c = c[:match.start(1)-18] + "                }\n            }\n            }\n        }\n    }\n}" + match.group(1) + c[match.end():]
# This added 3 extra braces.
# Let's just fix DetailsScreens.kt by balancing it properly.
# The compiler said:
# DetailsScreens.kt:930:5 Expecting a top level declaration
# DetailsScreens.kt:931:1 Expecting a top level declaration
# So there were 2 extra braces around line 930.

c = c.replace("                }\n            }\n            }\n        }\n    }\n}", "            }\n        }\n    }\n}", 1)

# auto_brace removed 2 braces from the end of the file. So let's add them back.
c += "\n}\n}\n"

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

