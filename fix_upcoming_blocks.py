import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

def replace_block(text, method_name, api_call, domain_mapper, filter_field):
    pattern = rf"(override fun {method_name}\(\): Flow<List<[a-zA-Z]+>> = flow {{\s*val response = RetrofitClient\.tmdbApi\.{api_call}\(apiKey\)\s*)emit\(response\.results\.map {{ it\.toDomain\(\) }}\)"
    replacement = rf"\1val today = LocalDate.now().toString()\n        emit(response.results.filter {{ (it.{filter_field} ?: \"\") > today }}.map {{ it.toDomain() }})"
    return re.sub(pattern, replacement, text)

# For getUpcomingMovies
text = replace_block(text, "getUpcomingMovies", "getUpcomingMovies", "Movie", "releaseDate")

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

