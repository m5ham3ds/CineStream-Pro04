with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

target = """    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServerLinks else emptyMap()
    ) }"""

replacement = """    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServerLinks else emptyMap()
    ) }
    var extractedServerIds by remember { mutableStateOf<Map<String, String>>(
        if (ServerStateStore.currentMediaKey == mediaKey) ServerStateStore.extractedServerIds else emptyMap()
    ) }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
