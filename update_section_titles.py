import re

def rewrite_file(filepath, func_name):
    with open(filepath, 'r') as f:
        text = f.read()
    
    start_str = f"fun {func_name}(title: String, onSeeAllClick: (() -> Unit)? = null) {{"
    
    start_idx = text.find(start_str)
    if start_idx == -1:
        print(f"Could not find {func_name} in {filepath}")
        return
        
    # Find matching closing brace
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
                
    new_func = f"""fun {func_name}(title: String, onSeeAllClick: (() -> Unit)? = null) {{
    val parts = title.split(" ", limit = 2)
    val firstWord = parts.getOrNull(0) ?: ""
    val rest = parts.getOrNull(1) ?: ""

    androidx.compose.foundation.layout.Row(
        modifier = androidx.compose.ui.Modifier
            .androidx.compose.foundation.layout.fillMaxWidth()
            .androidx.compose.foundation.layout.padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween,
        verticalAlignment = androidx.compose.ui.Alignment.CenterVertically
    ) {{
        androidx.compose.foundation.layout.Column {{
            androidx.compose.foundation.layout.Row {{
                androidx.compose.material3.Text(
                    text = firstWord,
                    style = androidx.compose.material3.MaterialTheme.typography.titleLarge,
                    fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                    color = androidx.compose.ui.graphics.Color.White
                )
                if (rest.isNotEmpty()) {{
                    androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.width(6.dp))
                    androidx.compose.material3.Text(
                        text = rest,
                        style = androidx.compose.material3.MaterialTheme.typography.titleLarge,
                        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                        color = androidx.compose.ui.graphics.Color(0xFFE50914)
                    )
                }}
            }}
            androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.height(4.dp))
            androidx.compose.foundation.layout.Box(
                modifier = androidx.compose.ui.Modifier
                    .androidx.compose.foundation.layout.width(28.dp)
                    .androidx.compose.foundation.layout.height(3.dp)
                    .androidx.compose.ui.draw.clip(androidx.compose.foundation.shape.RoundedCornerShape(1.5.dp))
                    .androidx.compose.foundation.background(androidx.compose.ui.graphics.Color(0xFFE50914))
            )
        }}
        
        if (onSeeAllClick != null) {{
            androidx.compose.foundation.layout.Row(
                verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
                modifier = androidx.compose.ui.Modifier.androidx.compose.foundation.clickable {{ onSeeAllClick() }}
            ) {{
                androidx.compose.material3.Text(
                    text = androidx.compose.ui.res.stringResource(com.example.R.string.see_all),
                    style = androidx.compose.material3.MaterialTheme.typography.labelLarge,
                    color = androidx.compose.ui.graphics.Color(0xFFE50914)
                )
                androidx.compose.foundation.layout.Spacer(modifier = androidx.compose.ui.Modifier.width(4.dp))
                androidx.compose.material3.Icon(
                    imageVector = androidx.compose.material.icons.Icons.Default.KeyboardArrowRight,
                    contentDescription = "See All",
                    tint = androidx.compose.ui.graphics.Color(0xFFE50914),
                    modifier = androidx.compose.ui.Modifier.size(16.dp)
                )
            }}
        }}
    }}"""
    
    text = text[:start_idx] + new_func + text[end_idx+1:]
    with open(filepath, 'w') as f:
        f.write(text)
    print(f"Rewrote {func_name} in {filepath}")

rewrite_file('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt', 'SectionTitle')
rewrite_file('app/src/main/java/com/example/ui/components/SharedUI.kt', 'SectionTitleShared')
