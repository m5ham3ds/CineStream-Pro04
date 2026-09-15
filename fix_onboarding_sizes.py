import re
with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "r") as f:
    content = f.read()

# Make texts smaller
content = content.replace("fontSize = 36.sp", "fontSize = 28.sp")
content = content.replace("fontSize = 22.sp", "fontSize = 20.sp")

# Adjust blur
content = content.replace("blur(radius = 16.dp)", "blur(radius = 24.dp)")
# Also change alpha layer to 0.7f from 0.5f
content = content.replace("Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.5f)))", "Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.7f)))")

# Remove some spacers if they are too big
content = content.replace("Spacer(modifier = Modifier.height(48.dp))", "Spacer(modifier = Modifier.height(24.dp))")
content = content.replace("padding(top = 340.dp, bottom = 180.dp)", "padding(top = 280.dp, bottom = 160.dp)")

# Fix slogan text string
with open("app/src/main/res/values/strings.xml", "r") as f:
    strings = f.read()

strings = re.sub(r'<string name="slogan_new">.*?</string>', '<string name="slogan_new">Movies. Series. Anime Endless entertainment.</string>', strings, flags=re.DOTALL)
with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(strings)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    strings_ar = f.read()

strings_ar = re.sub(r'<string name="slogan_new">.*?</string>', '<string name="slogan_new">أفلام. مسلسلات. أنمي ترفيه لا ينتهي.</string>', strings_ar, flags=re.DOTALL)
with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(strings_ar)

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "w") as f:
    f.write(content)
