with open("app/src/main/java/com/example/data/remote/RetrofitClient.kt", "r") as f:
    text = f.read()

# Fix the language code to be just 'ar'
text = text.replace('val tmdbLanguage = if (currentLanguage == "ar") "ar-SA" else "en-US"', 'val tmdbLanguage = if (currentLanguage == "ar") "ar" else "en-US"')

# Fix the aggressive 7-day cache to be just 1 hour
text = text.replace('.header("Cache-Control", "public, max-age=" + 60 * 60 * 24 * 7) // Cache for 7 days', '.header("Cache-Control", "public, max-age=" + 60 * 60) // Cache for 1 hour')

with open("app/src/main/java/com/example/data/remote/RetrofitClient.kt", "w") as f:
    f.write(text)
