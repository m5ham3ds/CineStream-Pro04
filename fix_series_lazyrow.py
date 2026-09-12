with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "r") as f:
    content = f.read()

target = """                    }
                }
            }
            }
        if (selectedCategory == "Series") {"""

replacement = """                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
        if (selectedCategory == "Series") {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "w") as f:
    f.write(content)
