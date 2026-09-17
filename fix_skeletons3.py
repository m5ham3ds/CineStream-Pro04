import re

with open("app/src/main/java/com/example/ui/components/SkeletonScreens.kt", "r") as f:
    c = f.read()

skeletons = """

@Composable
fun NotificationsScreenSkeleton() {
    Column(modifier = Modifier.fillMaxSize()) {
        // TopBar fake
        Row(modifier = Modifier.fillMaxWidth().height(64.dp).padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(24.dp).clip(CircleShape).shimmerEffect())
            Spacer(modifier = Modifier.width(16.dp))
            Box(modifier = Modifier.width(120.dp).height(24.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Notifications list
        repeat(6) {
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(48.dp).clip(CircleShape).shimmerEffect())
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Box(modifier = Modifier.width(150.dp).height(18.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(modifier = Modifier.fillMaxWidth(0.9f).height(14.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                    Spacer(modifier = Modifier.height(8.dp))
                    Box(modifier = Modifier.width(80.dp).height(12.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                }
            }
        }
    }
}

@Composable
fun HelpSupportScreenSkeleton() {
    Column(modifier = Modifier.fillMaxSize()) {
        // TopBar fake
        Row(modifier = Modifier.fillMaxWidth().height(64.dp).padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(24.dp).clip(CircleShape).shimmerEffect())
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Box(modifier = Modifier.width(120.dp).height(20.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                Spacer(modifier = Modifier.height(4.dp))
                Box(modifier = Modifier.width(80.dp).height(12.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
            }
        }
        
        // Agent Card fake
        Box(modifier = Modifier.fillMaxWidth().padding(16.dp).height(80.dp).clip(RoundedCornerShape(16.dp)).shimmerEffect())
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Chat bubbles fake
        repeat(3) { index ->
            val isUser = index % 2 != 0
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
            ) {
                if (!isUser) {
                    Box(modifier = Modifier.size(36.dp).clip(CircleShape).shimmerEffect())
                    Spacer(modifier = Modifier.width(8.dp))
                }
                Box(
                    modifier = Modifier
                        .width(200.dp)
                        .height(80.dp)
                        .clip(RoundedCornerShape(16.dp))
                        .shimmerEffect()
                )
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // Input bar fake
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(modifier = Modifier.size(24.dp).clip(CircleShape).shimmerEffect())
            Spacer(modifier = Modifier.width(16.dp))
            Box(modifier = Modifier.weight(1f).height(48.dp).clip(RoundedCornerShape(24.dp)).shimmerEffect())
            Spacer(modifier = Modifier.width(16.dp))
            Box(modifier = Modifier.size(48.dp).clip(CircleShape).shimmerEffect())
        }
    }
}
"""

c += skeletons

with open("app/src/main/java/com/example/ui/components/SkeletonScreens.kt", "w") as f:
    f.write(c)

