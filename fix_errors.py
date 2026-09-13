# Fix 1: ExtensionsScreen anime_tab unresolved reference.
ext_path = "app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt"
with open(ext_path, 'r') as f:
    ext_content = f.read()

ext_content = ext_content.replace('stringResource(R.string.anime_tab)', 'stringResource(R.string.anime)')

with open(ext_path, 'w') as f:
    f.write(ext_content)

# Fix 2: PublicProfileScreen selectedStat delegation
profile_path = "app/src/main/java/com/example/ui/screens/profile/PublicProfileScreen.kt"
with open(profile_path, 'r') as f:
    prof_content = f.read()

prof_content = prof_content.replace('Text(stringResource(R.string.stat_activity, selectedStat)', 'Text(stringResource(R.string.stat_activity, selectedStat.toString())')

with open(profile_path, 'w') as f:
    f.write(prof_content)

# Fix 3: CineStreamHeader @Composable calls inside draw scope
# When we replaced colors with MaterialTheme.colorScheme we put it inside DrawScope which is not a Composable context!
# We need to extract the color reading outside.
header_path = "app/src/main/java/com/example/ui/components/CineStreamHeader.kt"
with open(header_path, 'r') as f:
    h_content = f.read()

# It's better to just revert the CineStreamHeader colors to hardcoded ones, or declare them at the top of the Composable.
# Let's revert back to hardcoded since this is a complex UI component and hardcoded colors were fine for the gradient canvas.
# Or wait, you said the header had fixed colors you wanted changed. We can declare them at the top of the Composable function.
