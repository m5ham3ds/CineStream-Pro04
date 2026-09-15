import re
with open("app/src/main/java/com/example/utils/NotificationHelper.kt", "r") as f:
    content = f.read()

# Fix showDownloadStarted
start_idx = content.find("fun showDownloadStarted")
end_idx = content.find("fun showDownloadCompleted")

part1 = content[:start_idx]
part2 = content[start_idx:end_idx].replace("            .setTimeoutAfter(3000)\n", "")
part3 = content[end_idx:]

with open("app/src/main/java/com/example/utils/NotificationHelper.kt", "w") as f:
    f.write(part1 + part2 + part3)
