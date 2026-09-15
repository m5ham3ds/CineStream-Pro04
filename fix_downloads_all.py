import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # MoviesScreen
    if 'MoviesScreen.kt' in filepath:
        content = re.sub(
            r'downloadRepository\.addToDownloads\(DownloadItem\(\s*id = selectedMediaId,\s*title = selectedMediaTitle,',
            r'downloadRepository.addToDownloads(DownloadItem(\n                            id = selectedMediaId,\n                            mediaId = selectedMediaId,\n                            title = selectedMediaTitle,',
            content
        )
    # HomeScreen
    if 'HomeScreen.kt' in filepath:
        content = re.sub(
            r'downloadRepository\.addToDownloads\(DownloadItem\(\s*id = selectedMediaId,\s*title = selectedMediaTitle,',
            r'downloadRepository.addToDownloads(DownloadItem(\n                            id = selectedMediaId,\n                            mediaId = selectedMediaId,\n                            title = selectedMediaTitle,',
            content
        )
    # AnimeScreen
    if 'AnimeScreen.kt' in filepath:
        content = re.sub(
            r'downloadRepository\.addToDownloads\(DownloadItem\(\s*id = selectedMediaId,\s*title = selectedMediaTitle,',
            r'downloadRepository.addToDownloads(DownloadItem(\n                            id = selectedMediaId,\n                            mediaId = selectedMediaId,\n                            title = selectedMediaTitle,',
            content
        )
    # SeriesScreen
    if 'SeriesScreen.kt' in filepath:
        content = re.sub(
            r'downloadRepository\.addToDownloads\(DownloadItem\(\s*id = selectedMediaId,\s*title = selectedMediaTitle,',
            r'downloadRepository.addToDownloads(DownloadItem(\n                            id = selectedMediaId,\n                            mediaId = selectedMediaId,\n                            title = selectedMediaTitle,',
            content
        )
    # ShareScreen
    if 'ShareScreen.kt' in filepath:
        content = re.sub(
            r'DownloadItem\(\s*id = mediaId,\s*title = title,',
            r'DownloadItem(\n                        id = mediaId,\n                        mediaId = mediaId,\n                        title = title,',
            content
        )
    # BatchDownloadSheet
    if 'BatchDownloadSheet.kt' in filepath:
        content = re.sub(
            r'DownloadItem\(\s*id = ep\.id,',
            r'DownloadItem(\n                                                        id = "${series.id}_${ep.id}",\n                                                        mediaId = series.id.toString(),',
            content
        )
        content = re.sub(
            r'AndroidDownloader\.downloadVideo\(context, preferredSource\.url, "(.*?)", epIdStr\)',
            r'AndroidDownloader.downloadVideo(context, preferredSource.url, "\1", "${series.id}_${ep.id}")',
            content
        )
        # also the case where epIdStr wasn't passed initially:
        content = re.sub(
            r'AndroidDownloader\.downloadVideo\(context, preferredSource\.url, "(.*?)"\)',
            r'AndroidDownloader.downloadVideo(context, preferredSource.url, "\1", "${series.id}_${ep.id}")',
            content
        )

    with open(filepath, 'w') as f:
        f.write(content)

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt",
    "app/src/main/java/com/example/ui/components/BatchDownloadSheet.kt"
]

for fp in files_to_fix:
    fix_file(fp)

