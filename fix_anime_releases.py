import re
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

# Replace in getNewReleasesAnime
text = text.replace(
    'getAiringTodayAnime(apiKey, minDate = LocalDate.now().toString(), maxDate = LocalDate.now().plusMonths(1).toString())',
    'getAiringTodayAnime(apiKey, minDate = LocalDate.now().minusMonths(1).toString(), maxDate = LocalDate.now().toString())'
)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

