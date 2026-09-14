import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    text = f.read()

# 1. Add currentAppLayoutDirection and LTR wrapper before ModalNavigationDrawer
text = text.replace("    ModalNavigationDrawer(", "    val currentAppLayoutDirection = LocalLayoutDirection.current\n    CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {\n    ModalNavigationDrawer(")

# 2. Add current wrapper before Scaffold
text = text.replace("        Scaffold(", "        CompositionLocalProvider(LocalLayoutDirection provides currentAppLayoutDirection) {\n        Scaffold(")

# 3. Add closing braces at the end
# The end is currently:
# 1067	            }
# 1068	        }
# 1069	    }
# 1070	    }
# Let's just append two closing braces before the last brace of the MainScreen function.
text = text.rstrip()
if text.endswith("}"):
    text = text[:-1] + "    }\n    }\n}"

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(text)

