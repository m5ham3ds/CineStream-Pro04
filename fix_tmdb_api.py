import re

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    text = f.read()

# Add language parameter to all endpoints
# Replace: @Query("api_key") apiKey: String
# With: @Query("api_key") apiKey: String, @Query("language") language: String
text = re.sub(r'@Query\("api_key"\) apiKey: String(\s*\))', r'@Query("api_key") apiKey: String,\n        @Query("language") language: String\1', text)
text = re.sub(r'@Query\("api_key"\) apiKey: String(\s*,)', r'@Query("api_key") apiKey: String,\n        @Query("language") language: String\1', text)

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(text)
