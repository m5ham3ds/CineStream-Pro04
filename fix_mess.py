import re
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

# Replace the wrong emit back to the normal one in ALL places FIRST
text = text.replace('emit(response.results.filter { (it.releaseDate ?: "") > today || (it.firstAirDate ?: "") > today }.map { it.toDomain() })', 'emit(response.results.map { it.toDomain() })')

# Remove the incorrectly placed 'val today = LocalDate.now().toString()'
# (It might be in getUpcomingMovies, but we'll re-add it carefully)
text = text.replace('val today = LocalDate.now().toString()\n            emit(response.results.map { it.toDomain() })', 'emit(response.results.map { it.toDomain() })')

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

