import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        text = f.read()

    # Remove all fully qualified prefixes
    prefixes = [
        "androidx.compose.foundation.layout.",
        "androidx.compose.ui.Modifier.",
        "androidx.compose.ui.Alignment.",
        "androidx.compose.material3.",
        "androidx.compose.foundation.",
        "androidx.compose.ui.graphics.",
        "androidx.compose.ui.text.font.",
        "androidx.compose.ui.text.style.",
        "androidx.compose.ui.draw.",
        "androidx.compose.foundation.shape.",
        "androidx.compose.ui.layout.",
        "androidx.compose.ui.res.",
        "androidx.compose.material.icons."
    ]
    
    for p in prefixes:
        text = text.replace(p, "")
        
    text = text.replace("coil.compose.AsyncImage", "AsyncImage")
    
    # Add imports if missing
    imports = """import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.material3.*
import androidx.compose.foundation.*
import androidx.compose.ui.graphics.*
import androidx.compose.ui.text.font.*
import androidx.compose.ui.text.style.*
import androidx.compose.ui.draw.*
import androidx.compose.foundation.shape.*
import androidx.compose.ui.layout.*
import androidx.compose.ui.res.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import coil.compose.AsyncImage
"""
    # Just prepend imports to be safe, Kotlin allows duplicate imports usually, but let's check
    # Actually, let's just insert at the top after package
    lines = text.split('\n')
    out_lines = []
    for line in lines:
        out_lines.append(line)
        if line.startswith("package "):
            out_lines.append(imports)
            
    with open(filepath, 'w') as f:
        f.write('\n'.join(out_lines))
        
fix_file('app/src/main/java/com/example/ui/components/SharedUI.kt')
fix_file('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt')
