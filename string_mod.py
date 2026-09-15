import re

with open("app/src/main/res/values/strings.xml", "r") as f:
    content = f.read()

download_strings = """
    <string name="download_settings">Download Settings</string>
    <string name="max_concurrent_downloads">Max Concurrent Downloads</string>
    <string name="max_segments_per_download">Max Segments</string>
    <string name="download_network">Download Network</string>
    <string name="network_all">All (WiFi &amp; Cellular)</string>
    <string name="network_wifi">Wi-Fi Only</string>
    <string name="network_cellular">Cellular Only</string>
    <string name="configure_downloads">Configure multi-threading and network</string>
"""

if "download_settings" not in content:
    content = content.replace("</resources>", download_strings + "\n</resources>")

with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(content)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    content_ar = f.read()

download_strings_ar = """
    <string name="download_settings">إعدادات التنزيل</string>
    <string name="max_concurrent_downloads">أقصى عدد للتنزيلات المتزامنة</string>
    <string name="max_segments_per_download">أقصى عدد للأجزاء</string>
    <string name="download_network">شبكة التنزيل</string>
    <string name="network_all">الكل (واي فاي وبيانات الهاتف)</string>
    <string name="network_wifi">واي فاي فقط</string>
    <string name="network_cellular">بيانات الهاتف فقط</string>
    <string name="configure_downloads">تكوين التنزيل المتعدد والشبكة</string>
"""
if "download_settings" not in content_ar:
    content_ar = content_ar.replace("</resources>", download_strings_ar + "\n</resources>")

with open("app/src/main/res/values-ar/strings.xml", "w") as f:
    f.write(content_ar)
