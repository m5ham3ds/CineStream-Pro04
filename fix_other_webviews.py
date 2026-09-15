import re

files_to_fix = [
    "app/src/main/java/com/example/ui/components/BackgroundWebView.kt",
    "app/src/main/java/com/example/ui/components/YouTubePlayer.kt",
    "app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt"
]

for file_path in files_to_fix:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        old_update = "update = { webView ->"
        new_update = """onRelease = { webView ->
            webView.stopLoading()
            webView.destroy()
        },
        update = { webView ->"""
        
        if old_update in content:
            content = content.replace(old_update, new_update)
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Replaced successfully in {file_path}!")
        else:
            print(f"Could not find update block in {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

