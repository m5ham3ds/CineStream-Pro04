import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

broken_part = """                        ) {
                                            navController.navigate(Screen.Profile.route)
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {"""

fixed_part = """                        ) {
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onBackground)
                                    .clickable {
                                        navController.navigate(Screen.Profile.route)
                                    },
                                contentAlignment = Alignment.Center
                            ) {"""

if broken_part in text:
    text = text.replace(broken_part, fixed_part)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Fixed!")
else:
    print("Could not find broken part.")
