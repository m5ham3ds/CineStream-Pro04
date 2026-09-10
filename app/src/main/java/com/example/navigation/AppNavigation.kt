package com.example.navigation
import com.example.utils.SiteVerificationManager

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*

import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.outlined.Share

import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ExitToApp
import androidx.compose.material.icons.automirrored.filled.Help
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material3.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

import androidx.compose.ui.platform.LocalContext

import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.screens.auth.AuthViewModel
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale

import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import com.example.ui.components.BackgroundWebView
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import android.widget.Toast
import kotlinx.coroutines.launch
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import java.net.URLDecoder
import java.net.URLEncoder
import com.example.ui.components.BottomNavBar
import com.example.ui.components.ExpandableSearchBar
import com.example.ui.screens.details.MovieDetailsScreen
import com.example.ui.screens.details.SeriesDetailsScreen
import com.example.ui.screens.home.HomeScreen
import com.example.ui.screens.anime.AnimeScreen
import com.example.ui.screens.home.PopularScreen
import com.example.ui.screens.home.NewReleasesScreen
import com.example.ui.screens.home.UpcomingScreen
import com.example.ui.screens.home.TrendingScreen
import com.example.ui.screens.home.WatchingScreen
import com.example.ui.screens.library.LibraryScreen
import com.example.ui.screens.movies.MoviesScreen
import com.example.ui.screens.search.SearchScreen
import com.example.ui.screens.series.SeriesScreen
import com.example.ui.screens.player.PlayerScreen
import com.example.ui.screens.splash.SplashScreen
import com.example.ui.screens.onboarding.OnboardingScreen
import com.example.ui.screens.profile.ProfileScreen
import com.example.ui.screens.profile.SecurityScreen
import com.example.ui.screens.profile.SubscriptionScreen
import com.example.ui.screens.profile.EditProfileScreen
import com.example.ui.screens.profile.PublicProfileScreen
import com.example.ui.screens.downloads.DownloadsScreen
import com.example.ui.screens.settings.SettingsScreen

import com.example.ui.screens.social.SocialScreen
import com.example.ui.screens.social.ChatScreen
import com.example.ui.screens.share.ShareScreen

import com.example.ui.screens.about.AboutScreen
import com.example.ui.screens.auth.AuthScreen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route ?: Screen.Splash.route

    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    
    val authViewModel: AuthViewModel = viewModel()
    val currentUser by authViewModel.currentUser.collectAsState()
    val userPrefs = remember { com.example.data.repository.UserPreferencesRepository(context) }
    val isGuest by userPrefs.isGuest.collectAsState(initial = false)
    
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
    
    
    val extensionUrls = remember { 
        listOf(
            "https://tv10.egydead.live/", "https://vidsrc.me/", "https://multiembed.mov/", "https://vidsrc.to/",
            "https://egydead.icu/", "https://faselhd.club/", "https://anime4up.com/",
            "https://witanime.com/", "https://cimaleek.com/", "https://asia2tv.cc/",
            "https://tuktukcinema.net/", "https://arabseed-tv.com/", "https://www.arabseed.wine/",
            "https://e.cimalight.co/", "https://egybests.live/", "https://www.stardima.com/",
            "https://a.qfilm.tv/", "https://egydead.rip/", "https://mycima.red/", 
            "https://witanime.you/", "https://animesit.com/"
        )
    }
    val bottomBarRoutes = listOf(
        Screen.Home.route,
        Screen.Movies.route,
        Screen.Series.route,
        Screen.Search.route,
        Screen.Library.route,
        Screen.Anime.route
    )
    
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
                // Top Header Section with Gradient
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
                        verticalArrangement = Arrangement.Top
                    ) {
                        Text(
                            text = "CineStream",
                            style = MaterialTheme.typography.headlineMedium.copy(
                                fontWeight = FontWeight.Bold,
                                fontFamily = FontFamily.Serif
                            ),
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = TextAlign.Start
                        )
                        Spacer(modifier = Modifier.weight(1f))
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.clickable {
                                scope.launch { drawerState.close() }
                                if (isGuest) {
                                    navController.navigate(Screen.Auth.route)
                                } else {
                                    navController.navigate(Screen.Profile.route)
                                }
                            }
                        ) {
                            Column {
                                val displayName = if (isGuest || currentUser == null) "Guest User" else {
                                    "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                                }
                                Text(
                                    text = displayName,
                                    fontSize = 24.sp,
                                    fontFamily = FontFamily.SansSerif,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                if (!isGuest && currentUser?.username?.isNotBlank() == true) {
                                    Text(
                                        text = "@${currentUser?.username}",
                                        fontSize = 14.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
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
                            Spacer(modifier = Modifier.weight(1f))
                            Box(
                                modifier = Modifier
                                    .size(70.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                if (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true) {
                                    AsyncImage(
                                        model = currentUser?.photoUrl,
                                        contentDescription = "Avatar",
                                        contentScale = ContentScale.Crop,
                                        modifier = Modifier.fillMaxSize()
                                    )
                                } else if (currentUser != null) {
                                    Text(
                                        text = (currentUser?.firstName?.take(1) ?: currentUser?.username?.take(1) ?: "U").uppercase(),
                                        color = MaterialTheme.colorScheme.onSurface,
                                        fontSize = 28.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                } else {
                                    Icon(Icons.Default.Person, contentDescription = "Avatar", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(40.dp))
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
                            if (currentRoute != Screen.Extensions.route) {
                                navController.navigate(Screen.Extensions.route)
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
                            if (currentRoute == Screen.Settings.route) {
                                navController.popBackStack(Screen.Settings.route, inclusive = true)
                                navController.navigate(Screen.Settings.route)
                            } else {
                                navController.navigate(Screen.Settings.route)
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
                            if (currentRoute != Screen.Social.route) {
                                navController.navigate(Screen.Social.route)
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
                            if (currentRoute == Screen.Downloads.route) {
                                navController.popBackStack(Screen.Downloads.route, inclusive = true)
                                navController.navigate(Screen.Downloads.route)
                            } else {
                                navController.navigate(Screen.Downloads.route)
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
                            if (currentRoute != Screen.Share.route) {
                                navController.navigate(Screen.Share.route)
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
                            if (currentRoute == Screen.About.route) {
                                navController.popBackStack(Screen.About.route, inclusive = true)
                                navController.navigate(Screen.About.route)
                            } else {
                                navController.navigate(Screen.About.route)
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

                // Bottom Area (Logout)// Bottom Area (Logout)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surface)
                            .clickable { 
                                if (isGuest) {
                                    scope.launch { drawerState.close() }
                                    navController.navigate(Screen.Auth.route)
                                } else {
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
                            // Avatar on left
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.onSurfaceVariant)
                                    .clickable {
                                         if (isGuest) {
                                            navController.navigate(Screen.Auth.route)
                                        } else {
                                            navController.navigate(Screen.Profile.route)
                                        }
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
                                                            
                                                            // Center App Name
                                                            Text(
                                                                "CineStream",
                                                                fontWeight = FontWeight.Bold,
                                                                color = MaterialTheme.colorScheme.primary, // Red
                                                                fontSize = 22.sp
                                                            )
                                                            
                                                            Spacer(modifier = Modifier.weight(1f))
                            } else {
                                Spacer(modifier = Modifier.width(16.dp))
                            }
    
                            
                            
                            if (isSearchExpanded) {
                                ExpandableSearchBar(
                                    isExpanded = isSearchExpanded,
                                    onExpandedChange = { isSearchExpanded = it },
                                    onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.MovieDetails.createRoute(id)) },
                                    onSeriesClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                                )
                            } else {
                                // Right Icons
                                Icon(Icons.Default.Search, contentDescription = "Search", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(24.dp).clickable { isSearchExpanded = true })
                                Spacer(modifier = Modifier.width(16.dp))
                                BadgedBox(
                                    badge = {
                                        Badge(
                                            containerColor = MaterialTheme.colorScheme.primary, // Red badge
                                            contentColor = MaterialTheme.colorScheme.onPrimary,
                                            modifier = Modifier.offset(x = (-4).dp, y = 4.dp)
                                        ) {
                                            Text("1")
                                        }
                                    }
                                ) {
                                    Icon(Icons.Outlined.Notifications, contentDescription = "Notifications", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(24.dp))
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Icon(Icons.Default.Menu, contentDescription = "Menu", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(24.dp).clickable { scope.launch { drawerState.open() } })
                            }

                        }
                        
                        
                    }
                }
                }
            },
            bottomBar = {
                androidx.compose.foundation.layout.Column {
                    if (currentRoute != null && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
                        if (!currentRoute.contains("movie_details") && !currentRoute.contains("series_details") && !currentRoute.contains("player") && !currentRoute.contains("trailer")) {
                            com.example.ui.components.StartAppBanner()
                        }
                    }
                    if (bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(Screen.Extensions.route, Screen.Share.route)) {
                        BottomNavBar(navController = navController)
                    }
                }
            }
        
        ) { innerPadding ->
            val isFullScreen = currentRoute.contains("player") || currentRoute.contains("trailer") || currentRoute == Screen.Splash.route
            val navHostModifier = if (isFullScreen) {
                Modifier
            } else {
                Modifier.padding(innerPadding)
                    .consumeWindowInsets(innerPadding)
                    .then(
                    if (!hasTopBar) Modifier.windowInsetsPadding(WindowInsets.statusBars).consumeWindowInsets(WindowInsets.statusBars) else Modifier
                )
            }

            NavHost(
                navController = navController,
                startDestination = Screen.Splash.route,
                modifier = navHostModifier,
                enterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                exitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) },
                popEnterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                popExitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) }
            ) {
                composable(Screen.Splash.route) {
                    SplashScreen(
                        onNavigateToOnboarding = {
                            navController.navigate(Screen.Onboarding.route) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        },
                        onNavigateToAuth = {
                            navController.navigate(Screen.Auth.route) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        },
                        onNavigateToMain = { startRoute ->
                            navController.navigate(startRoute) {
                                popUpTo(Screen.Splash.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Onboarding.route) {
                    OnboardingScreen(
                        onComplete = {
                            navController.navigate(Screen.Auth.route) {
                                popUpTo(Screen.Onboarding.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Auth.route) {
                    AuthScreen(
                        onSkip = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Auth.route) { inclusive = true }
                            }
                        },
                        onAuthSuccess = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Auth.route) { inclusive = true }
                            }
                        }
                    )
                }
                composable(Screen.Home.route) {
                    HomeScreen(
                        onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onSeriesClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) },
                        onNavigateToUpcoming = { navController.navigate(Screen.Upcoming.route) },
                        onNavigateToAnime = { navController.navigate(Screen.Anime.route) }
                    )
                }
                composable(Screen.Movies.route) {
                    MoviesScreen(
                        onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.MovieDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }
                        composable(Screen.Anime.route) {
            AnimeScreen(
                onAnimeClick = { seriesId ->
                    com.example.utils.AdManager.showInterstitial(context)
                    navController.navigate(Screen.SeriesDetails.createRoute(seriesId))
                },
                onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) },
                onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                onNavigateToWatching = { navController.navigate(Screen.Watching.route) }
            )
        }
        composable(Screen.Series.route) {
                    SeriesScreen(
                        onSeriesClick = {  id -> com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.SeriesDetails.createRoute(id)) },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) },
                        onNavigateToWatching = { navController.navigate(Screen.Watching.route) },
                        onNavigateToPopular = { navController.navigate(Screen.Popular.route) },
                        onNavigateToNewReleases = { navController.navigate(Screen.NewReleases.route) }
                    )
                }
                composable(Screen.Search.route) {
                    SearchScreen(
                        onMediaClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onNavigateToTrending = { navController.navigate(Screen.Trending.route) }
                    )
                }
                composable(Screen.Library.route) {
                    LibraryScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    )
                }
                            composable(Screen.Profile.route) {
                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    },
                    onNavigateToEditProfile = {
                        navController.navigate(Screen.EditProfile.route)
                    },
                    onNavigateToSecurity = {
                        navController.navigate(Screen.Security.route)
                    },
                    onNavigateToSubscription = {
                        navController.navigate(Screen.Subscription.route)
                    },
                    onNavigateToSettings = {
                        navController.navigate(Screen.Settings.route)
                    }
                )
            }
            composable(Screen.EditProfile.route) {
                com.example.ui.screens.profile.EditProfileScreen(
                    onBack = { navController.popBackStack() }
                )
            }
            
            composable(Screen.PublicProfile.route) { backStackEntry ->
                val userId = backStackEntry.arguments?.getString("userId") ?: return@composable
                PublicProfileScreen(
                    userId = userId,
                    onBack = { navController.popBackStack() }
                )
            }
                composable(Screen.Downloads.route) { 
                    DownloadsScreen(
                        onNavigateToHome = {
                            navController.navigate(Screen.Home.route) {
                                popUpTo(Screen.Home.route) { inclusive = true }
                            }
                        },
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    ) 
                }
                
            composable(Screen.Social.route) {
                SocialScreen(
                    onChatSelected = { convId -> navController.navigate("chat/$convId") },
                    onBack = { navController.popBackStack() }
                )
            }
            composable("chat/{conversationId}") { backStackEntry ->
                val convId = backStackEntry.arguments?.getString("conversationId") ?: return@composable
                ChatScreen(
                    conversationId = convId,
                    onBack = { navController.popBackStack() },
                    onUserClick = { userId ->
                        navController.navigate(Screen.PublicProfile.createRoute(userId))
                    }
                )
            }
            composable(Screen.Share.route) {
                ShareScreen(
                    onBack = { navController.popBackStack() }
                )
            }

            
                composable(Screen.Security.route) {
                    SecurityScreen(onBack = { navController.popBackStack() })
                }
                composable(Screen.Subscription.route) {
                    SubscriptionScreen(onBack = { navController.popBackStack() })
                }

                composable(Screen.Extensions.route) { com.example.ui.screens.extensions.ExtensionsScreen(onBackClick = { navController.popBackStack() }) }
                composable(Screen.Settings.route) { SettingsScreen() }
                composable(Screen.About.route) { AboutScreen() }
                composable(Screen.Trending.route) {
                    TrendingScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.Popular.route) {
                    PopularScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.Upcoming.route) {
            UpcomingScreen(
                onItemClick = { id, isMovie ->
                    if (isMovie) {
                        navController.navigate(Screen.MovieDetails.createRoute(id))
                    } else {
                        navController.navigate(Screen.SeriesDetails.createRoute(id))
                    }
                },
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.NewReleases.route) {
                    NewReleasesScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                composable(Screen.Watching.route) {
                    WatchingScreen(
                        onItemClick = { id, isMovie ->
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        },
                        onBack = { navController.popBackStack() }
                    )
                }
                
                composable("person/{personId}") { backStackEntry ->
                    val personId = backStackEntry.arguments?.getString("personId") ?: return@composable
                    com.example.ui.screens.details.PersonDetailsScreen(
                        personId = personId,
                        onBack = { navController.popBackStack() },
                        onMovieClick = {  com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.MovieDetails.createRoute(it)) },
                        onSeriesClick = {  com.example.utils.AdManager.showInterstitial(context)
navController.navigate(Screen.SeriesDetails.createRoute(it)) }
                    )
                }

                composable(Screen.MovieDetails.route) { backStackEntry ->
                    val movieId = backStackEntry.arguments?.getString("movieId") ?: return@composable
                    MovieDetailsScreen(
                        movieId = movieId, 
                        onBack = { navController.popBackStack() },
                        onPersonClick = { personId -> navController.navigate("person/$personId") },
                        onNavigateToExtensions = { navController.navigate(Screen.Extensions.route) },
                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = URLEncoder.encode(server ?: "", "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        }
                    )
                }
                composable(Screen.SeriesDetails.route) { backStackEntry ->
                    val seriesId = backStackEntry.arguments?.getString("seriesId") ?: return@composable
                    SeriesDetailsScreen(
                        seriesId = seriesId, 
                        onBack = { navController.popBackStack() },
                        onPersonClick = { personId -> navController.navigate("person/$personId") },
                        onNavigateToExtensions = { navController.navigate(Screen.Extensions.route) },
                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedServer = URLEncoder.encode(server ?: "", "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        }
                    )
                }
                
                composable("trailer/{trailerId}") { backStackEntry ->
                    val trailerId = backStackEntry.arguments?.getString("trailerId") ?: return@composable
                    com.example.ui.screens.player.TrailerScreen(trailerId = trailerId, onBack = { navController.popBackStack() })
                }

                composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val url = backStackEntry.arguments?.getString("url") ?: ""
                    val server = backStackEntry.arguments?.getString("server") ?: ""
                    val website = backStackEntry.arguments?.getString("website") ?: ""
                    
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        url = decodedUrl,
                        targetServer = decodedServer,
                        website = decodedWebsite,
                        onBack = { navController.popBackStack() }
                    )
                }
            }
        }
    }
}
}
}
// Trending and Watching added at the end using sed later
