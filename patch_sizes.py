with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

# Make profile sizes smaller
content = content.replace("fontSize = 18.sp,", "fontSize = 14.sp,") # You're premium
content = content.replace("fontSize = 32.sp", "fontSize = 24.sp") # Avatar letter / crown
content = content.replace("fontSize = 16.sp", "fontSize = 13.sp") # Name, Stats count, Logout, items
content = content.replace("fontSize = 12.sp", "fontSize = 10.sp") # Subtitles, @username
content = content.replace("fontSize = 14.sp", "fontSize = 12.sp") # Item title
content = content.replace("fontSize = 10.sp", "fontSize = 9.sp")  # Stat label, GOOD STORIES NEVER END

# Make icons smaller
content = content.replace("size(24.dp)", "size(20.dp)") # Stat icons
content = content.replace("size(18.dp)", "size(16.dp)") # List item icons
content = content.replace("size(36.dp)", "size(30.dp)") # List item circle wrapper
content = content.replace("size(80.dp)", "size(64.dp)") # Avatar size

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
