package com.example.ui.screens.social

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.R
import com.example.data.repository.Conversation
import com.example.data.repository.UserProfile
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SocialScreen(
    viewModel: SocialViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onChatSelected: (String) -> Unit = {},
    onBack: () -> Unit = {}
) {
    val currentUser by viewModel.currentUser.collectAsState()
    val conversations by viewModel.conversations.collectAsState()
    val searchResults by viewModel.searchResults.collectAsState()
    var selectedCategory by remember { mutableStateOf("All Messages") }

    
    val primaryRed = Color(0xFFE50914)
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)
    
    var searchQuery by remember { mutableStateOf("") }

    if (currentUser == null) {
        Box(modifier = Modifier.fillMaxSize().background(bgColor), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("CineStream Community", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Sign in to chat and share with others", color = Color.Gray)
            }
        }
    } else {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(bgColor)
        ) {
            // Header / Search Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp)
            ) {
                TextField(
                    value = searchQuery,
                    onValueChange = { 
                        searchQuery = it 
                        viewModel.searchUsers(it)
                    },
                    placeholder = { Text("Search by username to message...", color = Color.Gray) },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.Gray) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, primaryRed.copy(alpha = 0.5f), RoundedCornerShape(24.dp))
                        .clip(RoundedCornerShape(24.dp)),
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = surfaceColor,
                        unfocusedContainerColor = surfaceColor,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White
                    ),
                    singleLine = true
                )
            }
            
            if (searchQuery.isNotEmpty()) {
                // Show Search Results
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp)
                ) {
                    items(searchResults) { user ->
                        if (user.uid != currentUser?.uid) {
                            UserSearchResultItem(user) {
                                viewModel.startConversation(user.uid, user.displayName) { convId ->
                                    onChatSelected(convId)
                                }
                            }
                        }
                    }
                }
            } else {
                // Default View (Stories + Conversations)
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Stories", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text("View all", color = primaryRed, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    item {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(
                                modifier = Modifier
                                    .size(64.dp)
                                    .border(1.dp, primaryRed, CircleShape)
                                    .clickable { /* TODO */ },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Add, contentDescription = "Add Story", tint = primaryRed, modifier = Modifier.size(32.dp))
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Add Story", color = Color.White, fontSize = 12.sp)
                        }
                    }
                    // For now, no actual stories are rendered until fetched, we just show add story
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Filter Chips container
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clip(RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                        .background(surfaceColor)
                ) {
                    Column {
                        LazyRow(
                            modifier = Modifier.padding(top = 16.dp, bottom = 8.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            val categories = listOf("All Messages", "Unread", "Groups", "Requests")
                            items(categories) { category ->
                                CustomFilterChip(
                                    text = category,
                                    selected = selectedCategory == category,
                                    onClick = { selectedCategory = category }
                                )
                            }
                        }
                        
                        LazyColumn(
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            val filteredConversations = when (selectedCategory) {
                                "All Messages" -> conversations.filter { !it.isGroup && !it.isRequest }
                                "Unread" -> conversations.filter { (it.unreadCounts[currentUser?.uid ?: ""] ?: 0) > 0 }
                                "Groups" -> conversations.filter { it.isGroup }
                                "Requests" -> conversations.filter { it.isRequest }
                                else -> conversations
                            }
                            items(filteredConversations) { conv ->
                                val otherUserId = conv.participants.firstOrNull { it != currentUser?.uid } ?: ""
                                val otherUserName = conv.participantNames[otherUserId] ?: "Unknown"
                                val unreadCount = conv.unreadCounts[currentUser?.uid ?: ""] ?: 0
                                
                                ChatListItem(
                                    name = otherUserName,
                                    message = conv.lastMessage,
                                    time = formatTime(conv.lastMessageTime),
                                    unreadCount = unreadCount,
                                    onClick = { onChatSelected(conv.id) }
                                )
                            }
                            item { Spacer(modifier = Modifier.height(80.dp)) }
                        }
                    }
                }
            }
        }
    }
}

private fun formatTime(timeMillis: Long): String {
    if (timeMillis == 0L) return ""
    val sdf = SimpleDateFormat("hh:mm a", Locale.getDefault())
    return sdf.format(Date(timeMillis))
}

@Composable
fun CustomFilterChip(text: String, selected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .clickable { onClick() }
            .background(if (selected) Color(0xFFE50914) else Color(0xFF2C2C2E))
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Text(text, color = if (selected) Color.White else Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.Medium)
    }
}

@Composable
fun UserSearchResultItem(user: UserProfile, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF1C1C1E))
            .clickable(onClick = onClick)
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .background(Color(0xFF2C2C2E)),
            contentAlignment = Alignment.Center
        ) {
            Text(user.displayName.take(1).uppercase(), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        Spacer(modifier = Modifier.width(16.dp))
        Text(user.displayName, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Composable
fun ChatListItem(name: String, message: String, time: String, unreadCount: Int, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF121212))
            .clickable(onClick = onClick)
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Avatar
        Box {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(Color(0xFF2C2C2E)),
                contentAlignment = Alignment.Center
            ) {
                Text(name.take(1).uppercase(), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            }
        }
        
        Spacer(modifier = Modifier.width(16.dp))
        
        // Texts
        Column(modifier = Modifier.weight(1f)) {
            Text(name, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(message.ifEmpty { "Start a conversation" }, color = Color.Gray, fontSize = 14.sp, maxLines = 1)
        }
        
        // Time & Badge
        Column(horizontalAlignment = Alignment.End) {
            Text(time, color = if (unreadCount > 0) Color(0xFFE50914) else Color.Gray, fontSize = 12.sp)
            Spacer(modifier = Modifier.height(6.dp))
            if (unreadCount > 0) {
                Box(
                    modifier = Modifier
                        .size(24.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE50914)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(unreadCount.toString(), color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            } else {
                Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
            }
        }
    }
}
