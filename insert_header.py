for filename in ["app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"]:
    with open(filename, "r") as f:
        content = f.read()

    target = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState) 
            // Leave space for bottom nav
    ) {"""
    
    if target not in content:
        target = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
               
    ) {"""
        if target not in content:
            target = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
    ) {"""

    replacement = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
    ) {
        com.example.ui.components.CineStreamHeader(
            onProfileClick = { },
            onSearchClick = { },
            onMenuClick = { }
        )"""

    content = content.replace(target, replacement)
    
    with open(filename, "w") as f:
        f.write(content)
