import sys

new_ui = """
        if (!isCloudflare) {
            val displayTitle = when {
                isFailed || extractedServers.isNotEmpty() -> "اختر السيرفر"
                else -> "الاتصال بالسيرفر"
            }
            
            val displaySubtitle = when {
                isFailed -> "جاري الإتصال بالسيرفرات المتاحة..."
                isExtractingQuality -> "اختر جودة العرض المتاحة"
                extractedServers.isNotEmpty() -> "جاري جلب السيرفرات المتاحة..."
                isVerified || isNormal -> "تم الاتصال ..."
                else -> "جاري الاتصال..."
            }
            
            val displayIcon = when {
                isFailed -> androidx.compose.material.icons.Icons.Outlined.CloudOff
                extractedServers.isNotEmpty() && !isFailed -> if (isExtractingQuality) androidx.compose.material.icons.Icons.Outlined.Storage else androidx.compose.material.icons.Icons.Outlined.CloudDownload
                isVerified || isNormal -> androidx.compose.material.icons.Icons.Outlined.CloudDone
                else -> androidx.compose.material.icons.Icons.Outlined.CloudDownload
            }
            
            val iconTint = if (isFailed) Color(0xFFFF1111) else if (isVerified || isNormal) Color(0xFF00C853) else MaterialTheme.colorScheme.primary
            
            val isHorizontal = isLoading && !isCloudflare && extractedServers.isEmpty() && !isFailed
            
            Box(
                modifier = Modifier
                    .fillMaxWidth(0.95f)
                    .wrapContentHeight()
                    .clip(RoundedCornerShape(24.dp))
                    .background(Color(0xFF101014))
                    .border(1.dp, iconTint.copy(alpha = 0.3f), RoundedCornerShape(24.dp))
                    .clickable(
                        interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                        indication = null,
                        onClick = {}
                    )
            ) {
                Box(
                    modifier = Modifier
                        .matchParentSize()
                        .background(
                            androidx.compose.ui.graphics.Brush.radialGradient(
                                colors = listOf(iconTint.copy(alpha = 0.15f), Color.Transparent),
                                radius = 600f,
                                center = androidx.compose.ui.geometry.Offset(0f, 0f)
                            )
                        )
                )
                
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp)
                        .animateContentSize()
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .background(iconTint.copy(alpha = 0.15f), CircleShape)
                                .border(1.dp, iconTint.copy(alpha = 0.3f), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(displayIcon, contentDescription = null, tint = iconTint, modifier = Modifier.size(24.dp))
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column(modifier = Modifier.weight(1f)) {
                            Text(displayTitle, color = Color.White, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(displaySubtitle, color = iconTint.copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall)
                        }
                        
                        if (isHorizontal) {
                            Spacer(modifier = Modifier.width(16.dp))
                            val progress = (currentSiteIndex.toFloat() / safeSites.size.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f)
                            val animatedProgress by androidx.compose.animation.core.animateFloatAsState(targetValue = if (progress == 0f) 0.1f else progress)
                            Box(modifier = Modifier.weight(1.5f).height(6.dp).clip(CircleShape).background(Color(0xFF222222))) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth(animatedProgress)
                                        .fillMaxHeight()
                                        .background(iconTint)
                                )
                            }
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .background(Color(0xFF222225), CircleShape)
                                .border(1.dp, Color(0xFF333333), CircleShape)
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
                    }
                    
                    if (!isHorizontal) {
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        if (isFailed) {
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
                                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                                        color = Color(0xFFFF4444),
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
                                Text(stringResource(R.string.retry_again), color = Color.White, fontWeight = FontWeight.Bold)
                            }
                            
                            Spacer(modifier = Modifier.height(12.dp))
                            
                            Button(
                                onClick = { showOpenBrowserConfirmDialog = true },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF222225)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.OpenInBrowser, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.open_browser_manual), color = Color.LightGray, fontWeight = FontWeight.Medium)
                            }
                            
                            Spacer(modifier = Modifier.height(12.dp))
                            
                            Button(
                                onClick = { showSkipSiteConfirmDialog = true },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF222225)),
                                shape = RoundedCornerShape(24.dp)
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.Language, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.skip_current), color = Color.LightGray, fontWeight = FontWeight.Medium)
                            }
                            
                            if (showOpenBrowserConfirmDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showOpenBrowserConfirmDialog = false },
                                    title = { Text(stringResource(R.string.confirm_browser), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.confirm_open_browser), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                isManualBrowserOpen = true
                                                forceBypassComplete = false
                                                showOpenBrowserConfirmDialog = false
                                                isFailed = false
                                                isLoading = true
                                                currentSiteIndex = 0
                                                currentExtension = safeSites[0]
                                                android.webkit.CookieManager.getInstance().removeAllCookies(null)
                                                android.webkit.CookieManager.getInstance().flush()
                                                bypassStatus = "CLOUDFLARE"
                                                retryTrigger++
                                            }
                                        ) { Text(stringResource(R.string.yes_ar), color = MaterialTheme.colorScheme.primary) }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(onClick = { showOpenBrowserConfirmDialog = false }) { Text(stringResource(R.string.cancel_ar), color = MaterialTheme.colorScheme.onBackground) }
                                    }
                                )
                            }
                            if (showSkipSiteConfirmDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showSkipSiteConfirmDialog = false },
                                    title = { Text(stringResource(R.string.confirm_skip), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.confirm_skip_site), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showSkipSiteConfirmDialog = false
                                                if (currentSiteIndex < safeSites.size - 1) {
                                                    isFailed = false
                                                    isLoading = true
                                                    currentSiteIndex++
                                                    currentExtension = safeSites[currentSiteIndex]
                                                    bypassStatus = "CLOUDFLARE"
                                                    isManualBrowserOpen = false
                                                    forceBypassComplete = false
                                                    retryTrigger++
                                                } else {
                                                    showNoMoreExtensionsDialog = true
                                                }
                                            }
                                        ) { Text(stringResource(R.string.yes_ar), color = MaterialTheme.colorScheme.primary) }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(onClick = { showSkipSiteConfirmDialog = false }) { Text(stringResource(R.string.cancel_ar), color = MaterialTheme.colorScheme.onBackground) }
                                    }
                                )
                            }
                            if (showNoMoreExtensionsDialog) {
                                AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text(stringResource(R.string.no_sites_left), color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text(stringResource(R.string.failed_all_sites), color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) {
                                            Text(stringResource(R.string.close), color = MaterialTheme.colorScheme.primary)
                                        }
                                    }
                                )
                            }
                        } else if (selectedServerForQuality == null) {
                            LazyColumn(
                                modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                items(extractedServers) { server ->
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clip(RoundedCornerShape(16.dp))
                                            .background(Color(0xFF16161A))
                                            .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                            .clickable {
                                                if (extractedQualities.isNotEmpty() && selectedServerForQuality == server) {
                                                    // Already selected
                                                } else {
                                                    selectedServerForQuality = server
                                                    extractedQualities = emptyList()
                                                    isExtractingQuality = true
                                                    qualityExtractionMessage = "جاري استخراج الجودات المتاحة..."
                                                    
                                                    val finalUrl = extractedServerLinks[server] ?: ""
                                                    currentExtension.extractQualities(
                                                        serverName = server,
                                                        videoUrl = finalUrl,
                                                        onQualitiesExtracted = { qualities ->
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                if (selectedServerForQuality == server) {
                                                                    if (qualities.isEmpty()) {
                                                                        val dLink = extractedDownloadLinks[server] ?: ""
                                                                        val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                                            finalUrl
                                                                        } else if (dLink.isNotEmpty()) {
                                                                            dLink
                                                                        } else {
                                                                            finalUrl
                                                                        }
                                                                        onPlay(watchUrl, server, currentSiteName)
                                                                    } else {
                                                                        extractedQualities = qualities
                                                                        isExtractingQuality = false
                                                                        ServerStateStore.extractedQualities = qualities
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    )
                                                }
                                            }
                                            .padding(12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Box(
                                            modifier = Modifier.size(32.dp).background(MaterialTheme.colorScheme.primary.copy(alpha=0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                        }
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(server, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                        Spacer(modifier = Modifier.weight(1f))
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        } else {
                            if (isExtractingQuality) {
                                Box(modifier = Modifier.fillMaxWidth().height(150.dp), contentAlignment = Alignment.Center) {
                                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                LazyColumn(
                                    modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                    verticalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    items(extractedQualities) { quality ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(RoundedCornerShape(16.dp))
                                                .background(Color(0xFF16161A))
                                                .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                                .clickable {
                                                    onPlay(quality.url, selectedServerForQuality ?: "", currentSiteName)
                                                }
                                                .padding(12.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Box(
                                                modifier = Modifier.size(32.dp).background(Color(0x15FFFFFF), CircleShape),
                                                contentAlignment = Alignment.Center
                                            ) {
                                                Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                                            }
                                            Spacer(modifier = Modifier.width(16.dp))
                                            Text(quality.quality, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                            Spacer(modifier = Modifier.weight(1f))
                                            
                                            val badgeColor = when {
                                                quality.quality.contains("1080") || quality.quality.contains("FHD") -> Color(0xFFE91E63)
                                                quality.quality.contains("720") || quality.quality.contains("HD") -> Color(0xFF9C27B0)
                                                else -> Color(0xFF607D8B)
                                            }
                                            val badgeText = when {
                                                quality.quality.contains("1080") || quality.quality.contains("FHD") -> "FHD"
                                                quality.quality.contains("720") || quality.quality.contains("HD") -> "HD"
                                                else -> "SD"
                                            }
                                            Box(
                                                modifier = Modifier.background(badgeColor.copy(alpha=0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 8.dp, vertical = 4.dp)
                                            ) {
                                                Text(badgeText, color = badgeColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "يمكنك التبديل إلى سيرفر آخر لاحقاً",
                                    color = Color.Gray,
                                    fontSize = 12.sp,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth()
                                )
                            }
                        }
                    }
                }
            }
        }
"""

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    lines = f.readlines()

start_line = -1
for i, line in enumerate(lines):
    if "if (!isCloudflare) {" in line:
        start_line = i
        break

if start_line != -1:
    brace_count = 0
    in_block = False
    end_line = -1
    for i in range(start_line, len(lines)):
        if "{" in lines[i]:
            brace_count += lines[i].count("{")
            in_block = True
        if "}" in lines[i]:
            brace_count -= lines[i].count("}")
        if in_block and brace_count == 0:
            end_line = i
            break
            
    if end_line != -1:
        # Check imports to ensure we have required ones
        import_block = ""
        imports_needed = [
            "import androidx.compose.material.icons.outlined.CloudDownload",
            "import androidx.compose.material.icons.outlined.CloudDone",
            "import androidx.compose.material.icons.outlined.CloudOff",
            "import androidx.compose.material.icons.outlined.Storage",
            "import androidx.compose.material.icons.filled.Error",
            "import androidx.compose.material.icons.filled.Refresh",
            "import androidx.compose.material.icons.filled.OpenInBrowser",
            "import androidx.compose.material.icons.filled.Language",
            "import androidx.compose.material.icons.filled.PlayArrow",
            "import androidx.compose.animation.core.animateFloatAsState"
        ]
        
        # Replace the block
        res = "".join(lines[:start_line]) + new_ui + "".join(lines[end_line+1:])
        
        for imp in imports_needed:
            if imp not in res:
                res = res.replace("import androidx.compose.runtime.*", f"import androidx.compose.runtime.*\n{imp}")
                
        with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
            f.write(res)
        print("Replaced UI successfully!")
    else:
        print("End line not found!")
else:
    print("Start line not found!")

