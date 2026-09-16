import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# 1. Add showCancelConfirmDialog
cancel_dialog = """
    if (showCancelConfirmDialog) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showCancelConfirmDialog = false },
            title = { Text("إلغاء العملية", color = MaterialTheme.colorScheme.onBackground) },
            text = { Text("هل أنت متأكد أنك تود إلغاء العملية؟", color = Color.LightGray) },
            containerColor = Color(0xFF222225),
            confirmButton = {
                androidx.compose.material3.TextButton(
                    onClick = {
                        showCancelConfirmDialog = false
                        onDismiss()
                    }
                ) { Text("نعم", color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(
                    onClick = { showCancelConfirmDialog = false }
                ) { Text("لا", color = MaterialTheme.colorScheme.primary) }
            }
        )
    }
"""

# Insert before Dialog(
c = c.replace("    Dialog(", cancel_dialog + "    Dialog(")

# 2. Modify isFailed UI
failed_ui_target = """                        if (isFailed) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFF220000))
                                    .border(1.dp, Color(0x33FF1111), RoundedCornerShape(12.dp))
                                    .padding(16.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Error, contentDescription = null, tint = Color(0xFFFF1111), modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text(
                                        text = "فشل في العثور على سيرفرات. يرجى تجربة موقع آخر أو تفعيل وضع التصفح اليدوي لتخطي الحماية.",
                                        color = Color(0xFFFF8888),
                                        style = MaterialTheme.typography.bodySmall,
                                        lineHeight = 18.sp
                                    )
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(24.dp))
                            
                            Button(
                                onClick = {
                                    isFailed = false
                                    isLoading = true
                                    currentSiteIndex = 0
                                    currentExtension = safeSites[0]
                                    retryTrigger++
                                },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF1111)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.Refresh, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("إعادة المحاولة", color = Color.White, fontWeight = FontWeight.Bold)
                            }
                        } else {"""

failed_ui_replace = """                        if (isFailed) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.2f))
                                    .border(1.dp, MaterialTheme.colorScheme.error.copy(alpha = 0.3f), RoundedCornerShape(12.dp))
                                    .padding(16.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Error, contentDescription = null, tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text(
                                        text = "لم يتم العثور على هذا العمل في هذا الموقع.",
                                        color = MaterialTheme.colorScheme.onErrorContainer,
                                        style = MaterialTheme.typography.bodyMedium,
                                        lineHeight = 18.sp
                                    )
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(24.dp))
                            
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(12.dp)
                            ) {
                                Button(
                                    onClick = { showCancelConfirmDialog = true },
                                    modifier = Modifier.weight(1f).height(48.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333)),
                                    shape = RoundedCornerShape(24.dp)
                                ) {
                                    Text("إلغاء", color = Color.White, fontWeight = FontWeight.Bold)
                                }
                                
                                Button(
                                    onClick = { showSkipSiteConfirmDialog = true },
                                    modifier = Modifier.weight(1f).height(48.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                    shape = RoundedCornerShape(24.dp)
                                ) {
                                    Text("تجربة موقع آخر", color = MaterialTheme.colorScheme.onPrimary, fontWeight = FontWeight.Bold)
                                }
                            }
                        } else {"""

c = c.replace(failed_ui_target, failed_ui_replace)


# 3. Add "Try another site" below server list
server_list_bottom_target = """                                }
                            }
                        } else {
                            if (isExtractingQuality) {"""
server_list_bottom_replace = """                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "تجربة موقع آخر",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth().clickable { showSkipSiteConfirmDialog = true }.padding(8.dp)
                                )
                            }
                        } else {
                            if (isExtractingQuality) {"""
c = c.replace(server_list_bottom_target, server_list_bottom_replace)


# 4. Modify quality list bottom text to "Switch server"
quality_bottom_target = """                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "يمكنك التبديل إلى سيرفر آخر لاحقاً",
                                    color = Color.Gray,
                                    fontSize = 12.sp,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth()
                                )"""
quality_bottom_replace = """                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "تبديل السيرفر",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth().clickable {
                                        isExtractingQuality = false
                                        extractedQualities = emptyList()
                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                        selectedServerForQuality = null
                                    }.padding(8.dp)
                                )"""
c = c.replace(quality_bottom_target, quality_bottom_replace)

# 5. Make sure the "No more extensions" dialog has a way to navigate
no_ext_dialog_target = """                            if (showNoMoreExtensionsDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text(stringResource(R.string.no_more_sites), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.all_sites_failed), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) { Text(stringResource(R.string.ok), color = MaterialTheme.colorScheme.primary) }
                                    }
                                )
                            }"""

no_ext_dialog_replace = """                            if (showNoMoreExtensionsDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text(stringResource(R.string.no_more_sites), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.all_sites_failed) + "\\nهل تود الذهاب لصفحة الإضافات؟", color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                                onNavigateToExtensions()
                                            }
                                        ) { Text("الذهاب للإضافات", color = MaterialTheme.colorScheme.primary) }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) { Text("إغلاق", color = Color.Gray) }
                                    }
                                )
                            }"""
c = c.replace(no_ext_dialog_target, no_ext_dialog_replace)


with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

