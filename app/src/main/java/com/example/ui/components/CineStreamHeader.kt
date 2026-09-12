package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun CineStreamHeader(
    onProfileClick: () -> Unit,
    onSearchClick: () -> Unit,
    onMenuClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                Brush.horizontalGradient(
                    colors = listOf(
                        Color(0xFF2A0505),
                        Color(0xFF101010),
                        Color(0xFF101010),
                        Color(0xFF2A0505)
                    )
                )
            )
            .statusBarsPadding()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        // Profile Icon
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(Color(0xFF1A1A1A))
                .border(2.dp, Color(0xFFE50914), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            IconButton(onClick = onProfileClick) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = "Profile",
                    tint = Color.LightGray,
                    modifier = Modifier.size(28.dp)
                )
            }
        }

        // Logo
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = buildAnnotatedString {
                    withStyle(style = SpanStyle(color = Color.White, fontWeight = FontWeight.Bold, fontSize = 26.sp)) {
                        append("Cine")
                    }
                    withStyle(style = SpanStyle(color = Color(0xFFE50914), fontWeight = FontWeight.Bold, fontSize = 26.sp)) {
                        append("Stream")
                    }
                }
            )
            Text(
                text = buildAnnotatedString {
                    withStyle(style = SpanStyle(color = Color(0xFFB3B3B3), fontSize = 9.sp, letterSpacing = 3.sp, fontWeight = FontWeight.Bold)) {
                        append("MOVIES")
                    }
                    withStyle(style = SpanStyle(color = Color(0xFFE50914), fontSize = 9.sp, fontWeight = FontWeight.Bold)) {
                        append(" • ")
                    }
                    withStyle(style = SpanStyle(color = Color(0xFFB3B3B3), fontSize = 9.sp, letterSpacing = 3.sp, fontWeight = FontWeight.Bold)) {
                        append("SERIES")
                    }
                    withStyle(style = SpanStyle(color = Color(0xFFE50914), fontSize = 9.sp, fontWeight = FontWeight.Bold)) {
                        append(" • ")
                    }
                    withStyle(style = SpanStyle(color = Color(0xFFB3B3B3), fontSize = 9.sp, letterSpacing = 3.sp, fontWeight = FontWeight.Bold)) {
                        append("ANIME")
                    }
                }
            )
        }

        // Actions
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // Search
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(CircleShape)
                    .background(Color(0xFF181818))
                    .border(1.dp, Color(0xFF2C2C2C), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                IconButton(onClick = onSearchClick) {
                    Icon(
                        imageVector = Icons.Default.Search,
                        contentDescription = "Search",
                        tint = Color.White,
                        modifier = Modifier.size(22.dp)
                    )
                }
            }

            // Notifications
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(CircleShape)
                    .background(Color(0xFF181818))
                    .border(1.dp, Color(0xFF2C2C2C), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                IconButton(onClick = { /* TODO */ }) {
                    Box {
                        Icon(
                            imageVector = Icons.Default.Notifications,
                            contentDescription = "Notifications",
                            tint = Color.White,
                            modifier = Modifier.size(22.dp)
                        )
                        // Notification badge
                        Box(
                            modifier = Modifier
                                .size(18.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFE50914))
                                .align(Alignment.TopEnd)
                                .offset(x = 6.dp, y = (-4).dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("1", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            // Menu
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(Color(0xFF181818))
                    .border(1.dp, Color(0xFF2C2C2C), RoundedCornerShape(14.dp)),
                contentAlignment = Alignment.Center
            ) {
                IconButton(onClick = onMenuClick) {
                    Icon(
                        imageVector = Icons.Default.Menu,
                        contentDescription = "Menu",
                        tint = Color.White,
                        modifier = Modifier.size(22.dp)
                    )
                }
            }
        }
    }
}
