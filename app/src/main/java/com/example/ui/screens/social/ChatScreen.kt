package com.example.ui.screens.social

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.MicNone
import androidx.compose.material.icons.filled.Block
import androidx.compose.material.icons.filled.PlayArrow
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
import com.example.data.repository.PrivateMessage

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ChatScreen(
    conversationId: String,
    viewModel: ChatViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onBack: () -> Unit,
    onUserClick: (String) -> Unit = {}
) {
    val currentUser by viewModel.currentUser.collectAsState()
    val context = LocalContext.current
    var selectedMessage by remember { mutableStateOf<PrivateMessage?>(null) }
    var editingMessage by remember { mutableStateOf<PrivateMessage?>(null) }
    var showDeleteConfirm by remember { mutableStateOf(false) }

    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri != null) {
            viewModel.sendMessage("Shared an image: $uri")
        }
    }


    val otherUser by viewModel.otherUser.collectAsState()
    val messages by viewModel.messages.collectAsState()
    var messageText by remember { mutableStateOf("") }
    
    val bgColor = Color(0xFF121212)
    val surfaceColor = Color(0xFF1C1C1E)
    val primaryRed = Color(0xFFE50914)
    val darkGray = Color(0xFF2C2C2E)

    LaunchedEffect(conversationId) {
        viewModel.loadConversation(conversationId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clickable { otherUser?.uid?.let { onUserClick(it) } }
                            .padding(vertical = 4.dp, horizontal = 4.dp)
                    ) {
                        Box(
                            modifier = Modifier.size(40.dp).clip(CircleShape).background(darkGray),
                            contentAlignment = Alignment.Center
                        ) {
                            if (otherUser?.photoUrl?.isNotEmpty() == true) {
                                AsyncImage(
                                    model = otherUser?.photoUrl,
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize()
                                )
                            } else {
                                Text((otherUser?.displayName?.take(1) ?: "U").uppercase(), color = Color.White, fontWeight = FontWeight.Bold)
                            }
                            
                            // Online indicator
                            Box(
                                modifier = Modifier
                                    .size(12.dp)
                                    .align(Alignment.BottomEnd)
                                    .background(bgColor, CircleShape)
                                    .padding(2.dp)
                            ) {
                                Box(modifier = Modifier.fillMaxSize().background(Color(0xFF4CAF50), CircleShape))
                            }
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(otherUser?.displayName ?: "Loading...", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(6.dp).background(primaryRed, CircleShape))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Online", color = Color.LightGray, fontSize = 12.sp)
                            }
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(onClick = {}) { Icon(Icons.Default.Phone, contentDescription = "Call", tint = primaryRed) }
                    
                    IconButton(onClick = {}) { Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.White) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
            )
        },
        bottomBar = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(bgColor)
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().background(surfaceColor, RoundedCornerShape(32.dp)).padding(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(44.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(darkGray)
                            .clickable {
                            launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.AttachFile, contentDescription = "Attach", tint = primaryRed, modifier = Modifier.size(24.dp))
                    }
                    
                    Spacer(modifier = Modifier.width(8.dp))
                    
                    Box(modifier = Modifier.weight(1f)) {
                        if (messageText.isEmpty()) {
                            Text(if (editingMessage != null) "Edit message..." else "Type a message...", color = Color.Gray, fontSize = 16.sp)
                        }
                        BasicTextField(
                            value = messageText,
                            onValueChange = { messageText = it },
                            textStyle = TextStyle(color = Color.White, fontSize = 16.sp),
                            cursorBrush = SolidColor(primaryRed),
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                    
                    Icon(Icons.Default.Face, contentDescription = "Emoji", tint = primaryRed, modifier = Modifier.size(24.dp).clickable {
                        Toast.makeText(context, "Emoji keyboard opened", Toast.LENGTH_SHORT).show()
                    })
                    
                    Spacer(modifier = Modifier.width(12.dp))
                    
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(primaryRed)
                            .clickable {
                                if (messageText.isNotBlank()) {
                                    if (editingMessage != null) {
                                        viewModel.editMessage(editingMessage!!.id, messageText)
                                        editingMessage = null
                                    } else {
                                        viewModel.sendMessage(messageText)
                                    }
                                    messageText = ""
                                } else {
                                    // Send voice message
                                    viewModel.sendVoiceMessage("local_voice_path.m4a")
                                    Toast.makeText(context, "Voice message sent", Toast.LENGTH_SHORT).show()
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        if (messageText.isNotBlank() || editingMessage != null) {
                            Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                        } else {
                            Icon(Icons.Outlined.MicNone, contentDescription = "Voice", tint = Color.White)
                        }
                    }
                }
            }
        },
        containerColor = bgColor
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            reverseLayout = true
        ) {
            items(messages.reversed()) { msg ->
                val isMe = msg.senderId == currentUser?.uid
                val isDeletedForMe = msg.deletedFor.contains(currentUser?.uid)
                if (isDeletedForMe) return@items
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    horizontalArrangement = if (isMe) Arrangement.End else Arrangement.Start
                ) {
                    Column(
                        horizontalAlignment = if (isMe) Alignment.End else Alignment.Start
                    ) {
                        val isEffectivelyDeleted = msg.isDeleted
                
                Box(
                            modifier = Modifier
                                .background(
                                    color = if (isEffectivelyDeleted) Color.Transparent else if (isMe) primaryRed else darkGray,
                                    shape = RoundedCornerShape(
                                        topStart = 20.dp,
                                        topEnd = 20.dp,
                                        bottomStart = if (isMe) 20.dp else 4.dp,
                                        bottomEnd = if (isMe) 4.dp else 20.dp
                                    )
                                )
                                .border(if (isEffectivelyDeleted) 1.dp else 0.dp, if (isEffectivelyDeleted) Color.Gray else Color.Transparent, RoundedCornerShape(20.dp))
                                .combinedClickable(
                                    onClick = {},
                                    onLongClick = {
                                        if (!isEffectivelyDeleted) {
                                            selectedMessage = msg
                                        }
                                    }
                                )
                                .padding(horizontal = 16.dp, vertical = 10.dp)
                        ) {
                            if (isEffectivelyDeleted) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Block, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(text = "تم حذف هذه الرسالة", color = Color.Gray, fontSize = 14.sp)
                                }
                            } else if (msg.isVoice) {
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.clickable {
                                    if (msg.mediaUrl != null && !msg.isDeleted) {
                                        Toast.makeText(context, "Voice message downloaded and deleted from cloud", Toast.LENGTH_SHORT).show()
                                        viewModel.deleteMessage(msg.id, true)
                                    }
                                }) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.White, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Box(modifier = Modifier.width(100.dp).height(2.dp).background(Color.White.copy(alpha = 0.5f)))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("0:12", color = Color.White, fontSize = 12.sp)
                                }
                            } else {
                                Column {
                                    Text(text = msg.text, color = Color.White, fontSize = 15.sp)
                                    if (msg.isEdited) {
                                        Text(text = "Edited", color = Color.White.copy(alpha = 0.5f), fontSize = 10.sp, modifier = Modifier.align(Alignment.End))
                                    }
                                }
                            }
                        }
                        
                        // Show Reactions if any
                        if (!isEffectivelyDeleted && msg.reactions.isNotEmpty()) {
                            Row(modifier = Modifier.padding(top = 2.dp)) {
                                msg.reactions.values.distinct().forEach { emoji ->
                                    Text(text = emoji, fontSize = 14.sp, modifier = Modifier.background(Color(0xFF2C2C2E), CircleShape).padding(horizontal = 4.dp, vertical = 2.dp))
                                }
                            }
                        }
                        
                        val sdf = SimpleDateFormat("hh:mm a", Locale.getDefault())
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {
                            Text(sdf.format(Date(msg.timestamp)), fontSize = 11.sp, color = Color.Gray)
                            if (isMe) {
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.DoneAll, contentDescription = "Read", tint = primaryRed, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }
            
            item {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .background(surfaceColor, RoundedCornerShape(16.dp))
                            .padding(horizontal = 12.dp, vertical = 12.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Security, contentDescription = "Encrypted", tint = primaryRed, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Messages are end-to-end encrypted.\nYour privacy is our priority.", color = Color.LightGray, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Box(
                        modifier = Modifier
                            .background(surfaceColor, RoundedCornerShape(16.dp))
                            .padding(horizontal = 12.dp, vertical = 4.dp)
                    ) {
                        Text("Today", color = Color.White, fontSize = 12.sp)
                    }
                }
            }
        }
    }

    if (selectedMessage != null) {
        ModalBottomSheet(onDismissRequest = { selectedMessage = null }, containerColor = Color(0xFF1E1E1E)) {
            val msg = selectedMessage!!
            val isMe = msg.senderId == currentUser?.uid
            val isLastMessage = messages.firstOrNull { it.senderId == currentUser?.uid }?.id == msg.id
            
            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp)) {
                // Reactions
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    val emojis = listOf("👍", "❤️", "😂", "😮", "😢", "🙏")
                    emojis.forEach { emoji ->
                        Text(
                            text = emoji,
                            fontSize = 28.sp,
                            modifier = Modifier.clickable {
                                viewModel.reactToMessage(msg.id, emoji)
                                selectedMessage = null
                            }.padding(8.dp)
                        )
                    }
                }
                
                HorizontalDivider(color = Color.DarkGray)
                
                if (!msg.isVoice) {
                    ListItem(
                        headlineContent = { Text("Copy", color = Color.White) },
                        leadingContent = { Icon(Icons.Outlined.ContentCopy, contentDescription = null, tint = Color.White) },
                        colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                        modifier = Modifier.clickable {
                            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                            clipboard.setPrimaryClip(android.content.ClipData.newPlainText("message", msg.text))
                            Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                            selectedMessage = null
                        }
                    )
                }
                
                if (isMe && isLastMessage && !msg.isVoice) {
                    ListItem(
                        headlineContent = { Text("Edit", color = Color.White) },
                        leadingContent = { Icon(Icons.Outlined.Edit, contentDescription = null, tint = Color.White) },
                        colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                        modifier = Modifier.clickable {
                            editingMessage = msg
                            messageText = msg.text
                            selectedMessage = null
                        }
                    )
                }
                
                ListItem(
                    headlineContent = { Text("Delete", color = Color(0xFFE50914)) },
                    leadingContent = { Icon(Icons.Outlined.Delete, contentDescription = null, tint = Color(0xFFE50914)) },
                    colors = ListItemDefaults.colors(containerColor = Color.Transparent),
                    modifier = Modifier.clickable {
                        if (isMe) {
                            showDeleteConfirm = true
                        } else {
                            viewModel.deleteMessage(msg.id, false)
                            selectedMessage = null
                        }
                    }
                )
            }
        }
    }
    
    if (showDeleteConfirm && selectedMessage != null) {
        AlertDialog(
            onDismissRequest = { showDeleteConfirm = false },
            title = { Text("Delete Message", color = Color.White) },
            text = { Text("Who do you want to delete this message for?", color = Color.Gray) },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.deleteMessage(selectedMessage!!.id, true)
                    showDeleteConfirm = false
                    selectedMessage = null
                }) { Text("Delete for Everyone", color = Color(0xFFE50914)) }
            },
            dismissButton = {
                TextButton(onClick = {
                    viewModel.deleteMessage(selectedMessage!!.id, false)
                    showDeleteConfirm = false
                    selectedMessage = null
                }) { Text("Delete for Me", color = Color.White) }
            },
            containerColor = Color(0xFF1E1E1E)
        )
    }

}