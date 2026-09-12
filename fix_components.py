import re

def fix_components(filepath):
    with open(filepath, 'r') as f:
        text = f.read()

    # Revert the broken ContinueWatchingCardShared
    # We will just write a new one
    new_func = """@Composable
fun ContinueWatchingCardShared(item: HistoryItem, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .width(340.dp)
            .height(140.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF141414))
            .border(1.dp, Color(0xFFE50914).copy(alpha=0.3f), RoundedCornerShape(16.dp))
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.fillMaxSize()
        ) {
            // Image Section
            Box(
                modifier = Modifier
                    .width(160.dp)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(16.dp))
            ) {
                AsyncImage(
                    model = item.posterUrl,
                    contentDescription = item.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                
                // Overlay to darken image slightly
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.3f))
                )
                
                // HD Badge top left
                Box(
                    modifier = Modifier
                        .padding(8.dp)
                        .align(Alignment.TopStart)
                        .border(1.dp, Color.White.copy(alpha=0.7f), RoundedCornerShape(4.dp))
                        .padding(horizontal=4.dp, vertical=2.dp)
                ) {
                    Text("HD", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
                
                // Pause Icon bottom left
                Box(
                    modifier = Modifier
                        .padding(start = 12.dp, bottom = 20.dp)
                        .align(Alignment.BottomStart)
                        .size(28.dp)
                        .border(1.5.dp, Color.White, CircleShape)
                        .padding(6.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.width(8.dp).height(10.dp)) {
                        Box(modifier = Modifier.width(2.5.dp).fillMaxHeight().background(Color.White))
                        Box(modifier = Modifier.width(2.5.dp).fillMaxHeight().background(Color.White))
                    }
                }
                
                // Time text
                Text("32:14 / 1:54:20", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.BottomEnd).padding(bottom = 20.dp, end = 12.dp))
                
                // Progress Bar
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 12.dp, end = 12.dp, bottom = 8.dp)
                        .fillMaxWidth()
                        .height(4.dp)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha=0.3f))
                ) {
                    Box(modifier = Modifier.fillMaxWidth(0.3f).fillMaxHeight().background(Color(0xFFE50914)))
                }
            }
            
            // Text Section
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(12.dp)
            ) {
                Text(
                    text = item.title, 
                    color = Color.White, 
                    fontSize = 18.sp, 
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("2023", color = Color.Gray, fontSize = 12.sp)
                    Text("  |  " + (if (item.isMovie) "فيلم" else "مسلسل") + "  |  ", color = Color.Gray, fontSize = 12.sp)
                    Box(modifier = Modifier.border(1.dp, Color.Gray, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                        Text("R", color = Color.Gray, fontSize = 10.sp)
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Box(modifier = Modifier.border(1.dp, Color.Gray, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                        Text("HD", color = Color.Gray, fontSize = 10.sp)
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    "A group of men fight for survival in a world where trust is a luxury.", 
                    color = Color.Gray, 
                    fontSize = 12.sp, 
                    lineHeight = 16.sp,
                    maxLines = 3, 
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        
        // Top Right Menu
        Icon(
            imageVector = Icons.Default.MoreVert,
            contentDescription = "Menu",
            tint = Color.Gray,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(8.dp)
                .size(24.dp)
                .background(Color.Black.copy(alpha=0.5f), CircleShape)
                .padding(2.dp)
        )
        
        // Bottom Right Play Button
        Box(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(12.dp)
                .size(44.dp)
                .clip(CircleShape)
                .background(Color(0xFFE50914)),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.PlayArrow, 
                contentDescription = "Play", 
                tint = Color.White,
                modifier = Modifier.size(28.dp)
            )
        }
    }
}
"""

    start_idx = text.find("fun ContinueWatchingCardShared")
    if start_idx != -1:
        # Need to include the @Composable
        comp_idx = text.rfind("@Composable", 0, start_idx)
        if comp_idx != -1 and start_idx - comp_idx < 30:
            start_idx = comp_idx
            
        brace_count = 0
        end_idx = -1
        # find first {
        first_brace = text.find('{', start_idx)
        brace_count = 1
        for i in range(first_brace + 1, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        text = text[:start_idx] + new_func + text[end_idx+1:]
        
    with open(filepath, 'w') as f:
        f.write(text)


def fix_section(filepath, name):
    with open(filepath, 'r') as f:
        text = f.read()

    new_func = f"""@Composable
fun {name}(title: String, onSeeAllClick: (() -> Unit)? = null) {{
    val parts = title.split(" ", limit = 2)
    val firstWord = parts.getOrNull(0) ?: ""
    val rest = parts.getOrNull(1) ?: ""

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {{
        Column {{
            Row {{
                Text(
                    text = firstWord,
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                if (rest.isNotEmpty()) {{
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = rest,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFFE50914)
                    )
                }}
            }}
            Spacer(modifier = Modifier.height(4.dp))
            Box(
                modifier = Modifier
                    .width(28.dp)
                    .height(3.dp)
                    .clip(RoundedCornerShape(1.5.dp))
                    .background(Color(0xFFE50914))
            )
        }}
        
        if (onSeeAllClick != null) {{
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.clickable {{ onSeeAllClick() }}
            ) {{
                Text(
                    text = stringResource(R.string.see_all),
                    style = MaterialTheme.typography.labelLarge,
                    color = Color(0xFFE50914)
                )
                Spacer(modifier = Modifier.width(4.dp))
                Icon(
                    imageVector = Icons.Default.KeyboardArrowRight,
                    contentDescription = "See All",
                    tint = Color(0xFFE50914),
                    modifier = Modifier.size(16.dp)
                )
            }}
        }}
    }}
}}
"""

    start_idx = text.find(f"fun {name}")
    if start_idx != -1:
        comp_idx = text.rfind("@Composable", 0, start_idx)
        if comp_idx != -1 and start_idx - comp_idx < 30:
            start_idx = comp_idx
            
        first_brace = text.find('{', start_idx)
        brace_count = 1
        end_idx = -1
        for i in range(first_brace + 1, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
                    
        text = text[:start_idx] + new_func + text[end_idx+1:]
        
    with open(filepath, 'w') as f:
        f.write(text)


fix_components('app/src/main/java/com/example/ui/components/SharedUI.kt')
fix_section('app/src/main/java/com/example/ui/components/SharedUI.kt', 'SectionTitleShared')
fix_section('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt', 'SectionTitle')
