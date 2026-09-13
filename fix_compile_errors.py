import re

# 1. DetailsScreens.kt - add sp import
filepath = 'app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()
if 'import androidx.compose.ui.unit.sp' not in content:
    content = content.replace('import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.unit.sp')
with open(filepath, 'w') as f:
    f.write(content)

# 2. SeriesDetailsViewModel.kt - fix getCachedState scoping
filepath = 'app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Since getCachedState is inside Cache companion object, it should be called on the companion object if it was named. 
# Wait, companion object methods are available directly in the class.
# Let's check where the companion object was added. 
if 'class SeriesDetailsViewModel' in content:
    pass
# It was probably added outside the class!
# Let's see: `content = content.replace('class SeriesDetailsViewModel(', cache_code + '\nclass SeriesDetailsViewModel(')`
# This puts it BEFORE the class, making it a companion object of WHAT? Nothing, it's invalid Kotlin! A top-level companion object is invalid. Or maybe it created a `companion object` block at the top level which Kotlin might parse as an object? No, it's invalid.
content = content.replace('''    companion object {
        private val cache = mutableMapOf<String, SeriesDetailsUiState>()
        fun getCachedState(seriesId: String) = cache[seriesId]
        fun saveState(seriesId: String, state: SeriesDetailsUiState) {
            cache[seriesId] = state
        }
    }''', '')

new_class_decl = '''class SeriesDetailsViewModel(
    private val repository: MediaRepository
) : ViewModel() {
    companion object {
        private val cache = mutableMapOf<String, SeriesDetailsUiState>()
        fun getCachedState(seriesId: String): SeriesDetailsUiState? = cache[seriesId]
        fun saveState(seriesId: String, state: SeriesDetailsUiState) {
            cache[seriesId] = state
        }
    }'''
content = re.sub(r'class SeriesDetailsViewModel\s*\(\s*private val repository: MediaRepository\s*\)\s*:\s*ViewModel\(\)\s*\{', new_class_decl, content, flags=re.DOTALL)
with open(filepath, 'w') as f:
    f.write(content)

# 3. HomeScreen.kt
filepath = 'app/src/main/java/com/example/ui/screens/home/HomeScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('items(categories, key = { category })', 'items(categories, key = { it })')
content = content.replace('items(historyItems, key = { item.id })', 'items(historyItems, key = { it.id })')

with open(filepath, 'w') as f:
    f.write(content)
    
# 4. WatchingScreen.kt
filepath = 'app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('items(items, key = { item.id })', 'items(items, key = { it.id })')
with open(filepath, 'w') as f:
    f.write(content)

# 5. Fix items in share and social etc, which were modified by the wild regex
# Wait, the wild regex didn't touch them if they weren't in `home` or `details` directory!
# My fix_keys script only processed: directories = ['app/src/main/java/com/example/ui/screens/home', 'app/src/main/java/com/example/ui/screens/details']

