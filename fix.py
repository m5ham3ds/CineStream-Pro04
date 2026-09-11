import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

# Find the LaunchedEffect
start_marker = "updateFinishedShowGreen = false\n        }\n    }"
start_idx = text.find(start_marker) + len(start_marker)

# Find the Column
end_marker = "Column(modifier = Modifier.weight(1f).verticalScroll(androidx.compose.foundation.rememberScrollState())) {"
end_idx = text.find(end_marker)

replacement = """
    val hasTopBar = bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(
        Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, Screen.Extensions.route, Screen.Share.route, Screen.About.route, Screen.Social.route
    )

    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl) {
    ModalNavigationDrawer(
        drawerState = drawerState,
        gesturesEnabled = drawerState.isOpen,
        drawerContent = {
            ModalDrawerSheet(
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                modifier = Modifier.width(300.dp)
            ) {
                // Top Header Section
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .background(
                            brush = Brush.verticalGradient(
                                colors = listOf(MaterialTheme.colorScheme.surfaceVariant, MaterialTheme.colorScheme.surface)
                            )
                        )
                        .padding(16.dp)
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Bottom
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                val displayName = if (isGuest || currentUser == null) "Guest User" else {
                                    "${currentUser?.firstName ?: ""} ${currentUser?.lastName ?: ""}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                                }
                                Text(
                                    text = displayName,
                                    fontSize = 24.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                if (!isGuest && currentUser?.username?.isNotBlank() == true) {
                                    Text(
                                        text = "@${currentUser?.username}",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    if (!isGuest) {
                                        Icon(painter = painterResource(android.R.drawable.ic_dialog_info), contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                        Spacer(modifier = Modifier.width(4.dp))
                                    }
                                    Text(
                                        text = if (isGuest) "Free Account" else "Premium User",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                            
                            Box(
                                modifier = Modifier
                                    .size(60.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f))
                                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                    .clickable { 
                                        scope.launch { drawerState.close() }
                                        navController.navigate(Screen.Profile.route)
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                if (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true) {
                                    AsyncImage(
                                        model = currentUser?.photoUrl,
                                        contentDescription = "Avatar",
                                        contentScale = ContentScale.Crop,
                                        modifier = Modifier.fillMaxSize()
                                    )
                                } else {
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
                                }
                            }
                        }
                    }
                }
                
                """

new_text = text[:start_idx] + replacement + text[end_idx:]

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(new_text)

