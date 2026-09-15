with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'Box(modifier = Modifier.width(20.dp).height(1.dp).background(MaterialTheme.colorScheme.primary).padding(top=8.dp))',
    'Spacer(modifier = Modifier.height(8.dp))\n                Box(modifier = Modifier.width(20.dp).height(1.dp).background(MaterialTheme.colorScheme.primary))'
)

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "w") as f:
    f.write(content)
