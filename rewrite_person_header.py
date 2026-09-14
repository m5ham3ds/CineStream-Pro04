import re

file_path = "app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

start_marker = "// Info Section"
end_marker = "// Biography"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_info_section = """// Info Section
                    Column(
                        modifier = Modifier.weight(0.58f)
                    ) {
                        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
                            Column(horizontalAlignment = Alignment.Start) {
                                val names = person.name.split(" ", limit = 2)
                                val firstName = names.getOrNull(0) ?: ""
                                val lastName = names.getOrNull(1) ?: ""
                                
                                Text(firstName, fontSize = 28.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground, lineHeight = 32.sp)
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(lastName, fontSize = 28.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, lineHeight = 32.sp)
                                    Spacer(modifier = Modifier.width(6.dp))
                                    Icon(Icons.Default.CheckCircle, contentDescription = "Verified", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
                                }
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(person.knownFor ?: "Actor", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        // Info Grid - Changed to vertical list for better text alignment
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            // Born
                            Row(verticalAlignment = Alignment.Top) {
                                Icon(Icons.Default.CalendarToday, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp).padding(top = 2.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Column {
                                    Text(stringResource(R.string.born), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
                                        Text(person.birthday ?: "-", fontSize = 13.sp, color = MaterialTheme.colorScheme.onBackground, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                    }
                                }
                            }
                            // Birthplace
                            Row(verticalAlignment = Alignment.Top) {
                                Icon(Icons.Default.LocationOn, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp).padding(top = 2.dp))
                                Spacer(modifier = Modifier.width(8.dp))
                                Column {
                                    Text(stringResource(R.string.birthplace), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
                                        Text(person.placeOfBirth ?: "-", fontSize = 13.sp, color = MaterialTheme.colorScheme.onBackground, maxLines = 2, overflow = TextOverflow.Ellipsis)
                                    }
                                }
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Stats Row
                val firstCreditYear = (person.movies.map { it.year } + person.series.map { it.year }).filter { it > 0 }.minOrNull()
                val currentYear = Calendar.getInstance().get(Calendar.YEAR)
                val yearsActive = if (firstCreditYear != null && firstCreditYear > 0) {
                    currentYear - firstCreditYear
                } else {
                    0
                }
                val yearsActiveStr = if (yearsActive > 0) "${yearsActive}+" else "-"
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    StatBox(icon = Icons.Default.Movie, value = if (person.movies.isNotEmpty()) "${person.movies.size}+" else "-", label = "Movies", modifier = Modifier.weight(1f))
                    Spacer(modifier = Modifier.width(8.dp))
                    StatBox(icon = Icons.Default.Tv, value = if (person.series.isNotEmpty()) "${person.series.size}+" else "-", label = "TV Shows", modifier = Modifier.weight(1f))
                    Spacer(modifier = Modifier.width(8.dp))
                    StatBox(icon = Icons.Outlined.Star, value = yearsActiveStr, label = "Years Active", modifier = Modifier.weight(1f))
                }
                
                """
    
    content = content[:start_idx] + new_info_section + content[end_idx:]
    with open(file_path, "w") as f:
        f.write(content)
else:
    print("Markers not found")
