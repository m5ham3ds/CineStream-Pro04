with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    lines = f.readlines()

# Remove the bad '-e' stuff at the very end
while lines and ('-e' in lines[-1] or lines[-1].strip() in (')', '}', '')):
    lines.pop()

text = "".join(lines)

if "val bottomBarRoutes =" not in text:
    # insert it before hasTopBar
    bottomBar = "    val bottomBarRoutes = listOf(Screen.Home.route, Screen.Library.route, Screen.Search.route, Screen.Extensions.route, Screen.Social.route)\n"
    text = text.replace("    val hasTopBar =", bottomBar + "    val hasTopBar =")

if "val navHostModifier =" not in text:
    navhost = """    val navHostModifier = if (hasTopBar) {
        Modifier.padding(bottom = 80.dp)
    } else {
        Modifier
    }
"""
    # The Scaffold block probably has innerPadding
    text = text.replace("Scaffold(", "Scaffold(\n")
    # Where does Scaffold end? Before NavHost. Wait.
    # I'll just write it manually

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(text)
