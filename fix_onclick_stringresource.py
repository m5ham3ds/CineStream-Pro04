import re
import glob

for filepath in glob.glob('app/src/main/java/com/example/**/*.kt', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()

    # The issue is typically in Toast.makeText(context, stringResource(R.string.xxx), ...) 
    # or inside onClick = { val x = stringResource(...) }
    
    # Actually, a simpler way is to just do `context.getString(R.string.xxx)` where we know it's a context or inside Toast
    content = content.replace('Toast.makeText(context, stringResource(', 'Toast.makeText(context, context.getString(')
    content = content.replace('Toast.makeText(LocalContext.current, stringResource(', 'Toast.makeText(LocalContext.current, context.getString(')
    # The regex approach:
    # Let's just fix the specific files and lines we saw in the error log.
    
    with open(filepath, 'w') as f:
        f.write(content)

