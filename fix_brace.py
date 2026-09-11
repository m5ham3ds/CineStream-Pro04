with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace(
"""                }
            },
            bottomBar = {""",
"""                }
                }
            },
            bottomBar = {"""
)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(text)
