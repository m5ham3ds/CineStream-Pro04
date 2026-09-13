import os

files = [
    'app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/PopularScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt'
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r') as f:
        content = f.read()

    content = content.replace('val animeStr = animeStr', 'val animeStr = stringResource(R.string.anime)')

    with open(file_path, 'w') as f:
        f.write(content)

