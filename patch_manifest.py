import re
with open("app/src/main/AndroidManifest.xml", "r") as f:
    c = f.read()

if "StreamDownloaderService" not in c:
    c = c.replace("</application>", "    <service android:name=\".utils.StreamDownloaderService\" android:foregroundServiceType=\"dataSync\" />\n    </application>")
    c = c.replace("<uses-permission android:name=\"android.permission.INTERNET\" />", "<uses-permission android:name=\"android.permission.INTERNET\" />\n    <uses-permission android:name=\"android.permission.FOREGROUND_SERVICE\" />\n    <uses-permission android:name=\"android.permission.FOREGROUND_SERVICE_DATA_SYNC\" />")
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write(c)
