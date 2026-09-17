import re
with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    c = f.read()

target = r'    if \(isLoading \|\| !transitionFinished\) \{\s+com\.example\.ui\.components\.SocialScreenSkeleton\(\)\s+return\s+\}'
replacement = r'''    androidx.compose.animation.Crossfade(targetState = isLoading || !transitionFinished, animationSpec = androidx.compose.animation.core.tween(800), label = "fade") { loading ->
        if (loading) {
            com.example.ui.components.SocialScreenSkeleton()
        } else {'''

c = re.sub(target, replacement, c)

# find end of SocialScreen
match = re.search(r'@Composable\s*fun\s+SocialScreen\s*\(.*?\)\s*\{', c, re.DOTALL)
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
with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(c)
