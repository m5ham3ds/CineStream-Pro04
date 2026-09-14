import re

# 1. Fix TmdbApiService.kt
with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    text = f.read()

# Remove duplicate language parameters
text = re.sub(r'(@Query\("language"\) language: String,\s*)+', r'@Query("language") language: String,\n        ', text)
text = re.sub(r',\s*@Query\("language"\) language: String\s*,\s*@Query\("language"\) language: String', r', @Query("language") language: String', text)

# Just in case, let's restore it to original and add carefully
text = text.replace('@Query("language") language: String,\n        @Query("language") language: String,', '@Query("language") language: String,')
text = text.replace('@Query("language") language: String,\n        @Query("language") language: String', '@Query("language") language: String')
text = text.replace('@Query("language") language: String, @Query("language") language: String', '@Query("language") language: String')
text = re.sub(r'(@Query\("language"\) language: String,\s*)+@Query\("language"\) language: String', r'@Query("language") language: String', text)

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(text)


# 2. Fix TmdbMediaRepositoryImpl.kt
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    repo_text = f.read()

# Add a language property
if "private val language =" not in repo_text:
    repo_text = repo_text.replace("private val apiKey = BuildConfig.TMDB_API_KEY", "private val apiKey = BuildConfig.TMDB_API_KEY\n    private val language = java.util.Locale.getDefault().toLanguageTag()")

# Replace calls to tmdbApi to include language
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(apiKey\)', r'\1(apiKey, language)', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.searchMulti)\(apiKey, query\)', r'\1(apiKey, language, query)', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(apiKey, minDate = "2026-09-11"\)', r'\1(apiKey, language, minDate = "2026-09-11")', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(apiKey, minDate = "2026-09-11", maxDate = "2026-10-11"\)', r'\1(apiKey, language, minDate = "2026-09-11", maxDate = "2026-10-11")', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(id\.toInt\(\), apiKey\)', r'\1(id.toInt(), apiKey, language)', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(personId\.toInt\(\), apiKey\)', r'\1(personId.toInt(), apiKey, language)', repo_text)
repo_text = re.sub(r'(RetrofitClient\.tmdbApi\.\w+)\(seriesId\.toInt\(\), seasonNumber, apiKey\)', r'\1(seriesId.toInt(), seasonNumber, apiKey, language)', repo_text)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(repo_text)


# 3. Fix SharedUI.kt and WatchingScreen.kt
# They need the language parameter in their tmdbApi calls as well, and the padding fix
for filepath in ["app/src/main/java/com/example/ui/components/SharedUI.kt", "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"]:
    with open(filepath, "r") as f:
        ui_text = f.read()
    
    # fix padding
    ui_text = ui_text.replace(".padding(start = 8.dp, bottom = 16.dp)", ".padding(start = 8.dp, top = 0.dp, end = 0.dp, bottom = 16.dp)")
    ui_text = ui_text.replace(".padding(end = 8.dp, bottom = 16.dp)", ".padding(start = 0.dp, top = 0.dp, end = 8.dp, bottom = 16.dp)")
    ui_text = ui_text.replace(".padding(bottom = 16.dp, start = 8.dp)", ".padding(start = 8.dp, top = 0.dp, end = 0.dp, bottom = 16.dp)")
    ui_text = ui_text.replace(".padding(bottom = 16.dp, end = 8.dp)", ".padding(start = 0.dp, top = 0.dp, end = 8.dp, bottom = 16.dp)")
    
    # fix api call in rememberCardMediaDetail
    ui_text = ui_text.replace("RetrofitClient.tmdbApi.getMovieDetails(idInt, apiKey)", "RetrofitClient.tmdbApi.getMovieDetails(idInt, apiKey, java.util.Locale.getDefault().toLanguageTag())")
    ui_text = ui_text.replace("RetrofitClient.tmdbApi.getSeriesDetails(idInt, apiKey)", "RetrofitClient.tmdbApi.getSeriesDetails(idInt, apiKey, java.util.Locale.getDefault().toLanguageTag())")

    with open(filepath, "w") as f:
        f.write(ui_text)

