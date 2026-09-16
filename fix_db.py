with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "r") as f:
    c = f.read()

c = c.replace('dao.getDownloadByIdSync(fileId)', 'dao.getItemById(fileId)')
c = c.replace('dao.update(updated)', 'dao.updateItem(updated)')

with open("app/src/main/java/com/example/utils/StreamDownloaderService.kt", "w") as f:
    f.write(c)
