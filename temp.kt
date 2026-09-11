    
    var isSearchExpanded by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
    var searchQuery by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var showLogoutDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

    var isUpdatingData by remember { mutableStateOf(com.example.utils.NetworkUtils.isInternetAvailable(context)) }
    var updateFinishedShowGreen by remember { mutableStateOf(false) }
    
    androidx.compose.runtime.LaunchedEffect(updateFinishedShowGreen) {
        if (updateFinishedShowGreen) {
            kotlinx.coroutines.delay(2000)
            isUpdatingData = false
            updateFinishedShowGreen = false
        }
    }
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
                
                Column(modifier = Modifier.weight(1f).verticalScroll(androidx.compose.foundation.rememberScrollState())) {
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Home, contentDescription = null, tint = if (currentRoute == Screen.Home.route) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onBackground) },
                        label = { Text(stringResource(R.string.home), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Home.route,
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent
                        ),
                        shape = RoundedCornerShape(16.dp),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Home.route) {
                                navController.popBackStack(Screen.Home.route, inclusive = true)
                                navController.navigate(Screen.Home.route)
                            } else {
                                navController.navigate(Screen.Home.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Favorite, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.library), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Library.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute == Screen.Library.route) {
                                navController.popBackStack(Screen.Library.route, inclusive = true)
                                navController.navigate(Screen.Library.route)
                            } else {
                                navController.navigate(Screen.Library.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text("الإضافات", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Extensions.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.Extensions.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text("Community", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Social.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.Social.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Share, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text("Offline Share", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Share.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.Share.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.settings), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Settings.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.Settings.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Download, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.downloads), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Downloads.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.Downloads.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Info, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.about_app), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.About.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            navController.navigate(Screen.About.route) {
                                popUpTo(navController.graph.startDestinationId) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(Icons.AutoMirrored.Filled.Help, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text(stringResource(R.string.help_support), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = false,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = { scope.launch { drawerState.close() } },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                }
                
                HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))

                                    scope.launch { drawerState.close() }
                                    showLogoutDialog = true
                                }
                            }
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) stringResource(R.string.login) else stringResource(R.string.logout), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    ) {
        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
        if (showLogoutDialog) {
            AlertDialog(
                onDismissRequest = { showLogoutDialog = false },
                title = { Text(stringResource(R.string.logout)) },
                text = { Text(stringResource(R.string.logout_confirm)) },
                confirmButton = {
                    TextButton(onClick = {
                        showLogoutDialog = false
                        scope.launch { 
                            userPrefs.saveIsGuest(true)
                            userPrefs.saveIsLoggedIn(false)
                        }
                        authViewModel.signOut()
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    }) { Text(stringResource(R.string.yes), color = Color.Red) }
                },
                dismissButton = {
                    TextButton(onClick = { showLogoutDialog = false }) { Text(stringResource(R.string.no), color = MaterialTheme.colorScheme.onSurface) }
                },
                containerColor = MaterialTheme.colorScheme.surface,
                titleContentColor = MaterialTheme.colorScheme.onSurface,
                textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Scaffold(
            containerColor = MaterialTheme.colorScheme.background,
            topBar = {
                Column {
                    if (hasTopBar) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .windowInsetsPadding(WindowInsets.statusBars)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                                            navController.navigate(Screen.Profile.route)
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                if (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true) {
