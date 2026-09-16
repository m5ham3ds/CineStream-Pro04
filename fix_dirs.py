import os

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt",
    "app/src/main/java/com/example/utils/AndroidDownloader.kt",
    "app/src/main/java/com/example/utils/StreamDownloaderService.kt"
]

for file_path in files_to_fix:
    with open(file_path, "r") as f:
        c = f.read()
    
    # In PlayerViewModel
    if "PlayerViewModel" in file_path:
        c = c.replace(
            """val file = java.io.File(android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES), "CineStream/${fileId}.mp4")""",
            """val file = java.io.File(com.example.CineStreamApp.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${fileId}.mp4")"""
        )
        c = c.replace(
            """val file = java.io.File(android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES), "CineStream/${download.id}.mp4")""",
            """val file = java.io.File(com.example.CineStreamApp.appContext.getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES), "${download.id}.mp4")"""
        )

    if "AndroidDownloader" in file_path:
        c = c.replace(
            """val destFile = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/$fileName")""",
            """val destFile = java.io.File(context.getExternalFilesDir(Environment.DIRECTORY_MOVIES), fileName)"""
        )
        c = c.replace(
            """.setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "CineStream/$fileName")""",
            """.setDestinationInExternalFilesDir(context, Environment.DIRECTORY_MOVIES, fileName)"""
        )
        
    if "StreamDownloaderService" in file_path:
        c = c.replace(
            """val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream")""",
            """val dir = getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies")"""
        )
        c = c.replace(
            """val file = java.io.File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "CineStream/${id}.mp4")""",
            """val file = java.io.File(getExternalFilesDir(Environment.DIRECTORY_MOVIES) ?: File(filesDir, "movies"), "${id}.mp4")"""
        )
        
    with open(file_path, "w") as f:
        f.write(c)

print("Done")
