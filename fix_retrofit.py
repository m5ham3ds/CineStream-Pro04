import re

file_path = "app/src/main/java/com/example/data/remote/RetrofitClient.kt"
with open(file_path, "r") as f:
    content = f.read()

target = """            .addInterceptor { chain ->
                var request = chain.request()"""

replacement = """            .addInterceptor { chain ->
                val originalRequest = chain.request()
                val originalUrl = originalRequest.url
                
                val currentLanguage = java.util.Locale.getDefault().language
                val tmdbLanguage = if (currentLanguage == "ar") "ar-SA" else "en-US"
                
                val urlWithLanguage = originalUrl.newBuilder()
                    .addQueryParameter("language", tmdbLanguage)
                    .build()
                
                var request = originalRequest.newBuilder().url(urlWithLanguage).build()"""

content = content.replace(target, replacement)
with open(file_path, "w") as f:
    f.write(content)
