with open('app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

text = '<resources>\n' + text

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)
print("Fixed strings.xml again!!!")
