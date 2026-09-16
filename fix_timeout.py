import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    c = f.read()

target = """        if (phase == "INIT") {
            statusMessage = "جاري التحضير للحلقة ${episode.episodeNumber}..."
            delay(500)
            phase = "GETTING_SERVERS"
        }
    }"""
replace = """        if (phase == "INIT") {
            statusMessage = "جاري التحضير للحلقة ${episode.episodeNumber}..."
            delay(500)
            phase = "GETTING_SERVERS"
        }
        
        // Timeout mechanism
        if (phase == "GETTING_SERVERS" || phase == "EXTRACTING_URL") {
            val timeoutPhase = phase
            val timeoutIndex = currentIndex
            delay(15000) // 15 seconds timeout
            if (phase == timeoutPhase && currentIndex == timeoutIndex) {
                // Timeout occurred
                currentIndex++
                phase = "INIT"
            }
        }
    }"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(c)
