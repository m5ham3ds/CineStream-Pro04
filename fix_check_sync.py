with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    'repository.getCurrentUser()',
    'repository.getCurrentUser()\n            if (repository.auth.currentUser != null) {\n                com.example.data.sync.CloudSyncManager(getApplication()).syncFromCloud(repository.auth.currentUser!!.uid)\n            }'
)

with open("app/src/main/java/com/example/ui/screens/auth/AuthViewModel.kt", "w") as f:
    f.write(content)
