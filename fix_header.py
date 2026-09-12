import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

pattern = r"androidx\.compose\.material3\.IconButton\(\s*onClick = \{ scope\.launch \{ drawerState\.open\(\) \} \}\s*\) \{\s*Icon\(\s*imageVector = Icons\.Default\.Menu,.*?\)\s*\}\s*\}\s*\}\s*\}"

import sys
# It's better to use sed or python with slicing by lines
