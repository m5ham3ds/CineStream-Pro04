package com.example.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(onBack: () -> Unit) {
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)
    val primaryRed = Color(0xFFE50914)
    val iconBgColor = Color(0xFF2C2C2E)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("App Settings", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = surfaceColor)
            )
        },
        containerColor = bgColor
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp)
        ) {
            Text("Preferences", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(12.dp))
            Column(modifier = Modifier.fillMaxWidth().background(surfaceColor, RoundedCornerShape(12.dp))) {
                SettingsListItem(Icons.Outlined.Settings, "General", "Language, theme", false, primaryRed, iconBgColor)
                SettingsListItem(Icons.Outlined.PlayCircleOutline, "Playback", "Quality, subtitles, autoplay", false, primaryRed, iconBgColor)
                SettingsListItem(Icons.Outlined.Notifications, "Notifications", "Manage your notification preferences", true, primaryRed, iconBgColor)
            }
            Spacer(modifier = Modifier.height(24.dp))
            Text("About", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(12.dp))
            Column(modifier = Modifier.fillMaxWidth().background(surfaceColor, RoundedCornerShape(12.dp))) {
                SettingsListItem(Icons.Outlined.Settings, "Version", "1.0.0", false, Color.Gray, iconBgColor)
                SettingsListItem(Icons.Outlined.Settings, "Terms of Service", "", false, Color.Gray, iconBgColor)
                SettingsListItem(Icons.Outlined.Settings, "Privacy Policy", "", true, Color.Gray, iconBgColor)
            }
        }
    }
}

@Composable
fun SettingsListItem(icon: ImageVector, title: String, subtitle: String, isLast: Boolean, tintColor: Color, iconBg: Color, onClick: () -> Unit = {}) {
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
            if (subtitle.isNotEmpty()) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(subtitle, color = Color.Gray, fontSize = 12.sp)
            }
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray)
    }
    if (!isLast) {
        HorizontalDivider(modifier = Modifier.padding(start = 72.dp), color = Color(0xFF2C2C2E))
    }
}
