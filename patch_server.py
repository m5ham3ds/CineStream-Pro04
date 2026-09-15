with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip() == ")" and "}" in lines[i-1] and "AndroidView" in "".join(lines[i-40:i]):
        if "loadUrl(targetUrl)" in "".join(lines[i-5:i]):
            lines[i] = "                                    },\n                                    onRelease = { webView ->\n                                        webView.stopLoading()\n                                        webView.destroy()\n                                    }\n                                )\n"
            break

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.writelines(lines)
