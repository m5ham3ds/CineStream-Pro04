import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    c = f.read()

target = """                val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${fileId}.mp4")"""
replace = """                val ctx = com.example.MyApplication.appContext
                val file = java.io.File(ctx.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES) ?: java.io.File(ctx.filesDir, "movies"), "${fileId}.mp4")"""
c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(c)

