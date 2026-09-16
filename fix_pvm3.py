with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    c = f.read()

c = c.replace(
    'val file = java.io.File("com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES)?.absolutePath + "/${fileId}.mp4")',
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${fileId}.mp4")'
)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(c)

