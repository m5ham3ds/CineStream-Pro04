import re

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "r") as f:
    original = f.read()

new_content = original.replace("enableAutomaticInitialization = false", "layoutParams = android.view.ViewGroup.LayoutParams(android.view.ViewGroup.LayoutParams.MATCH_PARENT, android.view.ViewGroup.LayoutParams.MATCH_PARENT)\n                    enableAutomaticInitialization = false")

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(new_content)
