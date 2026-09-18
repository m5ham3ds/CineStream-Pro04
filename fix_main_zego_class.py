import re

file_path = "app/src/main/java/com/example/MainActivity.kt"
with open(file_path, "r") as f:
    content = f.read()

# Change ZegoUIKitPrebuiltCallService to ZegoUIKitPrebuiltCallInvitationService
content = content.replace("ZegoUIKitPrebuiltCallService", "ZegoUIKitPrebuiltCallInvitationService")

with open(file_path, "w") as f:
    f.write(content)
