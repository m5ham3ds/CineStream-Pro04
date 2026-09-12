with open('app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

# find first </resources>
first_index = text.find('</resources>')
if first_index != -1:
    text = text[:first_index] + text[first_index + len('</resources>'):]
    
# find the next <resources>
second_index = text.find('<resources>')
if second_index != -1:
    text = text[:second_index] + text[second_index + len('<resources>'):]

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)
print("Fixed strings.xml again!")
