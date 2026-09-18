import re

file_path = "app/src/main/java/com/example/ui/screens/social/ChatScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

old_actions = """                actions = {
                    IconButton(onClick = {}) { Icon(Icons.Default.Phone, contentDescription = "Call", tint = primaryRed) }
                    
                    IconButton(onClick = {}) { Icon(Icons.Default.MoreVert, contentDescription = "More", tint = MaterialTheme.colorScheme.onBackground) }
                },"""

new_actions = """                actions = {
                    otherUser?.let { targetUser ->
                        androidx.compose.ui.viewinterop.AndroidView(
                            factory = { ctx ->
                                val btn = com.zegocloud.uikit.prebuilt.call.invite.widget.ZegoSendCallInvitationButton(ctx)
                                btn.setIsVideoCall(false)
                                btn.setInvitees(listOf(com.zegocloud.uikit.service.defines.ZegoUIKitUser(targetUser.uid, targetUser.displayName ?: targetUser.username)))
                                btn
                            },
                            modifier = Modifier.size(48.dp).padding(8.dp)
                        )
                        androidx.compose.ui.viewinterop.AndroidView(
                            factory = { ctx ->
                                val btn = com.zegocloud.uikit.prebuilt.call.invite.widget.ZegoSendCallInvitationButton(ctx)
                                btn.setIsVideoCall(true)
                                btn.setInvitees(listOf(com.zegocloud.uikit.service.defines.ZegoUIKitUser(targetUser.uid, targetUser.displayName ?: targetUser.username)))
                                btn
                            },
                            modifier = Modifier.size(48.dp).padding(8.dp)
                        )
                    }
                    
                    IconButton(onClick = {}) { Icon(Icons.Default.MoreVert, contentDescription = "More", tint = MaterialTheme.colorScheme.onBackground) }
                },"""

content = content.replace(old_actions, new_actions)

with open(file_path, "w") as f:
    f.write(content)

