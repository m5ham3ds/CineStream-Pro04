import re
with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

# Add onRelease to the AndroidView in VideoExtractor.kt
old_update = """        update = { webView ->"""
new_update = """        onRelease = { webView ->
            webView.stopLoading()
            webView.destroy()
        },
        update = { webView ->"""

if old_update in content:
    content = content.replace(old_update, new_update)
    with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find the block to replace!")
