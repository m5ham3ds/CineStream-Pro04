import os

def update_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)

update_file(
    "app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt",
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${fileId}.mp4")',
    'val file = java.io.File(java.io.File(com.example.MyApplication.appContext.filesDir, "offline_movies"), "${fileId}.mp4")'
)

update_file(
    "app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt",
    'val file = java.io.File(com.example.MyApplication.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${download.id}.mp4")',
    'val file = java.io.File(java.io.File(com.example.MyApplication.appContext.filesDir, "offline_movies"), "${download.id}.mp4")'
)

update_file(
    "app/src/main/java/com/example/utils/StreamDownloaderService.kt",
    'val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")',
    'val dir = File(filesDir, "offline_movies")'
)

update_file(
    "app/src/main/java/com/example/utils/AndroidDownloader.kt",
    'val destFile = java.io.File(context.getExternalFilesDir(Environment.DIRECTORY_MOVIES), fileName)',
    'val dir = java.io.File(context.filesDir, "offline_movies")\n            if (!dir.exists()) dir.mkdirs()\n            val destFile = java.io.File(dir, fileName)'
)

print("Done")
