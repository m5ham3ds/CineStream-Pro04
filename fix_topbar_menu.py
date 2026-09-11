import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

broken_part = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box("""

fixed_part = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            androidx.compose.material3.IconButton(
                                onClick = {
                                    if (currentRoute == Screen.Home.route) {
                                        scope.launch { drawerState.open() }
                                    } else {
                                        navController.navigate(Screen.Home.route) {
                                            popUpTo(navController.graph.startDestinationId) { inclusive = true }
                                            launchSingleTop = true
                                        }
                                    }
                                }
                            ) {
                                Icon(
                                    imageVector = if (currentRoute == Screen.Home.route) Icons.Default.Menu else Icons.AutoMirrored.Filled.ArrowBack,
                                    contentDescription = "Menu/Back"
                                )
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Box("""

if broken_part in text:
    text = text.replace(broken_part, fixed_part)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Injected Menu Icon!")
else:
    print("Could not find broken part.")
