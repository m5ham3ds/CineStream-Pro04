import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

pattern = r"if \(!isSearchExpanded\) \{(.*?)\}"

new_topbar = """if (!isSearchExpanded) {
                                Spacer(modifier = Modifier.weight(1f))
                                val titleRes = when(currentRoute) {
                                    Screen.Home.route -> R.string.app_name
                                    Screen.Movies.route -> R.string.movies
                                    Screen.Series.route -> R.string.series
                                    Screen.Anime.route -> R.string.anime
                                    Screen.Search.route -> R.string.search
                                    Screen.Profile.route -> R.string.profile
                                    Screen.Settings.route -> R.string.settings
                                    Screen.Downloads.route -> R.string.downloads
                                    Screen.About.route -> R.string.about
                                    Screen.Extensions.route -> R.string.extensions
                                    Screen.Share.route -> R.string.share
                                    Screen.Social.route -> R.string.social
                                    else -> R.string.app_name
                                }
                                Text(
                                    text = stringResource(id = titleRes),
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onBackground
                                )
                                Spacer(modifier = Modifier.weight(1f))
                            }"""

text = re.sub(pattern, new_topbar, text, count=1, flags=re.DOTALL)
with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(text)
print("Fixed TopBar!")
