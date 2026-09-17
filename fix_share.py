import re
with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "r") as f:
    c = f.read()

target = r'    if \(!transitionFinished\) \{\s+com\.example\.ui\.components\.ShareScreenSkeleton\(\)\s+return\s+\}'
replacement = r'''    androidx.compose.animation.Crossfade(targetState = !transitionFinished, animationSpec = androidx.compose.animation.core.tween(800), label = "fade") { loading ->
        if (loading) {
            com.example.ui.components.ShareScreenSkeleton()
        } else {'''

c = re.sub(target, replacement, c)

match = re.search(r'@Composable\s*fun\s+ShareScreen\s*\(.*?\)\s*\{', c, re.DOTALL)
start_index = match.end() - 1

brace_count = 0
end_index = -1
for i in range(start_index, len(c)):
    if c[i] == '{':
        brace_count += 1
    elif c[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end_index = i
            break

c = c[:end_index] + "\n    }\n" + c[end_index:]
with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "w") as f:
    f.write(c)
