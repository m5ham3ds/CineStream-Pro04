import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        c = f.read()

    # Find where the main function ends by looking at the first @Composable after our Crossfade,
    # or the end of the file.
    crossfade_match = re.search(r'Crossfade\(targetState =', c)
    if not crossfade_match:
        print(f"No Crossfade in {filepath}")
        return

    # For these specific files, we know the exact text is "    }\n}" before the next function or EOF.
    
    # Let's find the first "    }\n}" after the Crossfade block
    # But wait, there might be other matches?
    # Actually, it's safer to find the match that's before `private fun` or `@Composable` or EOF.
    
    # Find next function
    next_func = re.search(r'\n(private |@Composable)?\s*fun ', c[crossfade_match.end():])
    if next_func:
        end_search_index = crossfade_match.end() + next_func.start()
    else:
        end_search_index = len(c)
        
    last_braces = c.rfind("    }\n}", crossfade_match.end(), end_search_index)
    if last_braces != -1:
        c = c[:last_braces] + "        }\n    }\n}" + c[last_braces+6:]
        with open(filepath, "w") as f:
            f.write(c)
        print(f"Fixed {filepath}")
    else:
        print(f"Could not find closing braces for {filepath}")

files = [
    "app/src/main/java/com/example/ui/screens/about/AboutScreen.kt",
    "app/src/main/java/com/example/ui/screens/social/SocialScreen.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
]

for f in files:
    fix_file(f)

