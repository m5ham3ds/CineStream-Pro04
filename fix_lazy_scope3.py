import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# I need to add a `}` before the `item {` that I broke.

# Fix 1: Servers list
target1 = """                                        Spacer(modifier = Modifier.weight(1f))
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                                    }
                                }
                                item {"""
replace1 = """                                        Spacer(modifier = Modifier.weight(1f))
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                                    }
                                }
                                }
                                item {"""
c = c.replace(target1, replace1)

# Fix 2: Quality list
target2 = """                                                Text(badgeText, color = badgeColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }
                                    item {"""
replace2 = """                                                Text(badgeText, color = badgeColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    }
                                }
                                item {"""
c = c.replace(target2, replace2)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

