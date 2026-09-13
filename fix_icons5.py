import os

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            
            content = content.replace('import Icons.AutoMirrored.Filled.ArrowBack', 'import androidx.compose.material.icons.automirrored.filled.ArrowBack')
            content = content.replace('import Icons.AutoMirrored.Filled.KeyboardArrowRight', 'import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight')
            content = content.replace('import Icons.AutoMirrored.Filled.KeyboardArrowLeft', 'import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft')
            content = content.replace('import Icons.AutoMirrored.Filled.Send', 'import androidx.compose.material.icons.automirrored.filled.Send')
            content = content.replace('import Icons.AutoMirrored.Filled.HelpOutline', 'import androidx.compose.material.icons.automirrored.filled.HelpOutline')
            content = content.replace('import Icons.AutoMirrored.Outlined.ArrowBack', 'import androidx.compose.material.icons.automirrored.outlined.ArrowBack')
            
            # and let's remove duplicate imports just in case
            lines = []
            for line in content.split('\n'):
                if line.startswith('import ') and line in lines:
                    continue
                lines.append(line)

            content = '\n'.join(lines)

            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
