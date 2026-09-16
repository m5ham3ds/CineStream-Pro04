import re

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

target = """fun DownloadSettingsDialog(
    maxConcurrentDownloads: Int,
    maxSegments: Int,
    downloadNetwork: Int,
    onMaxConcurrentChanged: (Int) -> Unit,
    onMaxSegmentsChanged: (Int) -> Unit,
    onNetworkChanged: (Int) -> Unit,
    onDismiss: () -> Unit
) {"""

# Find the end of the DownloadSettingsDialog block.
# We will use regex to replace from DownloadSettingsDialog to the end of NetworkOption

match = re.search(r'fun DownloadSettingsDialog\(.*?\n\)\s*\{.*?fun NetworkOption.*?\}\n\}', content, re.DOTALL)

# Let's write the new replacement code
new_code = """import androidx.compose.material.Slider
import androidx.compose.material.SliderDefaults

@Composable
fun DownloadSettingsDialog(
    maxConcurrentDownloads: Int,
    maxSegments: Int,
    downloadNetwork: Int,
    onMaxConcurrentChanged: (Int) -> Unit,
    onMaxSegmentsChanged: (Int) -> Unit,
    onNetworkChanged: (Int) -> Unit,
    onDismiss: () -> Unit
) {
    androidx.compose.ui.window.Dialog(
        onDismissRequest = onDismiss,
        properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)
    ) {
        val darkBg = Color(0xFF0F0F11)
        val cardBg = Color(0xFF19191B)
        val redPrimary = Color(0xFFE50914)
        
        Box(
            modifier = Modifier
                .fillMaxWidth(0.9f)
                .clip(RoundedCornerShape(24.dp))
                .background(darkBg)
                .border(1.dp, redPrimary.copy(alpha = 0.3f), RoundedCornerShape(24.dp))
                .padding(24.dp)
        ) {
            Column {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFF1C1C1E))
                                .border(1.dp, redPrimary, RoundedCornerShape(12.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Outlined.FileDownload, contentDescription = null, tint = redPrimary, modifier = Modifier.size(24.dp))
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(stringResource(R.string.downloads_settings), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF2C2C2E))
                            .clickable { onDismiss() },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.Close, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))

                // Max Concurrent
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(cardBg)
                        .padding(16.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Layers, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(stringResource(R.string.max_concurrent_downloads), color = Color.LightGray, fontSize = 14.sp, modifier = Modifier.weight(1f))
                        Text(maxConcurrentDownloads.toString(), color = redPrimary, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    androidx.compose.material.Slider(
                        value = maxConcurrentDownloads.toFloat(),
                        onValueChange = { onMaxConcurrentChanged(it.toInt()) },
                        valueRange = 1f..5f,
                        steps = 3,
                        colors = androidx.compose.material.SliderDefaults.colors(
                            thumbColor = Color.White,
                            activeTrackColor = redPrimary,
                            inactiveTrackColor = Color(0xFF2C2C2E),
                            activeTickColor = Color.Transparent,
                            inactiveTickColor = Color.Transparent
                        )
                    )
                    Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        for (i in 1..5) {
                            Text(i.toString(), color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Max Segments
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(cardBg)
                        .padding(16.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Movie, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(stringResource(R.string.max_segments_per_download), color = Color.LightGray, fontSize = 14.sp, modifier = Modifier.weight(1f))
                        Text(maxSegments.toString(), color = redPrimary, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    val segmentOptions = listOf(5, 10, 20, 50)
                    val closestIndex = segmentOptions.indexOfMinByOrNull { kotlin.math.abs(it - maxSegments) } ?: 0
                    
                    androidx.compose.material.Slider(
                        value = closestIndex.toFloat(),
                        onValueChange = { onMaxSegmentsChanged(segmentOptions[it.toInt()]) },
                        valueRange = 0f..(segmentOptions.size - 1).toFloat(),
                        steps = segmentOptions.size - 2,
                        colors = androidx.compose.material.SliderDefaults.colors(
                            thumbColor = Color.White,
                            activeTrackColor = redPrimary,
                            inactiveTrackColor = Color(0xFF2C2C2E),
                            activeTickColor = Color.Transparent,
                            inactiveTickColor = Color.Transparent
                        )
                    )
                    Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        segmentOptions.forEach {
                            Text(it.toString(), color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Network
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(cardBg)
                        .padding(16.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 16.dp)) {
                        Icon(Icons.Default.Wifi, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(20.dp))
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Download Network", color = Color.LightGray, fontSize = 14.sp)
                    }
                    
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        NetworkOption(
                            modifier = Modifier.weight(1.2f),
                            title = "All",
                            subtitle = "WiFi & Cellular",
                            isSelected = downloadNetwork == 0,
                            onClick = { onNetworkChanged(0) }
                        )
                        NetworkOption(
                            modifier = Modifier.weight(1f),
                            title = "Wi-Fi Only",
                            subtitle = null,
                            isSelected = downloadNetwork == 1,
                            onClick = { onNetworkChanged(1) }
                        )
                        NetworkOption(
                            modifier = Modifier.weight(1f),
                            title = "Cellular Only",
                            subtitle = null,
                            isSelected = downloadNetwork == 2,
                            onClick = { onNetworkChanged(2) }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))

                Button(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = redPrimary),
                    shape = RoundedCornerShape(percent = 50)
                ) {
                    Text(stringResource(R.string.done), color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
fun NetworkOption(modifier: Modifier = Modifier, title: String, subtitle: String?, isSelected: Boolean, onClick: () -> Unit) {
    val bgColor = if (isSelected) Color(0xFF2B1114) else Color(0xFF141416)
    val borderColor = if (isSelected) Color(0xFFE50914) else Color(0xFF2C2C2E)
    val iconColor = if (isSelected) Color(0xFFE50914) else Color(0xFF555555)

    Row(
        modifier = modifier
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .border(1.dp, borderColor, RoundedCornerShape(12.dp))
            .clickable { onClick() }
            .padding(vertical = 12.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Start
    ) {
        Icon(
            if (isSelected) Icons.Default.RadioButtonChecked else Icons.Default.RadioButtonUnchecked,
            contentDescription = null,
            tint = iconColor,
            modifier = Modifier.size(18.dp)
        )
        Spacer(modifier = Modifier.width(6.dp))
        Column(verticalArrangement = Arrangement.Center) {
            Text(title, color = if (isSelected) Color.White else Color.LightGray, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
            if (subtitle != null) {
                Text(subtitle, color = Color.Gray, fontSize = 10.sp, maxLines = 1)
            }
        }
    }
}"""

# Find start and end indices
start_idx = content.find("fun DownloadSettingsDialog(")
if start_idx != -1:
    end_idx = content.find("inline fun <T, R : Comparable<R>> Iterable<T>.indexOfMinByOrNull")
    if end_idx != -1:
        new_content = content[:start_idx] + new_code + "\n\n" + content[end_idx:]
        with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
            f.write(new_content)
        print("Success")
    else:
        print("Could not find end index")
else:
    print("Could not find start index")
