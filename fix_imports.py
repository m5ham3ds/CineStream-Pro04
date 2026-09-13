import glob

for filepath in glob.glob('app/src/main/java/com/example/**/*.kt', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    
    if 'stringResource(R.string' in content:
        if 'import androidx.compose.ui.res.stringResource' not in content:
            # Find the package declaration line and insert after it
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith('package '):
                    lines.insert(i + 1, '\nimport androidx.compose.ui.res.stringResource')
                    lines.insert(i + 2, 'import com.example.R')
                    break
            content = '\n'.join(lines)
        elif 'import com.example.R' not in content:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith('package '):
                    lines.insert(i + 1, '\nimport com.example.R')
                    break
            content = '\n'.join(lines)

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)

print("Import fix done.")
