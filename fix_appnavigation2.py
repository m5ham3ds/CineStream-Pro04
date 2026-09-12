import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

old_topbar = """                            androidx.compose.material3.IconButton(
                                onClick = { scope.launch { drawerState.open() } }
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Menu,
                                    contentDescription = "Menu"
                                )
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onBackground)
                                    .clickable {
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
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.background)
                                }
                            }
                            
                            if (!isSearchExpanded) {
                                Spacer(modifier = Modifier.weight(1f))
                                val titleRes = when(currentRoute) {
                                    Screen.Home.route -> R.string.app_name
                                    Screen.Movies.route -> R.string.movies
                                    Screen.Series.route -> R.string.series
                                    Screen.Anime.route -> R.string.anime
                                    Screen.Search.route -> R.string.search
                                    Screen.Profile.route -> R.string.profile
                                    Screen.Settings.route -> R.string.settings
                                    Screen.Downloads.route -> R.string.downloads
                                    Screen.About.route -> R.string.about
                                    Screen.Extensions.route -> R.string.extensions
                                    Screen.Share.route -> R.string.share
                                    Screen.Social.route -> R.string.social
                                    else -> R.string.app_name
                                }
                                Text(
                                    text = stringResource(id = titleRes),
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onBackground
                                )
                                Spacer(modifier = Modifier.weight(1f))
                            }"""

new_topbar = """                            androidx.compose.material3.IconButton(
                                onClick = { scope.launch { drawerState.open() } }
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Menu,
                                    contentDescription = "Menu"
                                )
                            }
                            
                            if (!isSearchExpanded) {
                                Spacer(modifier = Modifier.width(16.dp))
                                val titleRes = when(currentRoute) {
                                    Screen.Home.route -> R.string.app_name
                                    Screen.Movies.route -> R.string.movies
                                    Screen.Series.route -> R.string.series
                                    Screen.Anime.route -> R.string.anime
                                    Screen.Search.route -> R.string.search
                                    Screen.Profile.route -> R.string.profile
                                    Screen.Settings.route -> R.string.settings
                                    Screen.Downloads.route -> R.string.downloads
                                    Screen.About.route -> R.string.about
                                    Screen.Extensions.route -> R.string.extensions
                                    Screen.Share.route -> R.string.share
                                    Screen.Social.route -> R.string.social
                                    else -> R.string.app_name
                                }
                                Text(
                                    text = stringResource(id = titleRes),
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onBackground
                                )
                                Spacer(modifier = Modifier.weight(1f))
                            } else {
                                Spacer(modifier = Modifier.weight(1f))
                            }
                            
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onBackground)
                                    .clickable {
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
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.background)
                                }
                            }"""

if old_topbar in text:
    text = text.replace(old_topbar, new_topbar)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Fixed TopBar layout!")
else:
    print("Could not find old_topbar.")
