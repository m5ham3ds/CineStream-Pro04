import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

target = """                                    }
                                }
                                item {
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text = "تبديل السيرفر",
                                        color = MaterialTheme.colorScheme.primary,"""

replace = """                                    }
                                    item {
                                        Spacer(modifier = Modifier.height(16.dp))
                                        Text(
                                            text = "تبديل السيرفر",
                                            color = MaterialTheme.colorScheme.primary,"""
c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

