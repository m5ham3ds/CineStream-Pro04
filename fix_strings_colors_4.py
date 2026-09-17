import re

def fix_file(filepath, replacements):
    with open(filepath, "r") as f:
        c = f.read()
    for old, new in replacements:
        c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

# PlayerScreen
fix_file("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", [
    ('contentDescription = "Unlock"', 'contentDescription = stringResource(R.string.unlock)'),
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Menu"', 'contentDescription = stringResource(R.string.menu)'),
    ('contentDescription = "Rewind"', 'contentDescription = stringResource(R.string.rewind)'),
    ('contentDescription = "Play/Pause"', 'contentDescription = stringResource(R.string.play_pause)'),
    ('contentDescription = "Forward"', 'contentDescription = stringResource(R.string.forward)')
])

# ServerSelectionDialog
fix_file("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", [
    ('Color(0xFF00C853)', 'MaterialTheme.colorScheme.tertiary'),
    ('Color(0xFFFF1111)', 'MaterialTheme.colorScheme.error'),
    ('Color(0xFF101014)', 'MaterialTheme.colorScheme.background'),
    ('Color(0xFF222222)', 'MaterialTheme.colorScheme.surfaceVariant'),
    ('Color(0xFF222225)', 'MaterialTheme.colorScheme.surface'),
    ('Color(0xFF333333)', 'MaterialTheme.colorScheme.outlineVariant'),
    ('Color.LightGray', 'MaterialTheme.colorScheme.onSurfaceVariant'),
    ('contentDescription = "إغلاق"', 'contentDescription = stringResource(R.string.close)'),
    ('Color(0xFF220000)', 'MaterialTheme.colorScheme.errorContainer'),
    ('Color(0x33FF1111)', 'MaterialTheme.colorScheme.error'),
    ('Color(0xFFFF4444)', 'MaterialTheme.colorScheme.error'),
    ('Text("لا يوجد مواقع أخرى"', 'Text(stringResource(R.string.no_other_sites)'),
    ('Text("عذراً، فشل البحث في جميع المواقع المتاحة."', 'Text(stringResource(R.string.no_other_sites_desc)'),
    ('Text("الإضافات"', 'Text(stringResource(R.string.extensions)'),
    ('Text("إغلاق"', 'Text(stringResource(R.string.close)'),
    ('Color(0xFF16161A)', 'MaterialTheme.colorScheme.surfaceVariant'),
    ('Color(0x15FFFFFF)', 'MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f)'),
    ('Color(0xFFE91E63)', 'MaterialTheme.colorScheme.primary'),
    ('Color(0xFF9C27B0)', 'MaterialTheme.colorScheme.secondary'),
    ('Color(0xFF607D8B)', 'MaterialTheme.colorScheme.onSurfaceVariant'),
    ('Text("إلغاء العملية"', 'Text(stringResource(R.string.cancel_op_title)'),
    ('Text("هل أنت متأكد أنك تود إلغاء العملية؟"', 'Text(stringResource(R.string.cancel_op_desc)'),
    ('Text("نعم"', 'Text(stringResource(R.string.yes_cancel)'),
    ('Text("لا"', 'Text(stringResource(R.string.no)')
])

