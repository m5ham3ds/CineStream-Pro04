package com.example.ui.screens.profile

import androidx.compose.ui.res.stringResource
import com.example.R

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

    

    val primaryRed = MaterialTheme.colorScheme.primary
    val bgColor = MaterialTheme.colorScheme.background
    val cardColor = MaterialTheme.colorScheme.surface
    val iconBgColor = MaterialTheme.colorScheme.surfaceVariant
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
            title = { Text(stringResource(R.string.sign_out), color = MaterialTheme.colorScheme.onBackground) },
            text = { Text(stringResource(R.string.confirm_sign_out), color = MaterialTheme.colorScheme.onSurfaceVariant) },
            confirmButton = {
                TextButton(
                    onClick = {
                        showLogoutConfirm = false
                        authViewModel.signOut()
                        onNavigateToAuth()
                    }
                ) { Text(stringResource(R.string.sign_out), color = primaryRed) }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutConfirm = false }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onBackground) }
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
            title = { Text(stringResource(R.string.update_profile_pic), color = MaterialTheme.colorScheme.onBackground) },
            text = { 
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    AsyncImage(
                        model = selectedImageUri,
                        contentDescription = "New Profile Photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.size(120.dp).clip(CircleShape).border(2.dp, primaryRed, CircleShape)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(stringResource(R.string.confirm_profile_pic), color = MaterialTheme.colorScheme.onSurfaceVariant)
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
                ) { Text(stringResource(R.string.save), color = primaryRed) }
            },
            dismissButton = {
                TextButton(
                    onClick = { 
                        showImageConfirmDialog = false 
                        selectedImageUri = null
                    },
                    enabled = !isLoading
                ) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onBackground) }
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
                            color = MaterialTheme.colorScheme.onBackground,
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold
                        )
                    } else {
                        Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(40.dp))
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
                        Icon(Icons.Filled.Edit, contentDescription = "Edit", tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(14.dp))
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
                Text(displayName, color = MaterialTheme.colorScheme.onBackground, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                if (currentUser != null && !currentUser?.username.isNullOrEmpty()) {
                    Text(
                        text = "@${currentUser?.username}",
                        color = Color.LightGray,
                        fontSize = 14.sp,
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .clickable {
                                val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                val clip = android.content.ClipData.newPlainText(context.getString(R.string.username_small), currentUser?.username)
                                clipboard.setPrimaryClip(clip)
                                Toast.makeText(context, "Username copied", Toast.LENGTH_SHORT).show()
                            }
                            .padding(2.dp)
                    )
                }
                Text(currentUser?.email ?: "Sign in to access features", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                
                Spacer(modifier = Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Row(
                        modifier = Modifier.background(Color(0xFF301934), RoundedCornerShape(4.dp)).padding(horizontal = 6.dp, vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("👑", fontSize = 10.sp)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(stringResource(R.string.premium_plan), color = Color(0xFFFF5252), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
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
                Text(stringResource(R.string.you_are_premium), color = MaterialTheme.colorScheme.onBackground, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(4.dp))
                Text(stringResource(R.string.enjoy_ad_free), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, lineHeight = 16.sp)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Button(
                onClick = onNavigateToSubscription,
                colors = ButtonDefaults.buttonColors(containerColor = primaryRed),
                shape = RoundedCornerShape(24.dp),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Text(stringResource(R.string.manage_plan), color = MaterialTheme.colorScheme.onBackground, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Account
        Text(stringResource(R.string.account), color = MaterialTheme.colorScheme.onBackground, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))
        Column(modifier = Modifier.fillMaxWidth().background(cardColor, RoundedCornerShape(12.dp))) {
            ProfileListItem(Icons.Default.Person, stringResource(R.string.account_info), stringResource(R.string.account_info_desc), false, primaryRed, iconBgColor, onClick = onNavigateToEditProfile)
            ProfileListItem(Icons.Outlined.Security, stringResource(R.string.security), stringResource(R.string.security_desc), false, primaryRed, iconBgColor, onClick = onNavigateToSecurity)
            ProfileListItem(Icons.Outlined.CreditCard, stringResource(R.string.subscription), stringResource(R.string.subscription_desc), false, primaryRed, iconBgColor, onClick = onNavigateToSubscription)
            ProfileListItem(Icons.Outlined.Settings, "Settings", stringResource(R.string.settings_desc), true, primaryRed, iconBgColor, onClick = onNavigateToSettings)
        }
        
        if (currentUser != null) {
            Spacer(modifier = Modifier.height(32.dp))
            Button(
                onClick = { showLogoutConfirm = true },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(stringResource(R.string.sign_out), color = primaryRed, fontWeight = FontWeight.Bold, fontSize = 16.sp)
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
        Text(count, color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
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
            Text(title, color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
    }
    if (!isLast) {
        HorizontalDivider(modifier = Modifier.padding(start = 72.dp), color = MaterialTheme.colorScheme.surfaceVariant)
    }
}