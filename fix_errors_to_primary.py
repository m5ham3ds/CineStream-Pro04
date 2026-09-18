import re
import os

file_path = "app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt"
with open(file_path, "r") as f:
    content = f.read()

# 1. Fix activeColor logic
# Old: val activeColor = if (isVerified || isNormal) SuccessGreen else SuccessGreen
# New: val activeColor = if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary
content = content.replace(
    "val activeColor = if (isVerified || isNormal) SuccessGreen else SuccessGreen",
    "val activeColor = if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary"
)

# 2. Fix iconTint logic
# Old: val iconTint = if (isFailed) SuccessGreen else if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary
# New: val iconTint = if (isFailed) MaterialTheme.colorScheme.primary else if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary
content = content.replace(
    "val iconTint = if (isFailed) SuccessGreen else if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary",
    "val iconTint = if (isFailed) MaterialTheme.colorScheme.primary else if (isVerified || isNormal) SuccessGreen else MaterialTheme.colorScheme.primary"
)

# 3. Fix the error message box
error_box_old = """                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(SuccessGreen.copy(alpha = 0.15f))
                                    .border(1.dp, SuccessGreen, RoundedCornerShape(12.dp))
                                    .padding(16.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Error, contentDescription = null, tint = SuccessGreen, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text(
                                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                                        color = SuccessGreen,"""

error_box_new = """                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f))
                                    .border(1.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(12.dp))
                                    .padding(16.dp)
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Error, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(24.dp))
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text(
                                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                                        color = MaterialTheme.colorScheme.primary,"""

content = content.replace(error_box_old, error_box_new)

# 4. Fix Retry Button
# Old: colors = ButtonDefaults.buttonColors(containerColor = SuccessGreen),
# New: colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
content = content.replace(
    "colors = ButtonDefaults.buttonColors(containerColor = SuccessGreen),",
    "colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),"
)

# 5. Fix Cancel confirm dialog
# Old: Text(stringResource(R.string.yes_cancel), color = SuccessGreen)
# New: Text(stringResource(R.string.yes_cancel), color = MaterialTheme.colorScheme.primary)
content = content.replace(
    "Text(stringResource(R.string.yes_cancel), color = SuccessGreen)",
    "Text(stringResource(R.string.yes_cancel), color = MaterialTheme.colorScheme.primary)"
)

with open(file_path, "w") as f:
    f.write(content)

# Fix CrashActivity and DetailsScreens
files_to_fix = [
    "app/src/main/java/com/example/ui/screens/crash/CrashActivity.kt",
    "app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt"
]

for fp in files_to_fix:
    with open(fp, "r") as f:
        c = f.read()
    c = c.replace("color = SuccessGreen", "color = MaterialTheme.colorScheme.primary")
    with open(fp, "w") as f:
        f.write(c)

