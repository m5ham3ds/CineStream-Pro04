import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

start_marker = "HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))"
# find the LAST occurrence of start_marker
start_idx = text.rfind(start_marker)
end_marker = "    ) {\n        androidx.compose.runtime.CompositionLocalProvider"
end_idx = text.find(end_marker, start_idx)

replacement = """HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp))
                
                // Bottom Area (Logout)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 16.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surface)
                            .clickable { 
                                scope.launch { drawerState.close() }
                                showLogoutDialog = true
                            }
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) stringResource(R.string.login) else stringResource(R.string.logout), color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
"""

new_text = text[:start_idx] + replacement + text[end_idx:]

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(new_text)

