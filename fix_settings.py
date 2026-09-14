import re

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    text = f.read()

# Let's replace the confirm button logic for language change
restart_logic = """
                    val lang = pendingLanguage
                    if (lang != null) {
                        coroutineScope.launch { 
                            userPrefs.saveAppLanguage(lang)
                            kotlinx.coroutines.delay(100) 
                            val intent = context.packageManager.getLaunchIntentForPackage(context.packageName)
                            intent?.addFlags(android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP or android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK)
                            if (intent != null) {
                                context.startActivity(intent)
                                (context as? android.app.Activity)?.finishAffinity()
                                Runtime.getRuntime().exit(0)
                            }
                        }
                    }
                    pendingLanguage = null
"""

text = re.sub(
    r'val lang = pendingLanguage\s*if \(lang != null\) \{\s*coroutineScope\.launch \{ userPrefs\.saveAppLanguage\(lang\) \}\s*\}\s*pendingLanguage = null',
    restart_logic.strip(), text, count=1, flags=re.MULTILINE
)

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(text)

