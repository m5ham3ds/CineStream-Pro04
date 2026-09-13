import re

filepath = 'app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Make sure the scroll indicator for "جاري تحميل الحلقات..." doesn't crash if sp isn't imported correctly.
# Already did this.
