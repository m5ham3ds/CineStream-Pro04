import re

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "r") as f:
    c = f.read()

# Add ColorPainter import
if "import androidx.compose.ui.graphics.painter.ColorPainter" not in c:
    c = c.replace("import coil.compose.AsyncImage", "import coil.compose.AsyncImage\nimport androidx.compose.ui.graphics.painter.ColorPainter\nimport coil.request.ImageRequest\nimport coil.size.Scale")

# Replace AsyncImage
old_async = """        AsyncImage(
            model = posterUrl,
            contentDescription = title,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )"""

new_async = """        val placeholderColor = MaterialTheme.colorScheme.surfaceVariant
        AsyncImage(
            model = ImageRequest.Builder(LocalContext.current)
                .data(posterUrl)
                .crossfade(true)
                .scale(Scale.FILL)
                .build(),
            placeholder = ColorPainter(placeholderColor),
            error = ColorPainter(placeholderColor),
            contentDescription = title,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )"""

c = c.replace(old_async, new_async)

with open("app/src/main/java/com/example/ui/components/MediaCard.kt", "w") as f:
    f.write(c)
