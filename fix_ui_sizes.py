import re

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "r") as f:
    content = f.read()

# Add blur import if not there
if "import androidx.compose.ui.draw.blur" not in content:
    content = content.replace("import androidx.compose.ui.draw.clip", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.blur")

# Blur background
content = content.replace(
    '''Image(
                    painter = painterResource(id = bgRes),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )''',
    '''Image(
                    painter = painterResource(id = bgRes),
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize().blur(radius = 16.dp)
                )
                // Additional tint layer
                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.5f)))'''
)

# Text sizes in fixed top content
content = content.replace('fontSize = 18.sp,', 'fontSize = 16.sp,')
content = content.replace('fontSize = 42.sp,', 'fontSize = 36.sp,')
content = content.replace('fontSize = 15.sp,', 'fontSize = 13.sp,')
content = content.replace('lineHeight = 22.sp,', 'lineHeight = 20.sp,')

# Button sizes
content = content.replace('.height(56.dp),', '.height(48.dp),')
# Need to ensure we don't catch the wrong 18.sp, we already replaced 18.sp above (Welcome to), wait, button text 18.sp -> 16.sp:
content = content.replace('fontSize = 18.sp,\n                            fontWeight = FontWeight.Bold,\n                            color = Color.White', 'fontSize = 16.sp,\n                            fontWeight = FontWeight.Bold,\n                            color = Color.White')

# PageOne Content Side texts
content = content.replace('fontSize = 10.sp,', 'fontSize = 9.sp,')
content = content.replace('lineHeight = 16.sp,', 'lineHeight = 14.sp,')
content = content.replace('padding(vertical = 20.dp)', 'padding(vertical = 16.dp)')

# FeatureItem text size
content = content.replace('fontSize = 12.sp, textAlign = TextAlign.Center, lineHeight = 16.sp', 'fontSize = 11.sp, textAlign = TextAlign.Center, lineHeight = 14.sp')

# PageTwo Content Icon
content = content.replace('size(64.dp)', 'size(56.dp)')
content = content.replace('size(32.dp)', 'size(28.dp)')
content = content.replace('fontSize = 24.sp,', 'fontSize = 22.sp,')

# PageThree Content
content = content.replace('.height(110.dp)', '.height(90.dp)')
content = content.replace('size(28.dp)', 'size(24.dp)')

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "w") as f:
    f.write(content)
