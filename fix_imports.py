import os

def fix_imports(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    out_lines = []
    for line in lines:
        if line.startswith("import "):
            continue
        out_lines.append(line)
        
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
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import com.example.R
import com.example.data.model.*
import com.example.data.repository.*
import com.example.domain.models.*
import com.example.ui.ViewModelFactory
import kotlinx.coroutines.launch
import androidx.compose.foundation.pager.*
import androidx.compose.foundation.lazy.*
import androidx.lifecycle.viewmodel.compose.viewModel
import android.widget.Toast
import androidx.compose.material3.pulltorefresh.*
import com.example.ui.screens.home.HomeViewModel
"""
    final_lines = []
    for line in out_lines:
        final_lines.append(line)
        if line.startswith("package "):
            final_lines.append(imports)
            
    with open(filepath, 'w') as f:
        f.write("".join(final_lines))

fix_imports('app/src/main/java/com/example/ui/components/SharedUI.kt')
fix_imports('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt')
