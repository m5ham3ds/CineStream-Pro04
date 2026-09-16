import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    c = f.read()

target = """                            val exactMatch = sortedQ.find { it.name == targetQuality }
                            if (exactMatch != null) {
                                finalQualityUrl = exactMatch.url
                                finalQualityName = exactMatch.name
                            } else {
                                // Fallback logic
                                val targetHeight = targetQuality.replace("p", "").toIntOrNull() ?: 0
                                val closest = sortedQ.find { (it.name.replace("p", "").toIntOrNull() ?: 0) <= targetHeight }
                                if (closest != null) {
                                    finalQualityUrl = closest.url
                                    finalQualityName = closest.name
                                } else {
                                    finalQualityUrl = sortedQ.last().url
                                    finalQualityName = sortedQ.last().name
                                }
                            }"""

replace = """                            if (targetQuality == "Auto" || targetQuality.isEmpty()) {
                                finalQualityUrl = sortedQ.first().url
                                finalQualityName = sortedQ.first().name
                            } else {
                                val exactMatch = sortedQ.find { it.name.contains(targetQuality.replace("p", "")) }
                                if (exactMatch != null) {
                                    finalQualityUrl = exactMatch.url
                                    finalQualityName = exactMatch.name
                                } else {
                                    // Fallback logic
                                    val targetHeight = targetQuality.replace("p", "").toIntOrNull() ?: 0
                                    val closest = sortedQ.find { (it.name.replace("p", "").toIntOrNull() ?: 0) <= targetHeight }
                                    if (closest != null) {
                                        finalQualityUrl = closest.url
                                        finalQualityName = closest.name
                                    } else {
                                        finalQualityUrl = sortedQ.last().url
                                        finalQualityName = sortedQ.last().name
                                    }
                                }
                            }"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(c)
