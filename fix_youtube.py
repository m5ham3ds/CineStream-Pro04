with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "r") as f:
    content = f.read()

content = content.replace('src="https://www.youtube.com/embed/${videoId}', 'src="https://www.youtube-nocookie.com/embed/${videoId}')

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(content)
