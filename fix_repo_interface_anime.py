with open('app/src/main/java/com/example/domain/repository/MediaRepository.kt', 'r') as f:
    text = f.read()

broken = "fun getNewReleasesSeries(): Flow<List<Series>>"
fixed = "fun getNewReleasesSeries(): Flow<List<Series>>\n    fun getNewReleasesAnime(): Flow<List<Series>>"

if broken in text:
    text = text.replace(broken, fixed)
    with open('app/src/main/java/com/example/domain/repository/MediaRepository.kt', 'w') as f:
        f.write(text)
    print("Fixed MediaRepository Interface for Anime")
else:
    print("Could not find broken string in MediaRepository")
