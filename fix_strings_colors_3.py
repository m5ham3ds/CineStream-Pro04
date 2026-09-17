import re

def fix_file(filepath, replacements):
    with open(filepath, "r") as f:
        c = f.read()
    for old, new in replacements:
        c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

# PlayerScreen and Details
fix_file("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", [
    ('contentDescription = "Rating"', 'contentDescription = stringResource(R.string.rating_r)'),
    ('Color(0xFFFFC107)', 'MaterialTheme.colorScheme.primary'),
    ('contentDescription = "Play"', 'contentDescription = stringResource(R.string.play_now)'),
    ('contentDescription = "Downloaded"', 'contentDescription = stringResource(R.string.completed)'),
    ('contentDescription = "Download"', 'contentDescription = stringResource(R.string.downloads)'),
    ('contentDescription = "Favorite"', 'contentDescription = stringResource(R.string.add_to_library_favorites)'),
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Downloading"', 'contentDescription = stringResource(R.string.downloading)'),
    ('Text("18+"', 'Text("18+"'), # keep as is
    ('Text("نعم"', 'Text(stringResource(R.string.yes_cancel)'),
    ('Text("لا"', 'Text(stringResource(R.string.no)')
])

# PersonDetailsScreen
fix_file("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Share"', 'contentDescription = stringResource(R.string.share)'), # Need string
    ('contentDescription = "Gallery"', 'contentDescription = stringResource(R.string.gallery)'), # Need string
    ('contentDescription = "Verified"', 'contentDescription = stringResource(R.string.verified)') # Need string
])

# EditProfileScreen
fix_file("app/src/main/java/com/example/ui/screens/profile/EditProfileScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Profile Picture"', 'contentDescription = stringResource(R.string.profile_picture)'), # Need string
    ('contentDescription = "Edit Photo"', 'contentDescription = stringResource(R.string.edit_photo)') # Need string
])

# SubscriptionScreen
fix_file("app/src/main/java/com/example/ui/screens/profile/SubscriptionScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('Color(0xFF2C1E20)', 'MaterialTheme.colorScheme.surfaceVariant')
])

# PublicProfileScreen
fix_file("app/src/main/java/com/example/ui/screens/profile/PublicProfileScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Avatar"', 'contentDescription = stringResource(R.string.avatar)') # Need string
])

# SecurityScreen
fix_file("app/src/main/java/com/example/ui/screens/profile/SecurityScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)')
])

# HelpSupportScreen
fix_file("app/src/main/java/com/example/ui/screens/profile/HelpSupportScreen.kt", [
    ('contentDescription = "Back"', 'contentDescription = stringResource(R.string.back)'),
    ('contentDescription = "Options"', 'contentDescription = stringResource(R.string.options)'), # Need string
    ('contentDescription = "Attach"', 'contentDescription = stringResource(R.string.attach)'), # Need string
    ('contentDescription = "Emoji"', 'contentDescription = stringResource(R.string.emoji)'), # Need string
    ('contentDescription = "Send"', 'contentDescription = stringResource(R.string.send)'),
    ('contentDescription = "Sent"', 'contentDescription = stringResource(R.string.sent)'), # Need string
    ('Color(0xFF1E3A2A)', 'MaterialTheme.colorScheme.primaryContainer'),
    ('Text("We\'re here to help you"', 'Text(stringResource(R.string.help_support_desc)') # Need string
])

