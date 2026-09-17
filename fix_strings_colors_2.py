import re

def fix_file(filepath, replacements):
    with open(filepath, "r") as f:
        c = f.read()
    for old, new in replacements:
        c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

# SettingsScreen
fix_file("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", [
    ('contentDescription = "System"', 'contentDescription = stringResource(R.string.system)'),
    ('contentDescription = "Light"', 'contentDescription = stringResource(R.string.light)'),
    ('contentDescription = "Dark"', 'contentDescription = stringResource(R.string.dark)'),
    ('val darkBg = Color(0xFF0F0F11)', 'val darkBg = MaterialTheme.colorScheme.background'),
    ('val cardBg = Color(0xFF19191B)', 'val cardBg = MaterialTheme.colorScheme.surfaceVariant'),
    ('Color(0xFF1C1C1E)', 'MaterialTheme.colorScheme.surface'),
    ('Color(0xFF2C2C2E)', 'MaterialTheme.colorScheme.outlineVariant'),
    ('Text("Download Network"', 'Text(stringResource(R.string.download_network)'),
    ('Color(0xFF2B1114)', 'MaterialTheme.colorScheme.primaryContainer'),
    ('Color(0xFF141416)', 'MaterialTheme.colorScheme.surface')
])

# DownloadsScreen
fix_file("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", [
    ('contentDescription = "Downloads"', 'contentDescription = stringResource(R.string.downloads)'),
    ('contentDescription = "Pause/Resume"', 'contentDescription = stringResource(R.string.pause_resume)'),
    ('contentDescription = "Delete"', 'contentDescription = stringResource(R.string.delete)'),
])

# AboutScreen
fix_file("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", [
    ('contentDescription = "Logo"', 'contentDescription = stringResource(R.string.logo)')
])

# NotificationsScreen
fix_file("app/src/main/java/com/example/ui/screens/notifications/NotificationsScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Mark all as read"', 'contentDescription = stringResource(R.string.mark_all_read)'),
    ('contentDescription = "Delete"', 'contentDescription = stringResource(R.string.delete)')
])

# SearchScreen
fix_file("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", [
    ('contentDescription = "Search"', 'contentDescription = stringResource(R.string.search)'),
    ('contentDescription = "Filter"', 'contentDescription = stringResource(R.string.filter)'),
    ('contentDescription = "Remove"', 'contentDescription = stringResource(R.string.remove)')
])

# ShareScreen
fix_file("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", [
    ('contentDescription = "Send"', 'contentDescription = stringResource(R.string.send)'),
    ('contentDescription = "Receive"', 'contentDescription = stringResource(R.string.receive)'),
    ('contentDescription = "Folder"', 'contentDescription = stringResource(R.string.folder)'),
    ('contentDescription = "Open"', 'contentDescription = stringResource(R.string.open)'),
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "QR Code"', 'contentDescription = stringResource(R.string.qr_code)'),
    ('contentDescription = "Signal"', 'contentDescription = stringResource(R.string.signal)'),
    ('Color(0xFF10b981)', 'MaterialTheme.colorScheme.tertiary')
])

# SocialScreen
fix_file("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", [
    ('contentDescription = "Search"', 'contentDescription = stringResource(R.string.search)'),
    ('contentDescription = "Add Story"', 'contentDescription = stringResource(R.string.add_story)')
])

# OnboardingScreen
fix_file("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", [
    ('Color(0xFF0D0D0D)', 'MaterialTheme.colorScheme.background')
])

# SplashScreen
fix_file("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", [
    ('Color(0xFF09090C)', 'MaterialTheme.colorScheme.background')
])

# ExtensionsScreen
fix_file("app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt", [
    ('contentDescription = "Filter"', 'contentDescription = stringResource(R.string.filter)'),
    ('contentDescription = "Search"', 'contentDescription = stringResource(R.string.search)'),
    ('contentDescription = "More"', 'contentDescription = stringResource(R.string.more)'),
    ('contentDescription = "Close"', 'contentDescription = stringResource(R.string.close)')
])

