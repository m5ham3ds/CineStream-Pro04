import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

start_idx = text.find("if (isSearchExpanded) {")
# search for NavHost
end_idx = text.find("NavHost(\n                navController = navController,", start_idx)

if start_idx != -1 and end_idx != -1:
    old_part = text[start_idx:end_idx]
    # find where ExpandableSearchBar ends:
    search_bar_end = old_part.find(")\n") + 2
    fixed_part = old_part[:search_bar_end] + """                            }
                        }
                    }
                }
            },
            bottomBar = {
                if (hasTopBar) {
                    com.example.ui.components.BottomNavBar(navController = navController, currentRoute = currentRoute)
                }
            }
        ) { innerPadding ->
            val navHostModifier = if (hasTopBar) {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding)
            } else {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding).then(Modifier.windowInsetsPadding(WindowInsets.statusBars).consumeWindowInsets(WindowInsets.statusBars))
            }
            """
    
    new_text = text[:start_idx] + fixed_part + text[end_idx:]
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(new_text)
    print("Fixed Scaffold!")
else:
    print("Failed to find boundaries.")
