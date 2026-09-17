import re

with open("app/src/main/res/values/strings.xml", "r") as f:
    c = f.read()

if '<string name="notifications">' not in c:
    additions_en = """
    <string name="notifications">Notifications</string>
    <string name="no_notifications_yet">No notifications yet</string>
    <string name="help_support">Help &amp; Support</string>
    <string name="cinestream_support">CineStream Support</string>
    <string name="support_online">Online</string>
    <string name="support_status">Online • Usually replies within a few minutes</string>
    <string name="type_a_message">Type a message...</string>
    <string name="today">Today</string>
</resources>
"""
    c = c.replace("</resources>", additions_en)
    with open("app/src/main/res/values/strings.xml", "w") as f:
        f.write(c)

with open("app/src/main/res/values-ar/strings.xml", "r") as f:
    c_ar = f.read()

if '<string name="notifications">' not in c_ar:
    additions_ar = """
    <string name="notifications">الإشعارات</string>
    <string name="no_notifications_yet">لا توجد إشعارات حالياً</string>
    <string name="help_support">المساعدة والدعم</string>
    <string name="cinestream_support">دعم CineStream</string>
    <string name="support_online">متصل</string>
    <string name="support_status">متصل • عادة ما يرد خلال دقائق قليلة</string>
    <string name="type_a_message">اكتب رسالة...</string>
    <string name="today">اليوم</string>
</resources>
"""
    c_ar = c_ar.replace("</resources>", additions_ar)
    with open("app/src/main/res/values-ar/strings.xml", "w") as f:
        f.write(c_ar)

