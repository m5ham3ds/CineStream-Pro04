with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

# I want to insert } and Spacer after the items block closes.
# The text is:
#                     }
#                 }
#             }
#         if (selectedCategory == animeStr) {

target = """                    }
                }
            }
        if (selectedCategory == animeStr) {"""

replacement = """                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
        if (selectedCategory == animeStr) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)
