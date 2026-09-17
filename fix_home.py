with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f: c = f.read()
# Replace the bad brace block before SectionTitle
# We have:
#        }
#    }
#        }
#    }
#}}
# @Composable
# fun SectionTitle

c = c.replace("        }\n    }\n        }\n    }\n}}", "        }\n    }\n}")
# Let's just use re.sub for any sequence of 4 or more braces before @Composable
import re
c = re.sub(r'(\s+\})+\n@Composable\nfun SectionTitle', '\n    }\n}\n\n@Composable\nfun SectionTitle', c)

# Add missing brace at end if needed
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f: f.write(c)
