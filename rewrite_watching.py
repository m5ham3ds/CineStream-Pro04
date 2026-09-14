import re

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "r") as f:
    text = f.read()

import_lines = "import com.example.ui.components.rememberCardMediaDetail\nimport com.example.ui.components.CardMediaDetail\nimport kotlin.math.absoluteValue\nimport androidx.compose.ui.text.style.TextOverflow\n"
text = text.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\n" + import_lines)

start_idx = text.find("@Composable\nfun DetailedContinueWatchingCard")
if start_idx == -1:
    print("Could not find DetailedContinueWatchingCard")
    exit(1)

brace_count = 0
end_idx = -1
in_function = False
for i in range(start_idx, len(text)):
    if text[i] == '{':
        brace_count += 1
        in_function = True
    elif text[i] == '}':
        brace_count -= 1
        
    if in_function and brace_count == 0:
        end_idx = i + 1
        break

new_func = """@Composable
fun DetailedContinueWatchingCard(item: HistoryItem, onClick: () -> Unit) {
    val mediaDetail = rememberCardMediaDetail(item) ?: CardMediaDetail(
        title = item.title, year = "", rating = "", overview = "", backdropUrl = item.posterUrl, isMovie = item.isMovie
    )
    val typeText = if (mediaDetail.isMovie) stringResource(R.string.movies) else stringResource(R.string.series)
    val fakeProgress = (item.id.hashCode().absoluteValue % 100) / 100f
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(140.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha=0.5f), RoundedCornerShape(16.dp))
            .clickable { onClick() }
    ) {
        Row(modifier = Modifier.fillMaxSize()) {
            // Left Image Section
            Box(
                modifier = Modifier
                    .weight(0.4f)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(topStart = 16.dp, bottomStart = 16.dp))
            ) {
                AsyncImage(
                    model = mediaDetail.backdropUrl,
                    contentDescription = mediaDetail.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.2f)))
                
                // Top Left HD
                Box(
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .padding(8.dp)
                        .border(1.dp, Color.White.copy(alpha=0.8f), RoundedCornerShape(4.dp))
                        .padding(horizontal=4.dp, vertical=2.dp)
                ) {
                    Text("HD", color=Color.White, fontSize=10.sp, fontWeight=FontWeight.Bold)
                }
                
                // Bottom Left Pause Icon in circle
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(bottom=16.dp, start=8.dp)
                        .size(32.dp)
                        .border(1.dp, Color.White, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Filled.Pause,
                        contentDescription = "Pause",
                        tint = Color.White,
                        modifier = Modifier.size(16.dp)
                    )
                }
                
                // Bottom Right Time
                Text(
                    text = "32:14 / 1:54:20",
                    color = Color.White,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.align(Alignment.BottomEnd).padding(bottom=16.dp, end=8.dp)
                )
                
                // Progress Bar
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .fillMaxWidth()
                        .height(4.dp)
                        .background(Color.DarkGray)
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(fakeProgress.coerceAtLeast(0.1f))
                            .fillMaxHeight()
                            .background(MaterialTheme.colorScheme.primary)
                    )
                }
            }
            
            // Right Content Section
            Column(
                modifier = Modifier
                    .weight(0.6f)
                    .fillMaxHeight()
                    .padding(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.Top
                ) {
                    Text(
                        text = mediaDetail.title,
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f)
                    )
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Default.MoreVert,
                        contentDescription = "More",
                        tint = Color.Gray,
                        modifier = Modifier.size(20.dp)
                    )
                }
                
                Spacer(modifier = Modifier.height(4.dp))
                
                // Subtitle Row: 2023 | Movie | [R] [HD]
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "${mediaDetail.year} | $typeText | ", color = Color.Gray, fontSize = 12.sp)
                    Box(modifier = Modifier.border(1.dp, Color.Gray, RoundedCornerShape(2.dp)).padding(horizontal=2.dp, vertical=1.dp)) {
                        Text("R", color = Color.Gray, fontSize = 10.sp)
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.border(1.dp, Color.Gray, RoundedCornerShape(2.dp)).padding(horizontal=2.dp, vertical=1.dp)) {
                        Text("HD", color = Color.Gray, fontSize = 10.sp)
                    }
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = mediaDetail.overview,
                    color = Color.Gray,
                    fontSize = 12.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
            }
        }
        
        // Big Yellow FAB-like play button at bottom right
        Box(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(end = 12.dp, bottom = 12.dp)
                .size(48.dp)
                .background(MaterialTheme.colorScheme.primary, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = androidx.compose.material.icons.Icons.Filled.PlayArrow,
                contentDescription = "Play",
                tint = Color.White,
                modifier = Modifier.size(28.dp)
            )
        }
    }
}
"""

text = text[:start_idx] + new_func + text[end_idx:]

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "w") as f:
    f.write(text)
