import re
import glob

for filepath in glob.glob('app/src/main/java/com/example/**/*.kt', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()

    # In ProfileScreen
    if 'context.getString(R.string.log_out)' in content:
        if 'val context = LocalContext.current' not in content:
             content = content.replace('@Composable', '@Composable\nimport androidx.compose.ui.platform.LocalContext', 1)
             # Wait, import should be at the top!
             content = content.replace('import androidx.compose.runtime.Composable', 'import androidx.compose.runtime.Composable\nimport androidx.compose.ui.platform.LocalContext')
             
    with open(filepath, 'w') as f:
        f.write(content)
