import re
with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "r") as f:
    c = f.read()

target = r'    if \(!transitionFinished\) \{\s+com\.example\.ui\.components\.AboutScreenSkeleton\(\)\s+return\s+\}'
replacement = r'''    androidx.compose.animation.Crossfade(targetState = !transitionFinished, animationSpec = androidx.compose.animation.core.tween(800), label = "fade") { loading ->
        if (loading) {
            com.example.ui.components.AboutScreenSkeleton()
        } else {'''

c = re.sub(target, replacement, c)
c += "\n    }\n"
with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "w") as f:
    f.write(c)
