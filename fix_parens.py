import re
import os

files = [
    'app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/PopularScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt'
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the line that starts with 'else -> (' but doesn't end with ')'
    new_lines = []
    for line in content.split('\n'):
        if line.strip().startswith('else -> (') and not line.strip().endswith(')'):
            line = line + ')'
        new_lines.append(line)

    with open(file_path, 'w') as f:
        f.write('\n'.join(new_lines))
