with open('app/src/main/java/com/example/domain/repository/MediaRepository.kt', 'r') as f:
    text = f.read()

broken = """    fun getUpcomingMovies(): Flow<List<Movie>>"""
fixed = """    fun getUpcomingMovies(): Flow<List<Movie>>
    fun getUpcomingSeries(): Flow<List<Series>>
    fun getUpcomingAnime(): Flow<List<Series>>"""

if broken in text:
    text = text.replace(broken, fixed)
    with open('app/src/main/java/com/example/domain/repository/MediaRepository.kt', 'w') as f:
        f.write(text)
    print("Fixed MediaRepository Interface")
else:
    print("Could not find broken string in MediaRepository")
