package com.example.ui.screens.profile

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.outlined.*
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.outlined.Person

import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.net.Uri
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.ViewModelFactory
import com.example.ui.screens.auth.AuthViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(onNavigateToAuth: () -> Unit = {}, onNavigateToEditProfile: () -> Unit = {}, onNavigateToSecurity: () -> Unit = {}, onNavigateToSubscription: () -> Unit = {}, onNavigateToSettings: () -> Unit = {}) {
    val authViewModel: AuthViewModel = viewModel(factory = ViewModelFactory())
    val currentUser by authViewModel.currentUser.collectAsState()
    val isLoading by authViewModel.isLoading.collectAsState()
    val context = LocalContext.current

    

    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val cardColor = Color(0xFF1E1E1E)
    val iconBgColor = Color(0xFF2C2C2E)
    var showEditPhoto by remember { mutableStateOf(false) }
    var showImageConfirmDialog by remember { mutableStateOf(false) }
    var showLogoutConfirm by remember { mutableStateOf(false) }
    
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedImageUri = uri
            showImageConfirmDialog = true
        }
    }
    
    if (showEditPhoto) {
        LaunchedEffect(Unit) {
            photoPickerLauncher.launch("image/*")
            showEditPhoto = false
        }
    }

    
    if (showLogoutConfirm) {
        AlertDialog(
            onDismissRequest = { showLogoutConfirm = false },
            title = { Text("Sign Out", color = Color.White) },
            text = { Text("Are you sure you want to sign out?", color = Color.Gray) },
            confirmButton = {
                TextButton(
                    onClick = {
                        showLogoutConfirm = false
                        authViewModel.signOut()
                        onNavigateToAuth()
                    }
                ) { Text("Sign Out", color = primaryRed) }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutConfirm = false }) { Text("Cancel", color = Color.White) }
            },
            containerColor = cardColor
        )
    }

    if (showImageConfirmDialog && selectedImageUri != null) {
        AlertDialog(
            onDismissRequest = { 
                showImageConfirmDialog = false 
                selectedImageUri = null
            },
            title = { Text("Update Profile Picture", color = Color.White) },
            text = { 
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    AsyncImage(
                        model = selectedImageUri,
                        contentDescription = "New Profile Photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.size(120.dp).clip(CircleShape).border(2.dp, primaryRed, CircleShape)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Do you want to set this as your new profile picture?", color = Color.Gray)
                    if (isLoading) {
                        Spacer(modifier = Modifier.height(16.dp))
                        CircularProgressIndicator(color = primaryRed)
                    }
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        authViewModel.updateProfile(
                            currentUser?.firstName ?: "", 
                            currentUser?.lastName ?: "", 
                            currentUser?.username ?: "", 
                            currentUser?.isProfilePublic ?: true,
                            selectedImageUri
                        ) { success, error ->
                            if (success) {
                                showImageConfirmDialog = false
                                selectedImageUri = null
                                Toast.makeText(context, "Profile picture updated", Toast.LENGTH_SHORT).show()
                            } else {
                                Toast.makeText(context, error ?: "Failed to update", Toast.LENGTH_SHORT).show()
                            }
                        }
                    },
                    enabled = !isLoading
                ) { Text("Save", color = primaryRed) }
            },
            dismissButton = {
                TextButton(
                    onClick = { 
                        showImageConfirmDialog = false 
                        selectedImageUri = null
                    },
                    enabled = !isLoading
                ) { Text("Cancel", color = Color.White) }
            },
            containerColor = cardColor
        )
    }


    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box {
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(iconBgColor)
                        .border(2.dp, primaryRed, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    if (selectedImageUri != null || (currentUser != null && currentUser?.photoUrl?.isNotEmpty() == true)) {
                        AsyncImage(
                            model = selectedImageUri ?: currentUser?.photoUrl,
                            contentDescription = "Profile Photo",
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                    } else if (currentUser != null) {
                        Text(
                            text = (currentUser?.firstName?.take(1) ?: currentUser?.username?.take(1) ?: "U").uppercase(),
                            color = Color.White,
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold
                        )
                    } else {
                        Icon(Icons.Default.Person, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(40.dp))
                    }
                }
                if (currentUser != null) {
                    Box(
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .size(24.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF3A3A3C))
                            .clickable { showEditPhoto = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Filled.Edit, contentDescription = "Edit", tint = Color.White, modifier = Modifier.size(14.dp))
                    }
                }
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(
                modifier = Modifier
                    .weight(1f)
                    .clickable(enabled = currentUser != null) { onNavigateToEditProfile() }
                    .padding(vertical = 4.dp)
            ) {
                val displayName = if (currentUser != null) {
                    "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "User"
                } else {
                    "Guest User"
                }
                Text(displayName, color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                if (currentUser != null && !currentUser?.username.isNullOrEmpty()) {
                    Text(
                        text = "@${currentUser?.username}",
                        color = Color.LightGray,
                        fontSize = 14.sp,
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .clickable {
                                val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                val clip = android.content.ClipData.newPlainText("username", currentUser?.username)
                                clipboard.setPrimaryClip(clip)
                                Toast.makeText(context, "Username copied", Toast.LENGTH_SHORT).show()
                            }
                            .padding(2.dp)
                    )
                }
                Text(currentUser?.email ?: "Sign in to access features", color = Color.Gray, fontSize = 14.sp)
                
                Spacer(modifier = Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Row(
                        modifier = Modifier.background(Color(0xFF301934), RoundedCornerShape(4.dp)).padding(horizontal = 6.dp, vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("👑", fontSize = 10.sp)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Premium Plan", color = Color(0xFFFF5252), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Stats Row
        Row(
            modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp)).padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            StatItem(Icons.Outlined.Movie, "24", "Movies", primaryRed)
            StatItem(Icons.Outlined.Tv, "12", "Series", primaryRed)
            StatItem(Icons.Outlined.Face, "5", "Anime", primaryRed)
            StatItem(Icons.Outlined.FavoriteBorder, "18", "Watchlist", primaryRed)
            StatItem(Icons.Outlined.Download, "7", "Downloads", primaryRed)
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Premium Banner
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, primaryRed.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                .background(cardColor, RoundedCornerShape(12.dp))
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(48.dp).clip(CircleShape).background(iconBgColor),
                contentAlignment = Alignment.Center
            ) {
                Text("👑", fontSize = 24.sp)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text("You're Premium!", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(4.dp))
                Text("Enjoy ad-free streaming and exclusive content.", color = Color.Gray, fontSize = 12.sp, lineHeight = 16.sp)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Button(
                onClick = onNavigateToSubscription,
                colors = ButtonDefaults.buttonColors(containerColor = primaryRed),
                shape = RoundedCornerShape(24.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Text("Manage Plan", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Account
        Text("Account", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, "Account Information", "Update your personal details", false, primaryRed, iconBgColor, onClick = onNavigateToEditProfile)
            ProfileListItem(Icons.Outlined.Security, "Security", "Password, device management", false, primaryRed, iconBgColor, onClick = onNavigateToSecurity)
            ProfileListItem(Icons.Outlined.CreditCard, "Subscription", "Manage your plan and billing", false, primaryRed, iconBgColor, onClick = onNavigateToSubscription)
            ProfileListItem(Icons.Outlined.Settings, "Settings", "App preferences and settings", true, primaryRed, iconBgColor, onClick = onNavigateToSettings)
        }
        
        if (currentUser != null) {
            Spacer(modifier = Modifier.height(32.dp))
            Button(
                onClick = { showLogoutConfirm = true },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2C2C2E)),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Sign Out", color = primaryRed, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            }
        }

        Spacer(modifier = Modifier.height(100.dp))
    }
}

@Composable
fun StatItem(icon: ImageVector, count: String, label: String, tintColor: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.height(8.dp))
        Text(count, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = Color.Gray, fontSize = 12.sp)
    }
}

@Composable
fun ProfileListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, iconBg: Color, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier.fillMaxWidth().clickable { onClick() }.padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier.size(40.dp).clip(CircleShape).background(iconBg),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(20.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = Color.Gray, fontSize = 12.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
    if (!isLast) {
        HorizontalDivider(modifier = Modifier.padding(start = 72.dp), color = Color(0xFF2C2C2E))
    }
}
