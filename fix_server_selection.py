import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_launched_effect = """    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= safeSites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentExtension = safeSites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        forceBypassComplete = false
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null"""

new_launched_effect = """    LaunchedEffect(currentSiteIndex, retryTrigger) {
        if (!isLoading && extractedServers.isNotEmpty()) {
            return@LaunchedEffect
        }
        if (currentSiteIndex >= safeSites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentExtension = safeSites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        forceBypassComplete = false
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null"""

if old_launched_effect in content:
    content = content.replace(old_launched_effect, new_launched_effect)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Updated LaunchedEffect")
else:
    print("Could not find LaunchedEffect")
