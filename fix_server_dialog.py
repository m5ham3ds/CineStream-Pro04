with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

import re
pattern = r'Row\(\s*modifier = Modifier\.fillMaxWidth\(\),\s*verticalAlignment = Alignment\.CenterVertically\s*\)\s*\{.*?Icon\(Icons\.Default\.Close, contentDescription = "إغلاق", tint = Color\.White, modifier = Modifier\.size\(16\.dp\)\).*?\}\s*\}'
match = re.search(pattern, content, re.DOTALL)
if match:
    new_box = """                    Box(
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Box(
                            modifier = Modifier
                                .align(Alignment.CenterStart)
                                .size(48.dp)
                                .background(iconTint.copy(alpha = 0.15f), CircleShape)
                                .border(1.dp, iconTint.copy(alpha = 0.3f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(displayIcon, contentDescription = null, tint = iconTint, modifier = Modifier.size(24.dp))
                        }
                        
                        Column(
                            modifier = Modifier.align(Alignment.Center).padding(horizontal = 56.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(displayTitle, color = Color.White, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, textAlign = androidx.compose.ui.text.style.TextAlign.Center, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(displaySubtitle, color = iconTint.copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall, textAlign = androidx.compose.ui.text.style.TextAlign.Center, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                            
                            if (isHorizontal) {
                                Spacer(modifier = Modifier.height(8.dp))
                                val progress = (currentSiteIndex.toFloat() / safeSites.size.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f)
                                val animatedProgress by androidx.compose.animation.core.animateFloatAsState(targetValue = if (progress == 0f) 0.1f else progress)
                                Box(modifier = Modifier.fillMaxWidth(0.6f).height(4.dp).clip(CircleShape).background(Color(0xFF222222))) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth(animatedProgress)
                                            .fillMaxHeight()
                                            .background(iconTint)
                                    )
                                }
                            }
                        }
                        
                        Box(
                            modifier = Modifier
                                .align(Alignment.CenterEnd)
                                .size(36.dp)
                                .background(Color(0xFF222225), CircleShape)
                                .border(1.dp, Color(0xFF333333), CircleShape)
                                .clip(CircleShape)
                                .clickable {
                                    if (isLoading || isExtractingQuality) {
                                        showCancelConfirmDialog = true
                                    } else {
                                        onDismiss()
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Close, contentDescription = "إغلاق", tint = Color.White, modifier = Modifier.size(16.dp))
                        }
                    }"""
    content = content.replace(match.group(0), new_box)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Failed")
