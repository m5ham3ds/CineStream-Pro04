with open("app/src/main/res/values/strings.xml", "r") as f:
    c = f.read()

c = c.replace("We're here to help you", r"We\'re here to help you")
with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(c)
