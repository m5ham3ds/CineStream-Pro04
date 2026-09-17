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
        
    # Find the function body start
    match = re.search(r'@Composable\s*fun\s+[A-Za-z0-9_]+\s*\(.*?\)\s*\{', c, re.DOTALL)
    if not match:
        continue
    
    start_index = match.end() - 1
    
    # Count braces to find the end of the function
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
        
    # Now extract the function body
    func_body = c[start_index:end_index]
    
    # We want to replace the early returns with Crossfade
    # Pattern to match the two if statements:
    pattern = r'    if \(uiState\.isLoading \|\| !transitionFinished\) \{\s+'+skeleton+r'\(\)\s+return\s+\}\s+if \(uiState\.error != null && '+empty_check+r'\) \{\s+'+skeleton+r'\(\)\s+return\s+\}'
    
    replacement = f'''    val showSkeleton = uiState.isLoading || !transitionFinished || (uiState.error != null && {empty_check})
    androidx.compose.animation.Crossfade(targetState = showSkeleton, animationSpec = androidx.compose.animation.core.tween(800), label = "skeleton_fade") {{ loading ->
        if (loading) {{
            {skeleton}()
        }} else {{'''
        
    new_func_body = re.sub(pattern, replacement, func_body)
    
    # Append the closing brace for Crossfade inside the function body
    # Wait, we need to add '}' at the end of the function body
    if new_func_body != func_body:
        new_func_body = new_func_body + "\n    }"
        
        # Put it all together
        new_c = c[:start_index] + new_func_body + c[end_index:]
        with open(filepath, "w") as f:
            f.write(new_c)
            print(f"Fixed {filepath}")
