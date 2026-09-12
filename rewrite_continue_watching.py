import re

with open('app/src/main/java/com/example/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

start_str = "fun ContinueWatchingCardShared(item: HistoryItem, onClick: () -> Unit) {"
start_idx = text.find(start_str)
if start_idx != -1:
    brace_count = 0
    end_idx = -1
    for i in range(start_idx + len(start_str) - 1, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i
                break
                
    new_func = """fun ContinueWatchingCardShared(item: HistoryItem, onClick: () -> Unit) {
    androidx.compose.foundation.layout.Box(
        modifier = androidx.compose.ui.Modifier
            .width(340.dp)
            .height(140.dp)
            .clip(androidx.compose.foundation.shape.RoundedCornerShape(16.dp))
            .background(androidx.compose.ui.graphics.Color(0xFF141414))
            .border(1.dp, androidx.compose.ui.graphics.Color(0xFFE50914).copy(alpha=0.3f), androidx.compose.foundation.shape.RoundedCornerShape(16.dp))
            .androidx.compose.foundation.clickable { onClick() }
    ) {
        androidx.compose.foundation.layout.Row(
            modifier = androidx.compose.ui.Modifier.fillMaxSize()
        ) {
            // Image Section
            androidx.compose.foundation.layout.Box(
                modifier = androidx.compose.ui.Modifier
                    .width(160.dp)
                    .fillMaxHeight()
                    .clip(androidx.compose.foundation.shape.RoundedCornerShape(16.dp))
            ) {
                coil.compose.AsyncImage(
                    model = item.posterUrl,
                    contentDescription = item.title,
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                    modifier = androidx.compose.ui.Modifier.fillMaxSize()
                )
                
                // Overlay to darken image slightly
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxSize()
                        .background(androidx.compose.ui.graphics.Color.Black.copy(alpha = 0.3f))
                )
                
                // HD Badge top left
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .padding(8.dp)
                        .align(androidx.compose.ui.Alignment.TopStart)
                        .border(1.dp, androidx.compose.ui.graphics.Color.White.copy(alpha=0.7f), androidx.compose.foundation.shape.RoundedCornerShape(4.dp))
                        .padding(horizontal=4.dp, vertical=2.dp)
                ) {
                    androidx.compose.material3.Text("HD", color = androidx.compose.ui.graphics.Color.White, fontSize = 10.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                }
                
                // Pause Icon bottom left (using two small boxes if Pause is unavailable, but let's try the icon)
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .padding(start = 12.dp, bottom = 20.dp)
                        .align(androidx.compose.ui.Alignment.BottomStart)
                        .size(28.dp)
                        .border(1.5.dp, androidx.compose.ui.graphics.Color.White, androidx.compose.foundation.shape.CircleShape)
                        .padding(6.dp),
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    androidx.compose.foundation.layout.Row(horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween, modifier = androidx.compose.ui.Modifier.width(8.dp).height(10.dp)) {
                        androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.width(2.5.dp).fillMaxHeight().background(androidx.compose.ui.graphics.Color.White))
                        androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.width(2.5.dp).fillMaxHeight().background(androidx.compose.ui.graphics.Color.White))
                    }
                }
                
                // Time text
                androidx.compose.material3.Text("32:14 / 1:54:20", color = androidx.compose.ui.graphics.Color.White, fontSize = 10.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold, modifier = androidx.compose.ui.Modifier.align(androidx.compose.ui.Alignment.BottomEnd).padding(bottom = 20.dp, end = 12.dp))
                
                // Progress Bar
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .align(androidx.compose.ui.Alignment.BottomStart)
                        .padding(start = 12.dp, end = 12.dp, bottom = 8.dp)
                        .fillMaxWidth()
                        .height(4.dp)
                        .clip(androidx.compose.foundation.shape.CircleShape)
                        .background(androidx.compose.ui.graphics.Color.White.copy(alpha=0.3f))
                ) {
                    androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.fillMaxWidth(0.3f).fillMaxHeight().background(androidx.compose.ui.graphics.Color(0xFFE50914)))
                }
            }
            
            // Text Section
            androidx.compose.foundation.layout.Column(
                modifier = androidx.compose.ui.Modifier
                    .weight(1f)
                    .padding(12.dp)
            ) {
                androidx.compose.material3.Text(
                    text = item.title, 
                    color = androidx.compose.ui.graphics.Color.White, 
                    fontSize = 18.sp, 
                    fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                    maxLines = 1,
                    overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                )
                androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.height(4.dp))
                androidx.compose.foundation.layout.Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                    androidx.compose.material3.Text("2023", color = androidx.compose.ui.graphics.Color.Gray, fontSize = 12.sp)
                    androidx.compose.material3.Text("  |  " + (if (item.isMovie) "فيلم" else "مسلسل") + "  |  ", color = androidx.compose.ui.graphics.Color.Gray, fontSize = 12.sp)
                    androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.border(1.dp, androidx.compose.ui.graphics.Color.Gray, androidx.compose.foundation.shape.RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                        androidx.compose.material3.Text("R", color = androidx.compose.ui.graphics.Color.Gray, fontSize = 10.sp)
                    }
                    androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.width(4.dp))
                    androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.border(1.dp, androidx.compose.ui.graphics.Color.Gray, androidx.compose.foundation.shape.RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                        androidx.compose.material3.Text("HD", color = androidx.compose.ui.graphics.Color.Gray, fontSize = 10.sp)
                    }
                }
                androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.height(8.dp))
                androidx.compose.material3.Text(
                    "A group of men fight for survival in a world where trust is a luxury.", 
                    color = androidx.compose.ui.graphics.Color.Gray, 
                    fontSize = 12.sp, 
                    lineHeight = 16.sp,
                    maxLines = 3, 
                    overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                )
            }
        }
        
        // Top Right Menu
        androidx.compose.material3.Icon(
            imageVector = androidx.compose.material.icons.Icons.Default.MoreVert,
            contentDescription = "Menu",
            tint = androidx.compose.ui.graphics.Color.Gray,
            modifier = androidx.compose.ui.Modifier
                .align(androidx.compose.ui.Alignment.TopEnd)
                .padding(8.dp)
                .size(24.dp)
                .background(androidx.compose.ui.graphics.Color.Black.copy(alpha=0.5f), androidx.compose.foundation.shape.CircleShape)
                .padding(2.dp)
        )
        
        // Bottom Right Play Button
        androidx.compose.foundation.layout.Box(
            modifier = androidx.compose.ui.Modifier
                .align(androidx.compose.ui.Alignment.BottomEnd)
                .padding(12.dp)
                .size(44.dp)
                .clip(androidx.compose.foundation.shape.CircleShape)
                .background(androidx.compose.ui.graphics.Color(0xFFE50914)),
            contentAlignment = androidx.compose.ui.Alignment.Center
        ) {
            androidx.compose.material3.Icon(
                imageVector = androidx.compose.material.icons.Icons.Default.PlayArrow, 
                contentDescription = "Play", 
                tint = androidx.compose.ui.graphics.Color.White,
                modifier = androidx.compose.ui.Modifier.size(28.dp)
            )
        }
    }"""
    
    text = text[:start_idx] + new_func + text[end_idx+1:]
    with open('app/src/main/java/com/example/ui/components/SharedUI.kt', 'w') as f:
        f.write(text)
    print("Rewrote ContinueWatchingCardShared")
else:
    print("Could not find function.")
