package com.example.ui.screens.extensions

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.extensions.ExtensionManager
import com.example.extensions.ProviderExtension

enum class ExtensionFilter(val title: String, val icon: ImageVector) {
    ALL("الكل", Icons.Filled.GridView),
    ANIME("الأنمي", Icons.Default.Face),
    MOVIES("الأفلام", Icons.Outlined.Movie),
    SERIES("المسلسلات", Icons.Outlined.Tv)
}

@Composable
fun ExtensionsScreen(onBackClick: () -> Unit) {
    val installedExtensions by ExtensionManager.installedExtensions.collectAsState()
    val availableExtensions = ExtensionManager.availableExtensions

    var selectedFilter by remember { mutableStateOf(ExtensionFilter.ALL) }
    var searchQuery by remember { mutableStateOf("") }
    var showNotice by remember { mutableStateOf(true) }

    val filteredExtensions = availableExtensions.filter { ext ->
        val matchesSearch = ext.name.contains(searchQuery, ignoreCase = true) || ext.baseUrl.contains(searchQuery, ignoreCase = true)
        val matchesFilter = when (selectedFilter) {
            ExtensionFilter.ALL -> true
            ExtensionFilter.ANIME -> ext.isAnime
            ExtensionFilter.MOVIES -> ext.isMovie
            ExtensionFilter.SERIES -> ext.isSeries
        }
        matchesSearch && matchesFilter
    }

    Scaffold(
        containerColor = Color(0xFF0F0F11)
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            Column(modifier = Modifier.fillMaxSize()) {
                ExtensionsTopBar(onBackClick = onBackClick)
                
                FilterTabs(selectedFilter = selectedFilter, onFilterSelected = { selectedFilter = it })
                
                SearchAndFilterRow(searchQuery = searchQuery, onSearchQueryChange = { searchQuery = it })
                
                LazyColumn(
                    modifier = Modifier.fillMaxWidth().weight(1f),
                    contentPadding = PaddingValues(bottom = if (showNotice) 120.dp else 16.dp)
                ) {
                    items(filteredExtensions) { ext ->
                        val isInstalled = installedExtensions.any { it.id == ext.id }
                        ExtensionItem(
                            ext = ext,
                            isInstalled = isInstalled,
                            onInstallClick = { ExtensionManager.installExtension(ext.id) },
                            onUninstallClick = { ExtensionManager.uninstallExtension(ext.id) }
                        )
                    }
                }
            }
            
            if (showNotice) {
                Box(
                    modifier = Modifier.align(Alignment.BottomCenter)
                ) {
                    NoticeBanner(onDismiss = { showNotice = false })
                }
            }
        }
    }
}

@Composable
fun ExtensionsTopBar(onBackClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text("الإضافات", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Text("إدارة مصادر المشاهدة واستمتع بمحتوى أكثر", color = Color.Gray, fontSize = 12.sp)
        }
        
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(RoundedCornerShape(12.dp))
                .border(1.dp, Color.Red.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                .background(Color.Red.copy(alpha = 0.1f)),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Filled.Extension, contentDescription = null, tint = Color.Red, modifier = Modifier.size(24.dp))
        }
    }
}

@Composable
fun FilterTabs(selectedFilter: ExtensionFilter, onFilterSelected: (ExtensionFilter) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        ExtensionFilter.values().forEach { filter ->
            val isSelected = filter == selectedFilter
            Surface(
                shape = RoundedCornerShape(24.dp),
                color = if (isSelected) Color(0xFFE50914) else Color(0xFF19191C),
                border = if (isSelected) null else BorderStroke(1.dp, Color(0xFF2A2A2E)),
                modifier = Modifier.clickable { onFilterSelected(filter) }
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Icon(
                        imageVector = filter.icon,
                        contentDescription = null,
                        tint = if (isSelected) Color.White else Color.Gray,
                        modifier = Modifier.size(16.dp)
                    )
                    Text(
                        text = filter.title,
                        color = if (isSelected) Color.White else Color.Gray,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}

@Composable
fun SearchAndFilterRow(searchQuery: String, onSearchQueryChange: (String) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .border(1.dp, Color.Red.copy(alpha = 0.5f), CircleShape)
                .background(Color.Red.copy(alpha = 0.1f))
                .clickable { /* Filter logic */ },
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Filled.Tune, contentDescription = "Filter", tint = Color.White)
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        TextField(
            value = searchQuery,
            onValueChange = onSearchQueryChange,
            modifier = Modifier
                .weight(1f)
                .height(52.dp),
            placeholder = { Text("البحث في الإضافات...", color = Color.Gray) },
            trailingIcon = { Icon(Icons.Filled.Search, contentDescription = "Search", tint = Color.Gray) },
            colors = TextFieldDefaults.colors(
                focusedContainerColor = Color(0xFF19191C),
                unfocusedContainerColor = Color(0xFF19191C),
                focusedIndicatorColor = Color.Transparent,
                unfocusedIndicatorColor = Color.Transparent,
                focusedTextColor = Color.White,
                unfocusedTextColor = Color.White
            ),
            shape = RoundedCornerShape(26.dp),
            singleLine = true
        )
    }
}

@Composable
fun ExtensionItem(ext: ProviderExtension, isInstalled: Boolean, onInstallClick: () -> Unit, onUninstallClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
        shape = RoundedCornerShape(16.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Logo
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(Color(0xFF0F0F11)),
                contentAlignment = Alignment.Center
            ) {
                if (ext.iconUrl.isNotEmpty()) {
                    AsyncImage(
                        model = ext.iconUrl,
                        contentDescription = null,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Text(
                        text = ext.name.take(2).uppercase(),
                        color = Color.White,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // Info
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = ext.name,
                        color = Color.White,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                
                Text(
                    text = ext.baseUrl,
                    color = Color.Gray,
                    fontSize = 12.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.height(6.dp))
                
                // Badges
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    if (ext.isAnime) {
                        Badge(text = "الأنمي", icon = null, color = Color.Red, bgColor = Color.Red.copy(alpha = 0.15f))
                    } else if (ext.isMovie || ext.isSeries) {
                        Badge(
                            text = if(ext.isMovie && ext.isSeries) "شامل" else if (ext.isMovie) "أفلام" else "مسلسلات", 
                            icon = null, 
                            color = Color.Red, 
                            bgColor = Color.Red.copy(alpha = 0.15f)
                        )
                    }
                    
                    if (ext.lang.isNotEmpty()) {
                        Badge(
                            text = ext.lang.uppercase(), 
                            icon = Icons.Outlined.Language, 
                            color = Color.Gray, 
                            bgColor = Color(0xFF2A2A2E)
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.width(4.dp))
            
            // Action Button & More
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (isInstalled) {
                    OutlinedButton(
                        onClick = onUninstallClick,
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.White),
                        border = BorderStroke(1.dp, Color(0xFF2A2A2E)),
                        shape = RoundedCornerShape(20.dp),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                        modifier = Modifier.height(36.dp)
                    ) {
                        Icon(Icons.Outlined.Delete, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("إلغاء التثبيت", fontSize = 12.sp)
                    }
                } else {
                    Button(
                        onClick = onInstallClick,
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914)),
                        shape = RoundedCornerShape(20.dp),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                        modifier = Modifier.height(36.dp)
                    ) {
                        Icon(Icons.Filled.Add, contentDescription = null, modifier = Modifier.size(16.dp), tint = Color.White)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("تثبيت", fontSize = 12.sp, color = Color.White)
                    }
                }
                
                IconButton(onClick = { /* TODO */ }, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Filled.MoreVert, contentDescription = "More", tint = Color.Gray)
                }
            }
        }
    }
}

@Composable
fun Badge(text: String, icon: ImageVector?, color: Color, bgColor: Color) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .padding(horizontal = 8.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        if (icon != null) {
            Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(12.dp))
        }
        Text(text, color = color, fontSize = 10.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun NoticeBanner(onDismiss: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF19191C)),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, Color.Red.copy(alpha = 0.3f))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(Color.Red.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Outlined.Lightbulb, contentDescription = null, tint = Color.Red)
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text("ملاحظة", color = Color.Red, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    "يمكنك تثبيت عدة إضافات للحصول على تجربة مشاهدة أفضل ومصادر أكثر.",
                    color = Color.Gray,
                    fontSize = 13.sp,
                    lineHeight = 18.sp
                )
            }
            
            IconButton(onClick = onDismiss, modifier = Modifier.size(24.dp)) {
                Icon(Icons.Filled.Close, contentDescription = "Close", tint = Color.Gray)
            }
        }
    }
}