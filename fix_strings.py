with open('app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

missing = """    <string name="trending_anime">Trending Anime</string>
    <string name="trending_movies">Trending Movies</string>
"""

text = text.replace('</resources>', missing + '</resources>')

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)
