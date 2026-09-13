import re
import os

translation_dict = {
    "A group of men fight for survival in a world where trust is a luxury.": ("desc_sample", "A group of men fight for survival in a world where trust is a luxury.", "مجموعة من الرجال يقاتلون من أجل البقاء في عالم حيث الثقة ترف."),
    "About": ("about", "About", "حول"),
    "About CineStream": ("about_app", "About CineStream", "حول التطبيق"),
    "Account": ("account", "Account", "الحساب"),
    "Active Devices": ("active_devices", "Active Devices", "الأجهزة النشطة"),
    "Active now • Riyadh, KSA": ("active_now_riyadh", "Active now • Riyadh, KSA", "نشط الآن • الرياض، السعودية"),
    "Add Story": ("add_story", "Add Story", "إضافة قصة"),
    "Allow others to search for you and see your profile": ("allow_search", "Allow others to search for you and see your profile", "السماح للآخرين بالبحث عنك ورؤية ملفك الشخصي"),
    "Android • Ready to connect": ("android_ready", "Android • Ready to connect", "أندرويد • جاهز للاتصال"),
    "App Crashed!": ("app_crashed", "App Crashed!", "توقف التطبيق!"),
    "App Settings": ("app_settings", "App Settings", "إعدادات التطبيق"),
    "Are you sure you want to sign out?": ("confirm_sign_out", "Are you sure you want to sign out?", "هل أنت متأكد أنك تريد تسجيل الخروج؟"),
    "Available Devices:": ("available_devices", "Available Devices:", "الأجهزة المتاحة:"),
    "Back to Folders": ("back_to_folders", "Back to Folders", "العودة للمجلدات"),
    "Basic": ("basic_plan", "Basic", "أساسي"),
    "Biography": ("biography", "Biography", "السيرة الذاتية"),
    "Birthplace": ("birthplace", "Birthplace", "مكان الميلاد"),
    "Born": ("born", "Born", "مواليد"),
    "Browse by Category": ("browse_by_category", "Browse by Category", "تصفح حسب الفئة"),
    "Cancel": ("cancel", "Cancel", "إلغاء"),
    "Change Password": ("change_password", "Change Password", "تغيير كلمة المرور"),
    "Choose Content Type": ("choose_content_type", "Choose Content Type", "اختر نوع المحتوى"),
    "Choose Your Plan": ("choose_plan", "Choose Your Plan", "اختر باقتك"),
    "CineStream": ("app_name", "CineStream", "CineStream"),
    "CineStream Community": ("community", "CineStream Community", "مجتمع CineStream"),
    "CineStream is your premium cinematic experience. Stream your favorite movies and series in high quality, anytime, anywhere.": ("app_desc_long", "CineStream is your premium cinematic experience. Stream your favorite movies and series in high quality, anytime, anywhere.", "سينما ستريم هو تجربتك السينمائية المميزة. شاهد أفلامك ومسلسلاتك المفضلة بجودة عالية في أي وقت ومكان."),
    "Completed": ("completed", "Completed", "مكتمل"),
    "Connect": ("connect", "Connect", "اتصال"),
    "Connection Status": ("connection_status", "Connection Status", "حالة الاتصال"),
    "Control what visitors can see about your profile.": ("control_visibility", "Control what visitors can see about your profile.", "تحكم في ما يمكن للزوار رؤيته في ملفك الشخصي."),
    "Copy": ("copy", "Copy", "نسخ"),
    "Copy Error": ("copy_error", "Copy Error", "نسخ الخطأ"),
    "Crash Error": ("crash_error", "Crash Error", "خطأ انهيار"),
    "Current Password": ("current_password", "Current Password", "كلمة المرور الحالية"),
    "Current Plan": ("current_plan", "Current Plan", "الباقة الحالية"),
    "Delete": ("delete", "Delete", "حذف"),
    "Delete Message": ("delete_message", "Delete Message", "حذف الرسالة"),
    "Delete for Everyone": ("delete_everyone", "Delete for Everyone", "حذف للجميع"),
    "Delete for Me": ("delete_for_me", "Delete for Me", "حذف لدي فقط"),
    "Do you want to set this as your new profile picture?": ("confirm_profile_pic", "Do you want to set this as your new profile picture?", "هل تريد تعيين هذه كصورة ملفك الشخصي الجديدة؟"),
    "Edit": ("edit", "Edit", "تعديل"),
    "Edit Profile": ("edit_profile", "Edit Profile", "تعديل الملف الشخصي"),
    "Edited": ("edited", "Edited", "معدلة"),
    "Email (Gmail)": ("email_hint", "Email (Gmail)", "البريد الإلكتروني (Gmail)"),
    "Enjoy ad-free streaming and exclusive content.": ("enjoy_ad_free", "Enjoy ad-free streaming and exclusive content.", "استمتع بمشاهدة بدون إعلانات ومحتوى حصري."),
    "Enter your email": ("enter_email", "Enter your email", "أدخل بريدك الإلكتروني"),
    "Episodes": ("episodes", "Episodes", "الحلقات"),
    "First Name": ("first_name", "First Name", "الاسم الأول"),
    "Forgot Password?": ("forgot_password", "Forgot Password?", "نسيت كلمة المرور؟"),
    "G": ("google_g", "G", "G"),
    "HD": ("hd", "HD", "HD"),
    "How it works?": ("how_it_works", "How it works?", "كيف تعمل؟"),
    "Known For": ("known_for", "Known For", "معروف بـ"),
    "Last Name": ("last_name", "Last Name", "الاسم الأخير"),
    "Last active: Yesterday • Riyadh, KSA": ("last_active_yesterday", "Last active: Yesterday • Riyadh, KSA", "آخر نشاط: أمس • الرياض، السعودية"),
    "Looking for devices...": ("looking_for_devices", "Looking for devices...", "جاري البحث عن أجهزة..."),
    "MacBook Air": ("macbook_air", "MacBook Air", "ماك بوك إير"),
    "Make sure both devices have Wi-Fi and are close to each other. Large files may take some time to transfer.": ("share_instruction_1", "Make sure both devices have Wi-Fi and are close to each other. Large files may take some time to transfer.", "تأكد من تشغيل الواي فاي في كلا الجهازين وتقاربهما. الملفات الكبيرة قد تستغرق بعض الوقت."),
    "Make sure the sender is on the same Wi-Fi network or Bluetooth is enabled. Transfer uses high-speed Wi-Fi Direct.": ("share_instruction_2", "Make sure the sender is on the same Wi-Fi network or Bluetooth is enabled. Transfer uses high-speed Wi-Fi Direct.", "تأكد أن المرسل على نفس شبكة الواي فاي أو البلوتوث مفعل. النقل يستخدم Wi-Fi Direct سريع."),
    "Manage Plan": ("manage_plan", "Manage Plan", "إدارة الباقة"),
    "Messages are end-to-end encrypted.\\nYour privacy is our priority.": ("e2e_encryption", "Messages are end-to-end encrypted.\\nYour privacy is our priority.", "الرسائل مشفرة من طرف إلى طرف.\\nخصوصيتك هي أولويتنا."),
    "Movies": ("movies", "Movies", "الأفلام"),
    "Nearby Devices": ("nearby_devices", "Nearby Devices", "الأجهزة القريبة"),
    "New Password": ("new_password", "New Password", "كلمة المرور الجديدة"),
    "No downloaded movies found.": ("no_downloads", "No downloaded movies found.", "لم يتم العثور على أفلام محملة."),
    "Offline Share": ("offline_share", "Offline Share", "مشاركة بدون إنترنت"),
    "Online": ("online", "Online", "متصل"),
    "Or continue with": ("continue_with", "Or continue with", "أو تابع باستخدام"),
    "POPULAR": ("popular_badge", "POPULAR", "شائع"),
    "Password": ("password", "Password", "كلمة المرور"),
    "Play Now": ("play_now", "Play Now", "تشغيل الآن"),
    "Preferences": ("preferences", "Preferences", "التفضيلات"),
    "Premium Member": ("premium_member", "Premium Member", "عضو مميز"),
    "Premium Plan": ("premium_plan", "Premium Plan", "باقة مميزة"),
    "Premium 👑": ("premium_crown", "Premium 👑", "مميز 👑"),
    "Privacy Settings": ("privacy_settings", "Privacy Settings", "إعدادات الخصوصية"),
    "Profile": ("profile", "Profile", "الملف الشخصي"),
    "Public Profile": ("public_profile", "Public Profile", "الملف العام"),
    "Quality": ("quality", "Quality", "الجودة"),
    "Quality:": ("quality_label", "Quality:", "الجودة:"),
    "R": ("rating_r", "R", "R"),
    "Ready to Play": ("ready_to_play", "Ready to Play", "جاهز للتشغيل"),
    "Ready to receive": ("ready_to_receive", "Ready to receive", "جاهز للاستلام"),
    "Receive Content": ("receive_content", "Receive Content", "استلام محتوى"),
    "Receive Media": ("receive_media", "Receive Media", "استلام وسائط"),
    "Receive from nearby devices": ("receive_from_nearby", "Receive from nearby devices", "استلام من أجهزة قريبة"),
    "Recent Transfers": ("recent_transfers", "Recent Transfers", "التحويلات الأخيرة"),
    "Remember me": ("remember_me", "Remember me", "تذكرني"),
    "Reset Password": ("reset_password", "Reset Password", "إعادة تعيين كلمة المرور"),
    "Restart App": ("restart_app", "Restart App", "إعادة تشغيل التطبيق"),
    "Results for \\": ("results_for", "Results for \\", "نتائج لـ \\"),
    "Save": ("save", "Save", "حفظ"),
    "Save Changes": ("save_changes", "Save Changes", "حفظ التغييرات"),
    "Scan": ("scan", "Scan", "بحث"),
    "Search by username to message...": ("search_username", "Search by username to message...", "ابحث باسم المستخدم للمراسلة..."),
    "Searching for video...": ("searching_video", "Searching for video...", "جاري البحث عن الفيديو..."),
    "Security": ("security", "Security", "الأمان"),
    "Select Download Quality": ("select_download_quality", "Select Download Quality", "اختر جودة التحميل"),
    "Select Quality": ("select_quality", "Select Quality", "اختر الجودة"),
    "Select Server": ("select_server", "Select Server", "اختر السيرفر"),
    "Select Server & Quality": ("select_server_quality", "Select Server & Quality", "اختر السيرفر والجودة"),
    "Select Source Website": ("select_source", "Select Source Website", "اختر موقع المصدر"),
    "Send": ("send", "Send", "إرسال"),
    "Send Content": ("send_content", "Send Content", "إرسال محتوى"),
    "Series / Anime": ("series_anime", "Series / Anime", "مسلسلات / أنمي"),
    "Share movies, series or anime": ("share_desc", "Share movies, series or anime", "شارك الأفلام، المسلسلات أو الأنمي"),
    "Sign Out": ("sign_out", "Sign Out", "تسجيل الخروج"),
    "Sign in to chat and share with others": ("sign_in_social", "Sign in to chat and share with others", "سجل دخولك للدردشة والمشاركة مع الآخرين"),
    "Sign in with Google": ("sign_in_google", "Sign in with Google", "تسجيل الدخول باستخدام جوجل"),
    "Sign out": ("sign_out2", "Sign out", "تسجيل الخروج"),
    "Skip": ("skip", "Skip", "تخطي"),
    "Source:": ("source_label", "Source:", "المصدر:"),
    "Stories": ("stories", "Stories", "القصص"),
    "Subscription": ("subscription", "Subscription", "الاشتراك"),
    "This account is private.": ("private_account", "This account is private.", "هذا الحساب خاص."),
    "Tips for faster transfer": ("tips_faster_transfer", "Tips for faster transfer", "نصائح لنقل أسرع"),
    "Today": ("today", "Today", "اليوم"),
    "Update Password": ("update_password", "Update Password", "تحديث كلمة المرور"),
    "Update Profile Picture": ("update_profile_pic", "Update Profile Picture", "تحديث صورة الملف الشخصي"),
    "Upgrade to Premium": ("upgrade_premium", "Upgrade to Premium", "الترقية للمميز"),
    "Upgrade to Premium to unlock all features": ("upgrade_premium_desc", "Upgrade to Premium to unlock all features", "قم بالترقية للمميز لفتح جميع الميزات"),
    "User not found": ("user_not_found", "User not found", "المستخدم غير موجود"),
    "Username": ("username", "Username", "اسم المستخدم"),
    "View All": ("view_all", "View All", "عرض الكل"),
    "View all": ("view_all_small", "View all", "عرض الكل"),
    "Waiting for action": ("waiting_for_action", "Waiting for action", "في انتظار الإجراء"),
    "Waiting for files...": ("waiting_for_files", "Waiting for files...", "في انتظار الملفات..."),
    "Welcome to": ("welcome_to", "Welcome to", "مرحباً بك في"),
    "Who do you want to delete this message for?": ("delete_msg_prompt", "Who do you want to delete this message for?", "لمن تريد حذف هذه الرسالة؟"),
    "You're Premium!": ("you_are_premium", "You're Premium!", "أنت عضو مميز!"),
    "Your Cinematic World, Anytime, Anywhere.": ("slogan1", "Your Cinematic World, Anytime, Anywhere.", "عالمك السينمائي، في أي وقت وأي مكان."),
    "Your ultimate destination for\\nmovies and series. Enjoy endless\\nentertainment, anytime, anywhere.": ("slogan2", "Your ultimate destination for\\nmovies and series. Enjoy endless\\nentertainment, anytime, anywhere.", "وجهتك المثالية\\nللأفلام والمسلسلات. استمتع بترفيه لا نهاية له، في أي وقت وأي مكان."),
    "iPhone 13 Pro": ("iphone_13", "iPhone 13 Pro", "iPhone 13 Pro"),
    "message": ("message", "message", "رسالة"),
    "username": ("username_small", "username", "اسم المستخدم"),
    "إدارة مصادر المشاهدة واستمتع بمحتوى أكثر": ("manage_sources", "Manage viewing sources and enjoy more content", "إدارة مصادر المشاهدة واستمتع بمحتوى أكثر"),
    "إعادة الفحص": ("rescan", "Rescan", "إعادة الفحص"),
    "إعادة المحاولة": ("retry", "Retry", "إعادة المحاولة"),
    "إعادة المحاولة مجدداً": ("retry_again", "Retry Again", "إعادة المحاولة مجدداً"),
    "إعادة محاولة استخراج الجودات": ("retry_extract", "Retry extracting qualities", "إعادة محاولة استخراج الجودات"),
    "إلغاء": ("cancel_ar", "Cancel", "إلغاء"),
    "إلغاء التثبيت": ("uninstall", "Uninstall", "إلغاء التثبيت"),
    "إلغاء العملية": ("cancel_op", "Cancel Operation", "إلغاء العملية"),
    "إلغاء تماماً": ("cancel_completely", "Cancel Completely", "إلغاء تماماً"),
    "اختر السيرفر": ("select_server_ar", "Select Server", "اختر السيرفر"),
    "اسحب للأعلى لتحميل المزيد": ("swipe_to_load", "Swipe up to load more", "اسحب للأعلى لتحميل المزيد"),
    "الإضافات": ("extensions", "Extensions", "الإضافات"),
    "الانتقال إلى الإضافات": ("go_to_extensions", "Go to Extensions", "الانتقال إلى الإضافات"),
    "البحث في الإضافات...": ("search_extensions", "Search in Extensions...", "البحث في الإضافات..."),
    "البحث في موقع آخر": ("search_other_site", "Search in another site", "البحث في موقع آخر"),
    "الرجاء الإنتظار، يتم جلب أحدث المعلومات من السيرفرات.": ("please_wait_servers", "Please wait, fetching latest info from servers.", "الرجاء الإنتظار، يتم جلب أحدث المعلومات من السيرفرات."),
    "العملية لا تزال جارية، هل أنت متأكد أنك تريد الإلغاء؟": ("cancel_confirm", "Operation is still in progress, are you sure you want to cancel?", "العملية لا تزال جارية، هل أنت متأكد أنك تريد الإلغاء؟"),
    "العودة لاختيار سيرفر آخر": ("back_select_server", "Back to select another server", "العودة لاختيار سيرفر آخر"),
    "تأكيد": ("confirm", "Confirm", "تأكيد"),
    "تأكيد التخطي": ("confirm_skip", "Confirm Skip", "تأكيد التخطي"),
    "تأكيد فتح المتصفح": ("confirm_browser", "Confirm open browser", "تأكيد فتح المتصفح"),
    "تثبيت": ("install", "Install", "تثبيت"),
    "تحميل المزيد من الحلقات": ("load_more_eps", "Load more episodes", "تحميل المزيد من الحلقات"),
    "تخطي الموقع الحالي": ("skip_current", "Skip current site", "تخطي الموقع الحالي"),
    "تم التحقق، متابعة": ("verified_continue", "Verified, continue", "تم التحقق، متابعة"),
    "تم حذف هذه الرسالة": ("msg_deleted", "This message was deleted", "تم حذف هذه الرسالة"),
    "جاري الإتصال بالسيرفرات المتاحة...": ("connecting_servers", "Connecting to available servers...", "جاري الإتصال بالسيرفرات المتاحة..."),
    "جاري تحميل الحلقات...": ("loading_eps", "Loading episodes...", "جاري تحميل الحلقات..."),
    "حدث خطأ في الاتصال بالإنترنت": ("net_error", "Internet connection error", "حدث خطأ في الاتصال بالإنترنت"),
    "روابط التحميل المباشرة": ("direct_links", "Direct Download Links", "روابط التحميل المباشرة"),
    "صفحة الإضافات": ("extensions_page", "Extensions Page", "صفحة الإضافات"),
    "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.": ("no_servers_found", "Sorry, no working servers found across supported sites.", "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة."),
    "فتح المتصفح يدوياً للتحقق": ("open_browser_manual", "Open browser manually to verify", "فتح المتصفح يدوياً للتحقق"),
    "فشل في العثور على أي جودة": ("no_quality_found", "Failed to find any quality", "فشل في العثور على أي جودة"),
    "لا توجد إضافات أخرى": ("no_other_ext", "No other extensions", "لا توجد إضافات أخرى"),
    "لم يتم تثبيت أي إضافات": ("no_ext_installed", "No extensions installed", "لم يتم تثبيت أي إضافات"),
    "لم يتم تثبيت أي إضافات أخرى للمتابعة. ماذا تريد أن تفعل؟": ("no_other_ext_prompt", "No other extensions installed to continue. What do you want to do?", "لم يتم تثبيت أي إضافات أخرى للمتابعة. ماذا تريد أن تفعل؟"),
    "متابعة": ("continue_btn", "Continue", "متابعة"),
    "ملاحظة": ("note", "Note", "ملاحظة"),
    "نعم": ("yes_ar", "Yes", "نعم"),
    "نعم، أكمل": ("yes_continue", "Yes, complete", "نعم، أكمل"),
    "نعم، إلغاء": ("yes_cancel", "Yes, cancel", "نعم، إلغاء"),
    "هل أنت متأكد أنك قمت بتخطي حماية Cloudflare بنجاح؟": ("confirm_cf", "Are you sure you bypassed Cloudflare successfully?", "هل أنت متأكد أنك قمت بتخطي حماية Cloudflare بنجاح؟"),
    "هل أنت متأكد من رغبتك في تخطي هذا الموقع والانتقال للتالي؟": ("confirm_skip_site", "Are you sure you want to skip this site?", "هل أنت متأكد من رغبتك في تخطي هذا الموقع والانتقال للتالي؟"),
    "هل أنت متأكد من رغبتك في فتح المتصفح يدوياً للتحقق من الرابط؟": ("confirm_open_browser", "Are you sure you want to open browser manually?", "هل أنت متأكد من رغبتك في فتح المتصفح يدوياً للتحقق من الرابط؟"),
    "يرجى التحقق من الشبكة والمحاولة مرة أخرى.": ("check_net_retry", "Please check network and try again.", "يرجى التحقق من الشبكة والمحاولة مرة أخرى."),
    "يرجى تثبيت إضافة واحدة على الأقل لجلب الخوادم والروابط.": ("install_ext_prompt", "Please install at least one extension to fetch servers.", "يرجى تثبيت إضافة واحدة على الأقل لجلب الخوادم والروابط."),
    "يرجى تخطي الحماية للمتابعة...": ("skip_protect_prompt", "Please bypass protection to continue...", "يرجى تخطي الحماية للمتابعة..."),
    "يمكنك تثبيت عدة إضافات للحصول على تجربة مشاهدة أفضل ومصادر أكثر.": ("install_multiple_ext", "You can install multiple extensions for better experience.", "يمكنك تثبيت عدة إضافات للحصول على تجربة مشاهدة أفضل ومصادر أكثر."),
}

import glob

# For replacing dynamic strings:
# We will do a generic replacement for standard `Text("str")`
# For strings containing variables like $ or ${}, we will leave them for now unless they match exactly.

def replace_in_files():
    for filepath in glob.glob('app/src/main/java/com/example/ui/**/*.kt', recursive=True):
        with open(filepath, 'r') as f:
            content = f.read()
            
        original_content = content
        
        for old_str, (key, en, ar) in translation_dict.items():
            # Escape old_str for regex safely
            # Note: The quotes are already in the file.
            old_str_escaped = re.escape(old_str)
            # Find exact matches inside Text("...") or Text(text = "...")
            # Using negative lookbehind to ensure we don't double replace
            pattern = r'Text\(\s*"' + old_str_escaped + r'"'
            replace = f'Text(stringResource(R.string.{key})'
            content = re.sub(pattern, replace, content)
            
            pattern2 = r'Text\(\s*text\s*=\s*"' + old_str_escaped + r'"'
            replace2 = f'Text(text = stringResource(R.string.{key})'
            content = re.sub(pattern2, replace2, content)
            
            # Replace placeholder = { Text("...") }
            pattern3 = r'placeholder\s*=\s*\{\s*Text\("' + old_str_escaped + r'"\)\s*\}'
            replace3 = f'placeholder = {{ Text(stringResource(R.string.{key})) }}'
            content = re.sub(pattern3, replace3, content)

            pattern4 = r'title\s*=\s*\{\s*Text\("' + old_str_escaped + r'"\)\s*\}'
            replace4 = f'title = {{ Text(stringResource(R.string.{key})) }}'
            content = re.sub(pattern4, replace4, content)

            pattern5 = r'text\s*=\s*\{\s*Text\("' + old_str_escaped + r'"\)\s*\}'
            replace5 = f'text = {{ Text(stringResource(R.string.{key})) }}'
            content = re.sub(pattern5, replace5, content)

            pattern6 = r'headlineContent\s*=\s*\{\s*Text\("' + old_str_escaped + r'"'
            replace6 = f'headlineContent = {{ Text(stringResource(R.string.{key})'
            content = re.sub(pattern6, replace6, content)
            
        if content != original_content:
            # Add import if needed
            if 'import androidx.compose.ui.res.stringResource' not in content:
                content = content.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.Text\nimport androidx.compose.ui.res.stringResource\nimport com.example.R')
                if 'import com.example.R' not in content:
                     content = content.replace('import androidx.compose.runtime.Composable', 'import androidx.compose.runtime.Composable\nimport com.example.R\nimport androidx.compose.ui.res.stringResource')

            with open(filepath, 'w') as f:
                f.write(content)

replace_in_files()

# Now update strings.xml
def update_xml(filepath, is_ar=False):
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>'
    else:
        with open(filepath, 'r') as f:
            content = f.read()

    new_strings = []
    for old_str, (key, en, ar) in translation_dict.items():
        if f'name="{key}"' not in content:
            val = ar if is_ar else en
            # Escape for XML
            val = val.replace("'", "\\'").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', '\\"')
            new_strings.append(f'    <string name="{key}">{val}</string>')
    
    if new_strings:
        content = content.replace('</resources>', '\n'.join(new_strings) + '\n</resources>')
        with open(filepath, 'w') as f:
            f.write(content)

update_xml('app/src/main/res/values/strings.xml', False)
update_xml('app/src/main/res/values-ar/strings.xml', True)

print("Translation replacements done.")
