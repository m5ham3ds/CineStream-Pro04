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
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.R
import com.example.ui.screens.auth.AuthViewModel
import kotlinx.coroutines.launch
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun ProfileScreen(
    onNavigateToEditProfile: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToSecurity: () -> Unit,
    onNavigateToSubscription: () -> Unit,
    onNavigateToHelpSupport: () -> Unit,
    onNavigateToAuth: () -> Unit = {},
    authViewModel: AuthViewModel = viewModel()
) {
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(350)
        isLoading = false
    }
    if (isLoading) {
        com.example.ui.components.ProfileScreenSkeleton()
        return
    }

    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val currentUser by authViewModel.currentUser.collectAsStateWithLifecycle()
    var showLogoutConfirm by remember { mutableStateOf(false) }

    val bgColor = Color(0xFF09090C)
    val cardBg = Color(0xFF16161A)
    val redPrimary = androidx.compose.material3.MaterialTheme.colorScheme.primary
    val textGrey = Color(0xFFAAAAAA)

    if (showLogoutConfirm) {
        AlertDialog(
            onDismissRequest = { showLogoutConfirm = false },
            title = { Text(stringResource(R.string.sign_out), color = Color.White) },
            text = { Text(stringResource(R.string.confirm_sign_out), color = textGrey) },
            confirmButton = {
                TextButton(onClick = {
                    showLogoutConfirm = false
                    authViewModel.signOut()
                    onNavigateToAuth()
                }) {
                    Text(stringResource(R.string.sign_out), color = redPrimary)
                }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutConfirm = false }) {
                    Text("Cancel", color = Color.White)
                }
            },
            containerColor = cardBg
        )
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .drawBehind {
                val glowBrush = Brush.radialGradient(
                    colors = listOf(redPrimary.copy(alpha = 0.15f), Color.Transparent),
                    center = Offset(0f, 0f),
                    radius = size.width * 0.8f
                )
                drawRect(brush = glowBrush)
            }
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            Spacer(modifier = Modifier.height(24.dp))

            // Top Profile Section
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Avatar with red glow
                Box(
                    modifier = Modifier
                        .size(64.dp)
                        .clip(CircleShape)
                        .border(2.dp, redPrimary, CircleShape)
                        .background(Color(0xFF1C1C1E)),
                    contentAlignment = Alignment.Center
                ) {
                    val initial = currentUser?.firstName?.firstOrNull()?.toString() 
                        ?: currentUser?.username?.firstOrNull()?.toString()?.uppercase() 
                        ?: "M"
                    Text(initial, color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    
                    // Camera icon badge
                    Box(
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .offset(x = (-4).dp, y = (-4).dp)
                            .size(20.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF2C2C2E)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Outlined.CameraAlt, contentDescription = null, tint = Color.White, modifier = Modifier.size(12.dp))
                    }
                }

                Spacer(modifier = Modifier.width(16.dp))

                // Name and details
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        val name = if (currentUser != null) {
                            "${currentUser?.firstName} ${currentUser?.lastName}".trim().takeIf { it.isNotBlank() } ?: currentUser?.username ?: "M O H A M E D"
                        } else {
                            "G U E S T"
                        }
                        Text(
                            name.uppercase().replace("", " ").trim(), // Add spaces between letters for the stylized look
                            color = Color.White,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Icon(
                            Icons.Default.Edit,
                            contentDescription = "Edit Profile",
                            tint = redPrimary,
                            modifier = Modifier
                                .size(16.dp)
                                .clickable { onNavigateToEditProfile() }
                        )
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        "@${currentUser?.username ?: "guest"}",
                        color = textGrey,
                        fontSize = 9.sp
                    )
                    Text(
                        currentUser?.email ?: "guest@example.com",
                        color = textGrey,
                        fontSize = 9.sp
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Premium Badge
                    Row(
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(
                                Brush.horizontalGradient(
                                    colors = listOf(Color(0xFF4A0E13), Color(0xFF2A080C))
                                )
                            )
                            .padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("👑", fontSize = 9.sp)
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Premium Plan >", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                    }
                }

                // Right Text Block
                Column(horizontalAlignment = Alignment.End) {
                    Text("GOOD\nSTORIES\nNEVER\nEND", color = textGrey, fontSize = 9.sp, textAlign = TextAlign.End, lineHeight = 14.sp)
                    Spacer(modifier = Modifier.height(4.dp))
                    Box(modifier = Modifier.width(24.dp).height(2.dp).background(redPrimary))
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Stats Row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(cardBg)
                    .padding(vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem(Icons.Outlined.Movie, "24", "Movies", redPrimary)
                StatItem(Icons.Outlined.Tv, "12", "Series", redPrimary)
                StatItem(Icons.Outlined.Face, "5", "Anime", redPrimary)
                StatItem(Icons.Outlined.FavoriteBorder, "18", "Watchlist", redPrimary)
                StatItem(Icons.Outlined.Download, "7", "Downloads", redPrimary)
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Premium Card
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .border(1.dp, Color(0xFF3A1015), RoundedCornerShape(16.dp))
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color(0xFF2A0C10), cardBg)
                        )
                    )
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("👑", fontSize = 24.sp)
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        buildAnnotatedString {
                            withStyle(style = SpanStyle(color = Color.White, fontWeight = FontWeight.Bold)) {
                                append("You're ")
                            }
                            withStyle(style = SpanStyle(color = redPrimary, fontWeight = FontWeight.Bold)) {
                                append("Premium!")
                            }
                        },
                        fontSize = 18.sp
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("Enjoy ad-free streaming\nand exclusive content.", color = textGrey, fontSize = 9.sp, lineHeight = 16.sp)
                }
                
                Button(
                    onClick = onNavigateToSubscription,
                    colors = ButtonDefaults.buttonColors(containerColor = redPrimary),
                    shape = RoundedCornerShape(24.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text("Manage Plan →", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Account Section Header
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                verticalAlignment = Alignment.Bottom,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(stringResource(R.string.account), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Text("Manage your account settings", color = textGrey, fontSize = 9.sp)
            }

            // Account List
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(cardBg)
            ) {
                ProfileListItem(Icons.Default.Person, stringResource(R.string.account_info), "Update your personal details", false, redPrimary, onClick = onNavigateToEditProfile)
                ProfileListItem(Icons.Outlined.Security, stringResource(R.string.security), "Password, device management", false, redPrimary, onClick = onNavigateToSecurity)
                ProfileListItem(Icons.Outlined.CreditCard, stringResource(R.string.subscription), "Manage your plan and billing", false, redPrimary, onClick = onNavigateToSubscription)
                ProfileListItem(Icons.Outlined.Settings, "App Settings", "App preferences and playback settings", false, redPrimary, onClick = onNavigateToSettings)
                ProfileListItem(Icons.AutoMirrored.Filled.HelpOutline, stringResource(R.string.help_support), "Get help or contact us", true, redPrimary, onClick = onNavigateToHelpSupport)
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Sign Out Button
            if (currentUser != null) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(cardBg)
                        .clickable { showLogoutConfirm = true }
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.AutoMirrored.Filled.Logout, contentDescription = null, tint = redPrimary, modifier = Modifier.size(20.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(stringResource(R.string.sign_out), color = redPrimary, fontSize = 13.sp, fontWeight = FontWeight.Medium)
                }
            }

            Spacer(modifier = Modifier.height(100.dp))
        }
    }
}

@Composable
fun StatItem(icon: ImageVector, count: String, label: String, tintColor: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(20.dp))
        Spacer(modifier = Modifier.height(8.dp))
        Text(count, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(2.dp))
        Text(label, color = Color.Gray, fontSize = 9.sp)
    }
}

@Composable
fun ProfileListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(30.dp)
                .clip(CircleShape)
                .background(Color(0xFF1E1E22)), // Slightly lighter dark circle
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = tintColor, modifier = Modifier.size(16.dp))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Medium)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, color = Color.Gray, fontSize = 9.sp)
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
    }
    if (!isLast) {
        HorizontalDivider(modifier = Modifier.padding(start = 68.dp), color = Color(0xFF222225), thickness = 1.dp)
    }
}
