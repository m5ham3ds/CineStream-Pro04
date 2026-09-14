import re

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "r") as f:
    text = f.read()

start_idx = text.find("@Composable\nfun ContinueWatchingCardShared")
if start_idx == -1:
    print("Could not find function")
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

if end_idx == -1:
    print("Could not find end of function")
    exit(1)

new_func = """@Composable
fun ContinueWatchingCardShared(item: com.example.data.model.HistoryItem, onClick: () -> Unit) {
    val mediaDetail = rememberCardMediaDetail(item) ?: CardMediaDetail(
        title = item.title, year = "", rating = "", overview = "", backdropUrl = item.posterUrl, isMovie = item.isMovie
    )
    val typeText = if (mediaDetail.isMovie) stringResource(R.string.movies) else stringResource(R.string.series)
    
    Box(
        modifier = Modifier
            .width(340.dp)
            .height(130.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .clickable { onClick() }
    ) {
        Row(modifier = Modifier.fillMaxSize()) {
            // Left Image Section
            Box(
                modifier = Modifier
                    .weight(0.45f)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(topStart = 16.dp, bottomStart = 16.dp))
            ) {
                AsyncImage(
                    model = mediaDetail.backdropUrl,
                    contentDescription = mediaDetail.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                // Dark overlay
                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.3f)))
                
                // Center Play Triangle
                Icon(
                    imageVector = androidx.compose.material.icons.Icons.Filled.PlayArrow,
                    contentDescription = "Play",
                    tint = Color.White,
                    modifier = Modifier.align(Alignment.Center).size(36.dp)
                )
                
                // Bottom Left Type Badge
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(8.dp)
                        .clip(RoundedCornerShape(6.dp))
                        .background(Color.Black.copy(alpha = 0.6f))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(text = typeText, color = Color.White, fontSize = 11.sp)
                }
            }
            
            // Right Content Section
            Column(
                modifier = Modifier
                    .weight(0.55f)
                    .fillMaxHeight()
                    .padding(start = 12.dp, top = 12.dp, bottom = 12.dp, end = 12.dp),
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Text(
                        text = typeText,
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = mediaDetail.title,
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = androidx.compose.material.icons.Icons.Filled.Star,
                            contentDescription = "Rating",
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(text = mediaDetail.rating, color = Color.White, fontSize = 12.sp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(text = mediaDetail.year, color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Box(
                            modifier = Modifier
                                .border(1.dp, Color.Gray, RoundedCornerShape(4.dp))
                                .padding(horizontal = 4.dp, vertical = 2.dp)
                        ) {
                            Text(text = "16+", color = Color.Gray, fontSize = 10.sp)
                        }
                    }
                }
            }
        }
        
        // Right Edge Play Button Box
        Box(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(end = 12.dp)
                .size(48.dp)
                .border(2.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(12.dp))
                .clickable { onClick() },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = androidx.compose.material.icons.Icons.Filled.PlayArrow,
                contentDescription = "Play",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(28.dp)
            )
        }
    }
}
"""

text = text[:start_idx] + new_func + text[end_idx:]

with open("app/src/main/java/com/example/ui/components/SharedUI.kt", "w") as f:
    f.write(text)
