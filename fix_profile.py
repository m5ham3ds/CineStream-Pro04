import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    c = f.read()

# Colors
c = re.sub(r'val bgColor\s*=\s*Color\(0xFF09090C\)', 'val bgColor = MaterialTheme.colorScheme.background', c)
c = re.sub(r'val cardBg\s*=\s*Color\(0xFF16161A\)', 'val cardBg = MaterialTheme.colorScheme.surfaceVariant', c)
c = re.sub(r'val textGrey\s*=\s*Color\(0xFFAAAAAA\)', 'val textGrey = MaterialTheme.colorScheme.onSurfaceVariant', c)
c = c.replace('Color(0xFF1C1C1E)', 'MaterialTheme.colorScheme.surface')
c = c.replace('Color(0xFF2C2C2E)', 'MaterialTheme.colorScheme.secondaryContainer')
c = c.replace('Color(0xFF4A0E13)', 'MaterialTheme.colorScheme.primaryContainer')
c = c.replace('Color(0xFF2A080C)', 'MaterialTheme.colorScheme.surface')
c = c.replace('Color(0xFF3A1015)', 'MaterialTheme.colorScheme.outline')
c = c.replace('Color(0xFF2A0C10)', 'MaterialTheme.colorScheme.surface')
c = c.replace('Color(0xFF1E1E22)', 'MaterialTheme.colorScheme.surface')
c = c.replace('Color(0xFF222225)', 'MaterialTheme.colorScheme.outlineVariant')

# Strings
c = c.replace('Text("Cancel"', 'Text(stringResource(R.string.cancel)')
c = c.replace('contentDescription = "Edit Profile"', 'contentDescription = stringResource(R.string.edit_profile)')
c = c.replace('Text("Premium Plan >"', 'Text(stringResource(R.string.premium_plan) + " >"')
c = c.replace('Text("GOOD\\nSTORIES\\nNEVER\\nEND"', 'Text(stringResource(R.string.good_stories_never_end)')
c = c.replace('Text("Enjoy ad-free streaming\\nand exclusive content."', 'Text(stringResource(R.string.enjoy_ad_free)')
c = c.replace('Text("Manage Plan →"', 'Text(stringResource(R.string.manage_plan) + " →"')
c = c.replace('Text("Manage your account settings"', 'Text(stringResource(R.string.settings_desc)') # or create new string. I see account_info_desc or similar. Wait, manage_your_account_settings was not in the grep?

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(c)

