import re

with open("app/src/main/java/com/example/ui/components/CineStreamHeader.kt", "r") as f:
    c = f.read()

target1 = """@Composable
fun CineStreamHeader(
    onProfileClick: () -> Unit,
    onSearchClick: () -> Unit,
    onMenuClick: () -> Unit
) {"""

replacement1 = """import androidx.compose.runtime.*
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.screens.notifications.NotificationsViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import androidx.compose.ui.text.style.TextOverflow

@Composable
fun CineStreamHeader(
    onProfileClick: () -> Unit,
    onSearchClick: () -> Unit,
    onMenuClick: () -> Unit,
    onNotificationsClick: () -> Unit = {},
    notificationsViewModel: NotificationsViewModel = viewModel()
) {
    val unreadCount by notificationsViewModel.unreadCount.collectAsState()
    val notifications by notificationsViewModel.notifications.collectAsState()
    var showNotificationsDropdown by remember { mutableStateOf(false) }
"""

c = c.replace(target1, replacement1)

target2 = """                // Notifications
                Box(
                    modifier = Modifier
                        .size(46.dp)
                        .clip(CircleShape)
                        .background(bgDark)
                        .border(1.5.dp, iconBorder, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    IconButton(onClick = { /* TODO */ }) {
                        Box {
                            Icon(
                                imageVector = Icons.Default.Notifications,
                                contentDescription = "Notifications",
                                tint = MaterialTheme.colorScheme.onBackground,
                                modifier = Modifier.size(24.dp)
                            )
                            // Notification badge with glow
                            Box(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .offset(x = 6.dp, y = (-4).dp)
                            ) {
                                // Glow behind badge
                                Box(
                                    modifier = Modifier
                                        .size(22.dp)
                                        .background(Brush.radialGradient(listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.6f), Color.Transparent)), CircleShape)
                                        .align(Alignment.Center)
                                )
                                Box(
                                    modifier = Modifier
                                        .size(18.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.primary)
                                        .align(Alignment.Center),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("1", color = androidx.compose.ui.graphics.Color.White, fontSize = 11.sp, fontWeight = FontWeight.ExtraBold)
                                }
                            }
                        }
                    }
                }"""

replacement2 = """                // Notifications
                Box(
                    modifier = Modifier
                        .size(46.dp)
                        .clip(CircleShape)
                        .background(bgDark)
                        .border(1.5.dp, iconBorder, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    IconButton(onClick = { showNotificationsDropdown = true }) {
                        Box {
                            Icon(
                                imageVector = Icons.Default.Notifications,
                                contentDescription = "Notifications",
                                tint = MaterialTheme.colorScheme.onBackground,
                                modifier = Modifier.size(24.dp)
                            )
                            if (unreadCount > 0) {
                                Box(
                                    modifier = Modifier
                                        .align(Alignment.TopEnd)
                                        .offset(x = 6.dp, y = (-4).dp)
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .size(22.dp)
                                            .background(Brush.radialGradient(listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.6f), Color.Transparent)), CircleShape)
                                            .align(Alignment.Center)
                                    )
                                    Box(
                                        modifier = Modifier
                                            .size(18.dp)
                                            .clip(CircleShape)
                                            .background(MaterialTheme.colorScheme.primary)
                                            .align(Alignment.Center),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(if (unreadCount > 9) "9+" else unreadCount.toString(), color = androidx.compose.ui.graphics.Color.White, fontSize = 11.sp, fontWeight = FontWeight.ExtraBold)
                                    }
                                }
                            }
                        }
                    }
                    
                    DropdownMenu(
                        expanded = showNotificationsDropdown,
                        onDismissRequest = { showNotificationsDropdown = false },
                        modifier = Modifier
                            .width(300.dp)
                            .background(MaterialTheme.colorScheme.surface)
                    ) {
                        if (notifications.isEmpty()) {
                            DropdownMenuItem(
                                text = { Text("No notifications yet", color = MaterialTheme.colorScheme.onSurfaceVariant) },
                                onClick = { showNotificationsDropdown = false; onNotificationsClick() }
                            )
                        } else {
                            val formatter = SimpleDateFormat("hh:mm a", Locale.getDefault())
                            notifications.take(3).forEach { notif ->
                                DropdownMenuItem(
                                    text = { 
                                        Column {
                                            Text(notif.title, fontWeight = if (notif.isRead) FontWeight.Normal else FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                            Text(notif.message, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                        }
                                    },
                                    onClick = {
                                        showNotificationsDropdown = false
                                        onNotificationsClick()
                                    }
                                )
                            }
                            if (notifications.size > 3) {
                                androidx.compose.material3.HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
                                DropdownMenuItem(
                                    text = { Text("View all notifications", color = MaterialTheme.colorScheme.primary, textAlign = androidx.compose.ui.text.style.TextAlign.Center, modifier = Modifier.fillMaxWidth()) },
                                    onClick = { showNotificationsDropdown = false; onNotificationsClick() }
                                )
                            }
                        }
                    }
                }"""

c = c.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/components/CineStreamHeader.kt", "w") as f:
    f.write(c)

