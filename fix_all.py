path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# Replace ANY onBackgroundColor with MaterialTheme.colorScheme.onBackground
content = content.replace('onBackgroundColor', 'MaterialTheme.colorScheme.onBackground')
content = content.replace('MaterialTheme.colorScheme.onBackground,', 'MaterialTheme.colorScheme.onBackground')
# Now, find Canvas(modifier =
# and insert `val onBackgroundColor = MaterialTheme.colorScheme.onBackground` right above it!
content = content.replace('val MaterialTheme.colorScheme.onBackground = MaterialTheme.colorScheme.onBackground', '')
content = content.replace('val MaterialTheme.colorScheme.onBackground = MaterialTheme.colorScheme.onBackground', '')

# Ensure we just have simple MaterialTheme.colorScheme.onBackground everywhere
content = content.replace('color = MaterialTheme.colorScheme.onBackground', 'color = MaterialTheme.colorScheme.onBackground')

# And specifically inside VerticalSlider, it needs to be fixed!
# Let's fix the specific lines inside VerticalSlider
target_slider = """        Canvas(modifier = Modifier
            .fillMaxHeight()
            .width(20.dp)
            .pointerInput(Unit) {
                detectDragGestures { change, _ ->
                    val y = change.position.y
                    val newValue = 1f - (y / size.height).coerceIn(0f, 1f)
                    if (newValue != value) {
                        onValueChange(newValue)
                    }
                }
            }
        ) {"""

replacement_slider = """        val canvasColor = MaterialTheme.colorScheme.onBackground
        Canvas(modifier = Modifier
            .fillMaxHeight()
            .width(20.dp)
            .pointerInput(Unit) {
                detectDragGestures { change, _ ->
                    val y = change.position.y
                    val newValue = 1f - (y / size.height).coerceIn(0f, 1f)
                    if (newValue != value) {
                        onValueChange(newValue)
                    }
                }
            }
        ) {"""
content = content.replace(target_slider, replacement_slider)

# Now inside that Canvas, change MaterialTheme.colorScheme.onBackground to canvasColor
# It's at lines 784, 792, 800
# 1. color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.3f),
# 2. color = MaterialTheme.colorScheme.onBackground,
# 3. color = MaterialTheme.colorScheme.onBackground,
target_canvas_body = """            val thumbY = height - (height * value)
            
            // Inactive Track (Full height)
            drawRoundRect(
                color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.3f),
                topLeft = Offset(centerX - trackWidth / 2f, 0f),
                size = Size(trackWidth, height),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Active Track (From bottom to thumb)
            drawRoundRect(
                color = MaterialTheme.colorScheme.onBackground,
                topLeft = Offset(centerX - trackWidth / 2f, thumbY),
                size = Size(trackWidth, height - thumbY),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Thumb
            drawCircle(
                color = MaterialTheme.colorScheme.onBackground,
                radius = thumbRadius,
                center = Offset(centerX, thumbY)
            )"""

replacement_canvas_body = """            val thumbY = height - (height * value)
            
            // Inactive Track (Full height)
            drawRoundRect(
                color = canvasColor.copy(alpha = 0.3f),
                topLeft = Offset(centerX - trackWidth / 2f, 0f),
                size = Size(trackWidth, height),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Active Track (From bottom to thumb)
            drawRoundRect(
                color = canvasColor,
                topLeft = Offset(centerX - trackWidth / 2f, thumbY),
                size = Size(trackWidth, height - thumbY),
                cornerRadius = CornerRadius(trackWidth / 2f)
            )
            
            // Thumb
            drawCircle(
                color = canvasColor,
                radius = thumbRadius,
                center = Offset(centerX, thumbY)
            )"""

content = content.replace(target_canvas_body, replacement_canvas_body)

with open(path, 'w') as f:
    f.write(content)
