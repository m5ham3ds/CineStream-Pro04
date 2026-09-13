import re

file_path = 'app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace('val animeStr = animeStr', 'val animeStr = stringResource(R.string.anime)')

# Remove lines 96 to 109 which are garbage
garbage = '''
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab,
                        color = MaterialTheme.colorScheme.onBackground,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        fontSize = 14.sp
                    )
                }
            }
        }
'''
if garbage in content:
    content = content.replace(garbage, '')

with open(file_path, 'w') as f:
    f.write(content)

