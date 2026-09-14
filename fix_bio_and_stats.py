import re

file_path = "app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

target = """                // Biography
                if (person.biography.isNotBlank()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.width(3.dp).height(16.dp).background(MaterialTheme.colorScheme.primary, RoundedCornerShape(4.dp)))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.biography), fontSize = 18.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            }
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(person.biography, color = Color.LightGray, fontSize = 14.sp, lineHeight = 20.sp)
                        }
                    }
                }"""

replacement = """                // Biography
                if (person.biography.isNotBlank()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.width(3.dp).height(16.dp).background(MaterialTheme.colorScheme.primary, RoundedCornerShape(4.dp)))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(stringResource(R.string.biography), fontSize = 18.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            }
                            Spacer(modifier = Modifier.height(12.dp))
                            
                            var isBioExpanded by remember { mutableStateOf(false) }
                            androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
                                Text(
                                    text = person.biography, 
                                    color = Color.LightGray, 
                                    fontSize = 14.sp, 
                                    lineHeight = 20.sp,
                                    maxLines = if (isBioExpanded) Int.MAX_VALUE else 4,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = if (isBioExpanded) stringResource(R.string.read_less) else stringResource(R.string.read_more),
                                color = MaterialTheme.colorScheme.primary,
                                fontSize = 14.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.clickable { isBioExpanded = !isBioExpanded }.padding(vertical = 4.dp)
                            )
                        }
                    }
                }"""

content = content.replace(target, replacement)

content = content.replace('label = "Movies"', 'label = stringResource(R.string.movies)')
content = content.replace('label = "TV Shows"', 'label = stringResource(R.string.series)')
content = content.replace('label = "Years Active"', 'label = stringResource(R.string.years_active)')

with open(file_path, "w") as f:
    f.write(content)
