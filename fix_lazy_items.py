import re
import os

files_to_fix = [
    'app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/PopularScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt'
]

for fpath in files_to_fix:
    with open(fpath, 'r') as f:
        content = f.read()
    
    # The line looks like:
    # itemsIndexed(items, key = { index, (media, isMovie) -> (media, isMovie).id }, key = { _, pair -> pair.first.hashCode() }) { index, (media, isMovie) ->
    # I want it to be:
    # itemsIndexed(items, key = { index, pair -> "${if(pair.second) (pair.first as com.example.domain.models.Movie).id else (pair.first as com.example.domain.models.Series).id}-$index" }) { index, (media, isMovie) ->
    
    bad_line_pattern = re.compile(r'itemsIndexed\(items.*?\)\s*\{\s*index,\s*\(media,\s*isMovie\)\s*->')
    good_line = 'itemsIndexed(items, key = { index, pair -> "${if(pair.second) (pair.first as com.example.domain.models.Movie).id else (pair.first as com.example.domain.models.Series).id}-$index" }) { index, (media, isMovie) ->'
    
    content = bad_line_pattern.sub(good_line, content)
    
    with open(fpath, 'w') as f:
        f.write(content)

