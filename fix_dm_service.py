import re
with open("app/src/main/java/com/example/data/repository/DownloadManagerService.kt", "r") as f:
    c = f.read()

# Remove the while loop in init()
c = re.sub(r'scope\.launch\s*\{\s*while\s*\(true\)\s*\{\s*try\s*\{\s*processQueue\(\)\s*\}\s*catch\s*\(e:\s*Exception\)\s*\{\s*e\.printStackTrace\(\)\s*\}\s*delay\(3000\)\s*\}\s*\}', '', c)

with open("app/src/main/java/com/example/data/repository/DownloadManagerService.kt", "w") as f:
    f.write(c)

