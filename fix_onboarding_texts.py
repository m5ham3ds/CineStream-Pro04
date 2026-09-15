with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Download & Watch Offline
content = content.replace(
    'append(stringResource(R.string.download_watch_offline).substringBefore("Offline"))',
    'append(stringResource(R.string.download_and_watch))'
)
content = content.replace(
    'append("Offline")',
    'append(stringResource(R.string.offline_highlight))'
)

# Fix Personalized for You
content = content.replace(
    'append(stringResource(R.string.personalized_for_you).substringBefore("for You"))',
    'append(stringResource(R.string.personalized_prefix))'
)
content = content.replace(
    'append("for You")',
    'append(stringResource(R.string.for_you_highlight))'
)

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
