with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# For MovieDetailsScreen, the end is before SeriesDetailsScreen
import re
match = re.search(r'\n(        \}\n    \}\n\})(\n\n@Composable\nfun SeriesDetailsScreen)', c)
if match:
    c = c[:match.start(1)] + "            }\n" + match.group(1) + match.group(2) + c[match.end():]
else:
    print("Could not find end of MovieDetailsScreen")

match = re.search(r'\n(            \}\n        \}\n    \}\n\})(\n@Composable\nfun AnimatedDownloadIcon)', c)
if match:
    # wait, the grep showed:
    # 925-            }$
    # 926-        }$
    # 927-    }$
    # 928-}$
    # Let's replace the whole block
    pass

# safer replacement for SeriesDetailsScreen:
match = re.search(r'\n            \}\n        \}\n    \}\n\}(\n@Composable\nfun AnimatedDownloadIcon)', c)
if match:
    # Add two closing braces: '            }\n        }\n'
    c = c[:match.start(1)-18] + "                }\n            }\n            }\n        }\n    }\n}" + match.group(1) + c[match.end():]
else:
    print("Could not find end of SeriesDetailsScreen")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

