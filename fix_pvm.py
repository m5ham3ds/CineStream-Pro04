with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    c = f.read()

# I wrote: val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)?.absolutePath + "/${fileId}.mp4")
# wait, previously it was: val file = java.io.File("/sdcard/Android/data/com.aistudio.cinestream/files/Movies/${fileId}.mp4")
# But I replaced the string literal "/sdcard/..." with something that broke the syntax.

c = c.replace(
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)?.absolutePath + "/${fileId}.mp4")',
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${fileId}.mp4")'
)

c = c.replace(
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)?.absolutePath + "/${download.id}.mp4")',
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${download.id}.mp4")'
)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(c)

