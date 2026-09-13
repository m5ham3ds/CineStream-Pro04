import os

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack', 'androidx.compose.material.icons.automirrored.filled.ArrowBack')
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight', 'androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight')
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowLeft', 'androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft')
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.Send', 'androidx.compose.material.icons.automirrored.filled.Send')
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.HelpOutline', 'androidx.compose.material.icons.automirrored.filled.HelpOutline')
            content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Outlined.ArrowBack', 'androidx.compose.material.icons.automirrored.outlined.ArrowBack')
            
            content = content.replace('Icons.AutoMirrored.Filled.ArrowBack', 'androidx.compose.material.icons.automirrored.filled.ArrowBack')
            content = content.replace('Icons.AutoMirrored.Filled.KeyboardArrowRight', 'androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight')
            content = content.replace('Icons.AutoMirrored.Filled.KeyboardArrowLeft', 'androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft')
            content = content.replace('Icons.AutoMirrored.Filled.Send', 'androidx.compose.material.icons.automirrored.filled.Send')
            content = content.replace('Icons.AutoMirrored.Filled.HelpOutline', 'androidx.compose.material.icons.automirrored.filled.HelpOutline')
            content = content.replace('Icons.AutoMirrored.Outlined.ArrowBack', 'androidx.compose.material.icons.automirrored.outlined.ArrowBack')

            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
