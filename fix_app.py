with open("app/src/main/java/com/example/MyApplication.kt", "r") as f:
    c = f.read()

if "companion object {" not in c:
    c = c.replace("class MyApplication : Application(), ImageLoaderFactory {", "class MyApplication : Application(), ImageLoaderFactory {\n    companion object {\n        lateinit var appContext: android.content.Context\n    }\n")
    c = c.replace("super.onCreate()", "super.onCreate()\n        appContext = applicationContext\n")
    with open("app/src/main/java/com/example/MyApplication.kt", "w") as f:
        f.write(c)
