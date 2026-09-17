import os
import re

directories = ["app/src/main/java/com/example/ui/screens/home", 
               "app/src/main/java/com/example/ui/screens/movies", 
               "app/src/main/java/com/example/ui/screens/series", 
               "app/src/main/java/com/example/ui/screens/anime",
               "app/src/main/java/com/example/ui/screens/social",
               "app/src/main/java/com/example/ui/screens/share"]

for dirpath in directories:
    if not os.path.exists(dirpath):
        continue
    for filename in os.listdir(dirpath):
        if filename.endswith(".kt"):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, "r") as f:
                content = f.read()
            
            # Replace 400 or 1000 delays with 1200
            content = re.sub(r'kotlinx\.coroutines\.delay\(\d+\)', 'kotlinx.coroutines.delay(1200)', content)
            
            # If it's a media screen, it usually has:
            # if (uiState.isLoading || !transitionFinished) { MediaScreenSkeleton(); return }
            # if (uiState.error != null) { ... return }
            # Replace the error handling with continuous skeleton if empty.
            # Actually, simpler: just show skeleton if error is not null AND lists are empty, or just always skeleton on error.
            error_pattern = r'    if \(uiState\.error != null\) \{\s+Box\(modifier = Modifier\.fillMaxSize\(\), contentAlignment = Alignment\.Center\) \{\s+Text\(.*?\)\s+\}\s+return\s+\}'
            replacement = r'''    if (uiState.error != null && uiState.movies.isEmpty() && uiState.series.isEmpty()) {
        MediaScreenSkeleton()
        return
    }'''
            # A bit safer to just replace error blocks globally where they match
            if "uiState.error != null" in content and "MediaScreenSkeleton" in content:
                content = re.sub(error_pattern, replacement, content, flags=re.DOTALL)
                
                # anime/movies/series might just have uiState.items
                error_pattern_items = r'    if \(uiState\.error != null\) \{\s+Box\(modifier = Modifier\.fillMaxSize\(\), contentAlignment = Alignment\.Center\) \{\s+Text\(.*?\)\s+\}\s+return\s+\}'
                replacement_items = r'''    if (uiState.error != null && uiState.items.isEmpty()) {
        MediaScreenSkeleton()
        return
    }'''
                content = re.sub(error_pattern_items, replacement_items, content, flags=re.DOTALL)
            
            with open(filepath, "w") as f:
                f.write(content)

