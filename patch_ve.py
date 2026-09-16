import re

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

target1 = """                            } else {
                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, targetServerId)
                                view.evaluateJavascript(autoPlayScript, null)
                            }"""

replacement1 = """                            } else {
                                val currentTargetServerId = view.getTag(com.example.R.id.tag_server_id) as? String ?: targetServerId
                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, currentTargetServerId)
                                view.evaluateJavascript(autoPlayScript, null)
                            }"""

target2 = """            if (lastUrl != url) {
                webView.setTag(com.example.R.id.tag_url, url)
                webView.setTag(com.example.R.id.tag_server, targetServer)
                val extraHeaders = mutableMapOf<String, String>()"""

replacement2 = """            if (lastUrl != url) {
                webView.setTag(com.example.R.id.tag_url, url)
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.setTag(com.example.R.id.tag_server_id, targetServerId)
                val extraHeaders = mutableMapOf<String, String>()"""

target3 = """            } else if (lastServer != targetServer) {
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.reload() // Server changed, reload the page
            }"""

replacement3 = """            } else if (lastServer != targetServer) {
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.setTag(com.example.R.id.tag_server_id, targetServerId)
                webView.reload() // Server changed, reload the page
            }"""

content = content.replace(target1, replacement1).replace(target2, replacement2).replace(target3, replacement3)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
