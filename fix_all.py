import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# We need to extract the parts and piece them together.
# Let's just use regex to replace everything from `} else if (selectedServerForQuality == null) {` up to `extractingEmbedUrl?.let { url ->`
pattern = re.compile(r"\} else if \(selectedServerForQuality == null\) \{.*?(?=extractingEmbedUrl\?\.let \{ url ->)", re.DOTALL)

replacement = """} else if (selectedServerForQuality == null) {
                            LazyColumn(
                                modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                items(extractedServers) { server ->
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clip(RoundedCornerShape(16.dp))
                                            .background(Color(0xFF16161A))
                                            .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                            .clickable {
                                                val finalUrl = extractedServerLinks[server] ?: ""
                                                val dLink = extractedDownloadLinks[server] ?: ""
                                                val watchUrl = if (finalUrl.contains("akamaized.net") || finalUrl.endsWith(".m3u8") || finalUrl.endsWith(".mp4")) {
                                                    finalUrl
                                                } else if (dLink.isNotEmpty()) {
                                                    dLink
                                                } else {
                                                    finalUrl
                                                }
                                                if (isDownloadMode) {
                                                    if (watchUrl.contains(".mp4")) {
                                                        com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList()
                                                        onPlay(watchUrl, server, currentSiteName)
                                                    } else {
                                                        selectedServerForQuality = server
                                                        isExtractingQuality = true
                                                        qualityExtractionMessage = "جاري استخراج الجودات لـ $server..."
                                                        if (watchUrl.contains(".m3u8") || watchUrl.contains("akamaized.net")) {
                                                            coroutineScope.launch {
                                                                val q = com.example.utils.M3U8Parser.getQualities(watchUrl)
                                                                extractedQualities = q
                                                                com.example.ui.screens.player.ServerStateStore.extractedQualities = q
                                                                isExtractingQuality = false
                                                            }
                                                        } else {
                                                            extractingEmbedUrl = watchUrl
                                                        }
                                                    }
                                                } else {
                                                    com.example.ui.screens.player.ServerStateStore.extractedQualities = emptyList() // clear so we fetch fresh
                                                    onPlay(watchUrl, server, currentSiteName)
                                                }
                                            }
                                            .padding(12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Box(
                                            modifier = Modifier.size(32.dp).background(MaterialTheme.colorScheme.primary.copy(alpha=0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                        }
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(server, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                        Spacer(modifier = Modifier.weight(1f))
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                                    }
                                }
                                item {
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
                            if (isExtractingQuality) {
                                Box(modifier = Modifier.fillMaxWidth().height(150.dp), contentAlignment = Alignment.Center) {
                                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                LazyColumn(
                                    modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                                    verticalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    items(extractedQualities) { quality ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(RoundedCornerShape(16.dp))
                                                .background(Color(0xFF16161A))
                                                .border(1.dp, Color(0xFF222225), RoundedCornerShape(16.dp))
                                                .clickable {
                                                    onPlay(quality.url, if (isDownloadMode) quality.name else (selectedServerForQuality ?: ""), currentSiteName)
                                                }
                                                .padding(12.dp),
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Box(
                                                modifier = Modifier.size(32.dp).background(Color(0x15FFFFFF), CircleShape),
                                                contentAlignment = Alignment.Center
                                            ) {
                                                Icon(Icons.Filled.PlayArrow, contentDescription = null, tint = Color.White, modifier = Modifier.size(16.dp))
                                            }
                                            Spacer(modifier = Modifier.width(16.dp))
                                            Text(quality.name, color = Color.White, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
                                            Spacer(modifier = Modifier.weight(1f))
                                                
                                            val badgeColor = when {
                                                quality.name.contains("1080") || quality.name.contains("FHD") -> Color(0xFFE91E63)
                                                quality.name.contains("720") || quality.name.contains("HD") -> Color(0xFF9C27B0)
                                                else -> Color(0xFF607D8B)
                                            }
                                            val badgeText = when {
                                                quality.name.contains("1080") || quality.name.contains("FHD") -> "FHD"
                                                quality.name.contains("720") || quality.name.contains("HD") -> "HD"
                                                else -> "SD"
                                            }
                                            Box(
                                                modifier = Modifier.background(badgeColor.copy(alpha=0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 8.dp, vertical = 4.dp)
                                            ) {
                                                Text(badgeText, color = badgeColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }
                                    item {
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
                }
            }
        }
        
"""

# Let's count braces in replacement:
# } else if {  [opens 1]
#   LazyColumn { [opens 2]
#     items { [opens 3]
#       Row { [opens 4]
#         clickable { [opens 5]
#           if { [opens 6]
#             if { [opens 7]
#             } else { [closes 7, opens 7]
#               if { [opens 8]
#                 coroutineScope { [opens 9]
#                 } [closes 9]
#               } else { [closes 8, opens 8]
#               } [closes 8]
#             } [closes 7]
#           } else { [closes 6, opens 6]
#           } [closes 6]
#         } [closes 5]
#         Box { [opens 5]
#         } [closes 5]
#       } [closes 4]
#     } [closes 3]
#     item { [opens 3]
#     } [closes 3]
#   } [closes 2]
# } else { [closes 1, opens 1]
#   if { [opens 2]
#     Box { [opens 3]
#     } [closes 3]
#   } else { [closes 2, opens 2]
#     LazyColumn { [opens 3]
#       items { [opens 4]
#         Row { [opens 5]
#           clickable { [opens 6]
#           } [closes 6]
#           Box { [opens 6]
#           } [closes 6]
#           Box { [opens 6]
#           } [closes 6]
#         } [closes 5]
#       } [closes 4]
#       item { [opens 4]
#         clickable { [opens 5]
#         } [closes 5]
#       } [closes 4]
#     } [closes 3]
#   } [closes 2]
# } [closes 1]
# } [closes ?]
# } [closes ?]
# } [closes ?]
# } [closes ?]
# 
# Wait, how many closing braces at the end?
# Looking at original code:
#                         } // else (selectedServerForQuality == null)
#                     } // if (!isHorizontal)
#                 } // Column
#             } // Box (content wrapper)
#         } // Dialog
# There are 4 closing braces needed!
# 
# In the original file BEFORE my Python messes:
#                             } // LazyColumn
#                         } else {
#                             if (isExtractingQuality) {
#                                 Box(...) {
#                                     CircularProgressIndicator(...)
#                                 }
#                             } else {
#                                 LazyColumn(...) {
#                                     items(...) { ... }
#                                 }
#                                 Spacer(...)
#                                 Text(...)
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#         
#         extractingEmbedUrl?.let { url ->

c_new = pattern.sub(replacement, c)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c_new)

