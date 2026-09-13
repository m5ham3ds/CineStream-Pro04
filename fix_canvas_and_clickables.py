def fix_player_screen():
    path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
    with open(path, 'r') as f:
        content = f.read()
    
    # In VerticalSlider, hoist the color:
    # Look for: Canvas(modifier = ... {
    # It's inside a function VerticalSlider(value: Float, onValueChange: (Float) -> Unit, modifier: Modifier = Modifier)
    
    if 'val onBackgroundColor = MaterialTheme.colorScheme.onBackground' not in content:
        content = content.replace('Canvas(modifier =', 'val onBackgroundColor = MaterialTheme.colorScheme.onBackground\n        Canvas(modifier =')
        content = content.replace('color = MaterialTheme.colorScheme.onBackground', 'color = onBackgroundColor')
        
    with open(path, 'w') as f:
        f.write(content)

def fix_profile_screen():
    path = 'app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt'
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace('stringResource(R.string.username_small)', 'context.getString(R.string.username_small)')
    with open(path, 'w') as f:
        f.write(content)
        
def fix_chat_screen():
    path = 'app/src/main/java/com/example/ui/screens/social/ChatScreen.kt'
    with open(path, 'r') as f:
        content = f.read()
    content = content.replace('stringResource(R.string.message)', 'context.getString(R.string.message)')
    with open(path, 'w') as f:
        f.write(content)

fix_player_screen()
fix_profile_screen()
fix_chat_screen()
