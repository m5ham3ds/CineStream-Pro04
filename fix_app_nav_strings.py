file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('"Guest User"', 'stringResource(R.string.guest_user)')
content = content.replace('"Free Account"', 'stringResource(R.string.free_account)')
content = content.replace('"Premium User"', 'stringResource(R.string.premium_user)')
content = content.replace('"Log Out"', 'stringResource(R.string.log_out)')
content = content.replace('Text("Log Out"', 'Text(stringResource(R.string.log_out)')

with open(file_path, "w") as f:
    f.write(content)
