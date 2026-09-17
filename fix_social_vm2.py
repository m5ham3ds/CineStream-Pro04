import re

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "r") as f:
    c = f.read()

target = """                } else {
                    _currentUser.value = null
                    stopListening()
                }"""

replacement = """                } else {
                    _currentUser.value = null
                    _isLoading.value = false
                    stopListening()
                }"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/social/SocialViewModel.kt", "w") as f:
    f.write(c)

