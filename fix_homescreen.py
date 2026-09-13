import re

filepath = 'app/src/main/java/com/example/ui/screens/home/HomeScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('items(categories, key = { category.id }) { category ->', 'items(categories, key = { category }) { category ->')

# Also check for index item -> item.id where item is actually string or something without id.
# But most others are media objects.
with open(filepath, 'w') as f:
    f.write(content)
