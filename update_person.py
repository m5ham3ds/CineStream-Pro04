import re

with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "r") as f:
    c = f.read()

# Make sure shimmerEffect is imported
import_stmt = "import com.example.ui.components.shimmerEffect"
if import_stmt not in c:
    c = c.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\n" + import_stmt)

# Target the loading state
target_loading = """        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator(color = MaterialTheme.colorScheme.primary) }
        } else if (uiState.person != null) {"""

replace_loading = """        if (uiState.isLoading) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // Header profile skeleton
                Box(
                    modifier = Modifier
                        .size(140.dp)
                        .clip(CircleShape)
                        .shimmerEffect()
                )
                Spacer(modifier = Modifier.height(16.dp))
                // Name skeleton
                Box(modifier = Modifier.width(180.dp).height(28.dp).clip(RoundedCornerShape(8.dp)).shimmerEffect())
                Spacer(modifier = Modifier.height(8.dp))
                // Known for skeleton
                Box(modifier = Modifier.width(120.dp).height(16.dp).clip(RoundedCornerShape(8.dp)).shimmerEffect())
                Spacer(modifier = Modifier.height(24.dp))
                
                // Info row skeleton
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    Box(modifier = Modifier.width(80.dp).height(60.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
                    Box(modifier = Modifier.width(80.dp).height(60.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
                }
                
                Spacer(modifier = Modifier.height(32.dp))
                // Biography skeleton
                Box(modifier = Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                Spacer(modifier = Modifier.height(8.dp))
                Box(modifier = Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                Spacer(modifier = Modifier.height(8.dp))
                Box(modifier = Modifier.fillMaxWidth(0.7f).height(16.dp).clip(RoundedCornerShape(4.dp)).shimmerEffect())
                
                Spacer(modifier = Modifier.height(32.dp))
                // Known for list skeleton
                Box(modifier = Modifier.width(120.dp).height(24.dp).clip(RoundedCornerShape(8.dp)).shimmerEffect().align(Alignment.Start))
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(modifier = Modifier.width(110.dp).height(160.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
                    Box(modifier = Modifier.width(110.dp).height(160.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
                    Box(modifier = Modifier.width(110.dp).height(160.dp).clip(RoundedCornerShape(12.dp)).shimmerEffect())
                }
            }
        } else if (uiState.person != null) {"""

c = c.replace(target_loading, replace_loading)

with open("app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt", "w") as f:
    f.write(c)

