with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    text = f.read()

# First, remove the two "}" from the very end of the file that I just appended
text = text.rstrip()
if text.endswith("}"): text = text[:-1].rstrip()
if text.endswith("}"): text = text[:-1].rstrip()

# Now find the end of AppNavigation function and insert "} } "
target = "fun NavGraphBuilder.addAuthGraph"
if target in text:
    text = text.replace(target, "        }\n    }\n\n" + target)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(text)
