import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# Fix Server list bottom text
server_bottom_target = """                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "تجربة موقع آخر",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth().clickable { showSkipSiteConfirmDialog = true }.padding(8.dp)
                                )
                            }
                        } else {
                            if (isExtractingQuality) {"""
server_bottom_replace = """                                item {
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text = "تجربة موقع آخر",
                                        color = MaterialTheme.colorScheme.primary,
                                        fontSize = 14.sp,
                                        fontWeight = FontWeight.Bold,
                                        textAlign = TextAlign.Center,
                                        modifier = Modifier.fillMaxWidth().clickable { showSkipSiteConfirmDialog = true }.padding(8.dp)
                                    )
                                }
                            }
                        } else {
                            if (isExtractingQuality) {"""
c = c.replace(server_bottom_target, server_bottom_replace)

# Fix Quality list bottom text
quality_bottom_target = """                                Spacer(modifier = Modifier.height(16.dp))
                                Text(
                                    text = "تبديل السيرفر",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = TextAlign.Center,
                                    modifier = Modifier.fillMaxWidth().clickable {
                                        isExtractingQuality = false
                                        extractedQualities = emptyList()
                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                        selectedServerForQuality = null
                                    }.padding(8.dp)
                                )
                            }
                        }
                    }
                }
            }"""

quality_bottom_replace = """                                item {
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text = "تبديل السيرفر",
                                        color = MaterialTheme.colorScheme.primary,
                                        fontSize = 14.sp,
                                        fontWeight = FontWeight.Bold,
                                        textAlign = TextAlign.Center,
                                        modifier = Modifier.fillMaxWidth().clickable {
                                            isExtractingQuality = false
                                            extractedQualities = emptyList()
                                            com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                            selectedServerForQuality = null
                                        }.padding(8.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }"""
c = c.replace(quality_bottom_target, quality_bottom_replace)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

