import re

with open("/tmp/ServerSelectionDialog.txt", "r") as f:
    code = f.read()

# 1. Add states
state_injection = """
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }
"""
code = code.replace("var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }", "var showSkipSiteConfirmDialog by remember { mutableStateOf(false) }\n" + state_injection)

# 2. Extract AndroidView
av_start = code.find("                            key(retryTrigger) {\n                                AndroidView(")
av_end_str = "loadUrl(targetUrl)\n                                        }\n                                    }\n                                )"
av_end = code.find(av_end_str) + len(av_end_str)
android_view_block = code[av_start:av_end] + "\n                            }"

# 3. Remove AndroidView from its current place
code = code.replace(android_view_block, "/* WEBVIEW WAS HERE */")

# 4. Remove the Cloudflare Confirmation overlay (which is inside the AnimatedContent)
cf_overlay = """// 1.5 The Cloudflare Confirmation Button overlay
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
code = code.replace(cf_overlay, "")

# 5. Restructure the main Box
main_box_find = "        Box(\n            modifier = Modifier\n                .fillMaxWidth(0.95f)"
main_box_idx = code.find(main_box_find)

new_structure_top = """
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            
            // --- THE WEBVIEW (Draggable if Cloudflare, hidden otherwise) ---
            Box(
                modifier = if (isCloudflare) {
                    Modifier
                        .offset { androidx.compose.ui.unit.IntOffset(offsetX.toInt(), offsetY.toInt()) }
                        .pointerInput(Unit) {
                            androidx.compose.foundation.gestures.detectDragGestures { change, dragAmount ->
                                change.consume()
                                offsetX += dragAmount.x
                                offsetY += dragAmount.y
                            }
                        }
                        .fillMaxWidth(0.9f)
                        .fillMaxHeight(0.85f)
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
                            textAlign = TextAlign.Center,
                            color = Color.Black,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        androidx.compose.material3.Button(
                            onClick = { showManualConfirmDialog = true },
                            modifier = Modifier
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                                .fillMaxWidth(),
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                        ) {
                            Text("تم التحقق، متابعة", color = Color.White)
                        }
                    }
                    
                    // The WebView block
                    ANDROID_VIEW_PLACEHOLDER
                }
            }
            
            if (!isCloudflare) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.95f)
"""
new_structure_top = new_structure_top.replace("ANDROID_VIEW_PLACEHOLDER", android_view_block)

code = code[:main_box_idx] + new_structure_top + code[main_box_idx + len("        Box(\n            modifier = Modifier\n                .fillMaxWidth(0.95f)"):]

# 6. We need to close the `if (!isCloudflare) {` block. 
# It ends right before `// Hidden Extractor for Quality`
extractor_idx = code.find("        // Hidden Extractor for Quality")
code = code[:extractor_idx] + "            }\n\n" + code[extractor_idx:]

# 7. Also move the dialogs out of the inner Column and into the outer Box!
# Currently showManualConfirmDialog and showCancelConfirmDialog are inside the 95% Box. 
# Let's just leave them there, they will still render because they are `AlertDialog` (which uses a separate Window).
# Actually, if (!isCloudflare) wraps the 95% Box, then when isCloudflare is true, the `showManualConfirmDialog` inside it WILL NOT RENDER!
# So we MUST move `showManualConfirmDialog` out.
# Find showManualConfirmDialog block:
man_dialog_start = code.find("                if (showManualConfirmDialog) {\n                    androidx.compose.material3.AlertDialog(")
man_dialog_end_str = "                    )\n                }"
man_dialog_end = code.find(man_dialog_end_str, man_dialog_start) + len(man_dialog_end_str)
man_dialog_block = code[man_dialog_start:man_dialog_end]

code = code.replace(man_dialog_block, "")
# Put it before `// Hidden Extractor for Quality`
code = code.replace("        // Hidden Extractor for Quality", man_dialog_block + "\n\n        // Hidden Extractor for Quality")


with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(code)

print("Patched successfully")
