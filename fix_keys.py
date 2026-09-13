import os
import re

directories = ['app/src/main/java/com/example/ui/screens/home', 'app/src/main/java/com/example/ui/screens/details']

for root, dirs, files in os.walk(directories[0]):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            # For items(items) { item -> ... }
            # Usually it's items(historyItems) { item ->
            content = re.sub(r'items\((.*?)\) { (.*?) ->', r'items(\1, key = { \2.id }) { \2 ->', content)
            
            # For itemsIndexed(items) { index, item -> ... }
            content = re.sub(r'itemsIndexed\((.*?)\) { index, (.*?) ->', r'itemsIndexed(\1, key = { index, \2 -> \2.id }) { index, \2 ->', content)
            
            # Special case for pairs like itemsIndexed(items) { index, (media, isMovie) ->
            # Let's fix that specifically for screens using it
            if '(media, isMovie)' in content:
                content = re.sub(r'itemsIndexed\((.*?)\) { index, \(media, isMovie\) ->', r'itemsIndexed(\1, key = { _, pair -> pair.first.hashCode() }) { index, (media, isMovie) ->', content)

            with open(filepath, 'w') as f:
                f.write(content)

