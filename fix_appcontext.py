with open("app/src/main/java/com/example/MyApplication.kt", "r") as f:
    c = f.read()

if "appContext" not in c:
    c = c.replace("class MyApplication : Application() {", "class MyApplication : Application() {\n    companion object {\n        lateinit var appContext: android.content.Context\n    }\n\n    override fun onCreate() {\n        super.onCreate()\n        appContext = applicationContext\n")
    with open("app/src/main/java/com/example/MyApplication.kt", "w") as f:
        f.write(c)

# Fix PlayerViewModel back to use MyApplication.appContext
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    c = f.read()

c = c.replace("com.example.CineStreamApp.appContext", "com.example.MyApplication.appContext")
c = c.replace("/sdcard/Android/data/com.aistudio.cinestream/files/Movies/", 'com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)?.absolutePath + "/')

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(c)
