import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    code = f.read()

# Let's add offsetX, offsetY to the top states
state_injection = """
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }
"""
code = code.replace("var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }", "var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }\n" + state_injection)

# Now, we need to wrap the main Box in a Box(fillMaxSize)
# The main dialog box starts around line 169
# Box(
#     modifier = Modifier
#         .fillMaxWidth(0.95f)

main_box_start = code.find("Box(\n        modifier = Modifier\n            .fillMaxWidth(0.95f)")

# Find the AndroidView block
android_view_start = code.find("key(retryTrigger) {\n                                AndroidView(")

# Find where AndroidView ends (it ends with loadUrl(targetUrl) \n } \n } \n ) \n } )
android_view_end_str = "loadUrl(targetUrl)\n                                        }\n                                    }\n                                )\n                            }"

android_view_end = code.find(android_view_end_str) + len(android_view_end_str)

android_view_block = code[android_view_start:android_view_end]

# Now we need to remove the whole `if (isLoading && !isFailed) { AnimatedContent(...) ... }` block where the WebView was?
# Actually, the AnimatedContent block handles both the WebView and the "Overlay UI" (the loading circles).
# Let's just remove the `key(retryTrigger) { AndroidView(...) }` and `// 1.5 The Cloudflare Confirmation Button overlay`
# and leave the `// 2. The Overlay UI` as it is, since it already checks `if (currentStatus != "CLOUDFLARE")`.

code = code.replace(android_view_block, "/* WEBVIEW_MOVED_HERE */")

cloudflare_btn = """// 1.5 The Cloudflare Confirmation Button overlay
                            if (currentStatus == "CLOUDFLARE") {
                                Box(modifier = Modifier.fillMaxSize().padding(bottom = 16.dp), contentAlignment = Alignment.BottomCenter) {
                                    Button(
                                        onClick = { showManualConfirmDialog = true },
                                        colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                                    ) {
                                        Text("تم التحقق، متابعة", color = Color.White, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }"""
code = code.replace(cloudflare_btn, "")

# Now we inject the new structure at `main_box_start`.
# But wait, `main_box_start` is the 95% width Box.
# We will replace it with:
# Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
#    // The Cloudflare WebView Container
#    ...
#    if (!isCloudflare) {
#       // The original 95% box
#    }
# }

new_wrapper_start = """
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        // --- 1. The always-alive WebView ---
        Box(
            modifier = if (isCloudflare) {
                Modifier
                    .offset { androidx.compose.ui.unit.IntOffset(offsetX.kotlin.math.roundToInt(), offsetY.kotlin.math.roundToInt()) }
                    .pointerInput(Unit) {
                        androidx.compose.foundation.gestures.detectDragGestures { change, dragAmount ->
                            change.consume()
                            offsetX += dragAmount.x
                            offsetY += dragAmount.y
                        }
                    }
                    .fillMaxWidth(0.9f)
                    .fillMaxHeight(0.8f)
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color.White)
                    .zIndex(100f)
            } else {
                Modifier.size(1.dp).alpha(0.01f).zIndex(-1f)
            }
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                if (isCloudflare) {
                    Text(
                        text = "يرجى تخطي الحماية للمتابعة...",
                        modifier = Modifier
                            .padding(16.dp)
                            .fillMaxWidth(),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                        color = Color.Black,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    androidx.compose.material3.Button(
                        onClick = { showManualConfirmDialog = true },
                        modifier = Modifier
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                            .fillMaxWidth()
                    ) {
                        Text("تم التحقق، متابعة")
                    }
                }
                
                // --- ANDROID VIEW GOES HERE ---
                ANDROID_VIEW_PLACEHOLDER
            }
        }

        // --- 2. The Main Server Dialog (Shown ONLY if NOT Cloudflare) ---
        if (!isCloudflare) {
            Box(
                modifier = Modifier
                    .fillMaxWidth(0.95f)
"""

new_wrapper_start = new_wrapper_start.replace("ANDROID_VIEW_PLACEHOLDER", android_view_block)

# Fix imports in string
new_wrapper_start = new_wrapper_start.replace("offsetX.kotlin.math.roundToInt()", "kotlin.math.roundToInt(offsetX)").replace("offsetY.kotlin.math.roundToInt()", "kotlin.math.roundToInt(offsetY)")
new_wrapper_start = new_wrapper_start.replace("kotlin.math.roundToInt(offsetX)", "offsetX.toInt()").replace("kotlin.math.roundToInt(offsetY)", "offsetY.toInt()") # Simpler

code = code[:main_box_start] + new_wrapper_start + code[main_box_start + len("    Box(\n        modifier = Modifier\n            .fillMaxWidth(0.95f)"):]

# Now we must close the `if (!isCloudflare) {` block at the end of the 95% Box.
# The 95% Box ends just before `// Hidden Extractor for Quality`
hidden_ext_start = code.find("// Hidden Extractor for Quality")
if hidden_ext_start != -1:
    code = code[:hidden_ext_start] + "        }\n" + code[hidden_ext_start:]
else:
    print("Error: Could not find hidden extractor")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(code)

print("Rewrite complete.")
