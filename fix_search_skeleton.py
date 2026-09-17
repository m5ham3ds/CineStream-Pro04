import re

with open("app/src/main/java/com/example/ui/components/SkeletonScreens.kt", "r") as f:
    c = f.read()

target = """@Composable
fun SearchScreenSkeleton() {
    Column(modifier = Modifier.fillMaxSize()) {
        // Search Bar
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .height(56.dp)
                .clip(RoundedCornerShape(50))
                .shimmerEffect()
        )
        
        // Filter Row
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            userScrollEnabled = false
        ) {
            items(5) {
                Box(
                    modifier = Modifier
                        .width(80.dp)
                        .height(32.dp)
                        .clip(RoundedCornerShape(16.dp))
                        .shimmerEffect()
                )
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Results Grid
        GridScreenSkeleton()
    }
}"""

replacement = """@Composable
fun SearchScreenSkeleton() {
    Column(modifier = Modifier.fillMaxWidth()) {
        Spacer(modifier = Modifier.height(16.dp))
        GridScreenSkeleton()
    }
}"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/SkeletonScreens.kt", "w") as f:
    f.write(c)
