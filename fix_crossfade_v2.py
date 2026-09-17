import re
import os

files_to_fix = [
    ("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "MediaScreenSkeleton", "uiState.trendingMovies.isEmpty()"),
    ("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "MediaScreenSkeleton", "uiState.movies.isEmpty()"),
    ("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "MediaScreenSkeleton", "uiState.series.isEmpty()"),
    ("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "MediaScreenSkeleton", "uiState.series.isEmpty()"),
]

for filepath, skeleton, empty_check in files_to_fix:
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r") as f:
        c = f.read()
        
    match = re.search(r'@Composable\s*fun\s+[A-Za-z0-9_]+\s*\(.*?\)\s*\{', c, re.DOTALL)
    if not match:
        continue
    
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
                
    if end_index == -1:
        continue
        
    func_body = c[start_index:end_index]
    
    # We can use sub with a more relaxed regex
    p1 = r'if\s*\(\s*uiState\.isLoading\s*\|\|\s*!transitionFinished\s*\)\s*\{\s*'+skeleton+r'\(\)\s*return\s*\}'
    p2 = r'if\s*\(\s*uiState\.error\s*!=\s*null\s*&&\s*'+empty_check.replace('(', r'\(').replace(')', r'\)')+r'\s*\)\s*\{\s*'+skeleton+r'\(\)\s*return\s*\}'
    
    if re.search(p1, func_body) and re.search(p2, func_body):
        func_body = re.sub(p1, '', func_body)
        
        replacement = f'''    val showSkeleton = uiState.isLoading || !transitionFinished || (uiState.error != null && {empty_check})
    androidx.compose.animation.Crossfade(targetState = showSkeleton, animationSpec = androidx.compose.animation.core.tween(800), label = "skeleton_fade") {{ loading ->
        if (loading) {{
            {skeleton}()
        }} else {{'''
        
        func_body = re.sub(p2, replacement, func_body)
        
        func_body = func_body + "\n    }"
        
        new_c = c[:start_index] + func_body + c[end_index:]
        with open(filepath, "w") as f:
            f.write(new_c)
            print(f"Fixed {filepath}")
            
