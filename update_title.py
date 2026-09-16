import re

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "r") as f:
    c = f.read()

target = """            val baseTitle = if (series.title.contains(" - S") && series.title.contains("E")) {
                series.title.substringBefore(" - S").trim()
            } else series.title"""
replace = """            val rawTitle = series.originalTitle ?: series.title
            val baseTitle = if (rawTitle.contains(" - S") && rawTitle.contains("E")) {
                rawTitle.substringBefore(" - S").trim()
            } else rawTitle"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/components/BatchDownloadProcessor.kt", "w") as f:
    f.write(c)
