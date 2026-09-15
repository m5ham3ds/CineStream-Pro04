with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

# Replace assignments of currentUserFlow to also call syncFromCloud
content = content.replace(
    'repository.currentUserFlow.value = snapshot.toObject(User::class.java)',
    'repository.currentUserFlow.value = snapshot.toObject(User::class.java)\n                            com.example.data.sync.CloudSyncManager(getApplication()).syncFromCloud(firebaseUser.uid)'
)

content = content.replace(
    'repository.currentUserFlow.value = newUser',
    'repository.currentUserFlow.value = newUser\n                            com.example.data.sync.CloudSyncManager(getApplication()).syncFromCloud(firebaseUser.uid)'
)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
