import re

file_path = "app/src/main/java/com/example/MainActivity.kt"
with open(file_path, "r") as f:
    content = f.read()

imports = """import com.zegocloud.uikit.prebuilt.call.invite.ZegoUIKitPrebuiltCallInvitationConfig
import com.zegocloud.uikit.prebuilt.call.invite.ZegoUIKitPrebuiltCallService
"""

if "import com.zegocloud.uikit" not in content:
    content = content.replace("import android.os.Bundle", imports + "import android.os.Bundle")

init_code = """
      LaunchedEffect(Unit) {
          val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
          auth.addAuthStateListener { firebaseAuth ->
              val user = firebaseAuth.currentUser
              if (user != null) {
                  try {
                      // Attempt to fetch Zego credentials (ensure they are strings in build config or handle long)
                      val appIdStr = com.example.BuildConfig.ZEGO_APP_ID
                      val appID = appIdStr.toLongOrNull() ?: 0L
                      val appSign = com.example.BuildConfig.ZEGO_APP_SIGN
                      if (appID != 0L && appSign.isNotBlank()) {
                          val callInvitationConfig = ZegoUIKitPrebuiltCallInvitationConfig()
                          ZegoUIKitPrebuiltCallService.init(
                              application, appID, appSign, user.uid, user.displayName ?: "User", callInvitationConfig
                          )
                      }
                  } catch (e: Exception) {
                      e.printStackTrace()
                  }
              } else {
                  try {
                      ZegoUIKitPrebuiltCallService.unInit()
                  } catch (e: Exception) {}
              }
          }
      }
"""

if "ZegoUIKitPrebuiltCallService.init" not in content:
    content = content.replace("val themeMode by userPreferences.themeMode.collectAsState(initial = 0)", init_code + "\n      val themeMode by userPreferences.themeMode.collectAsState(initial = 0)")

with open(file_path, "w") as f:
    f.write(content)
