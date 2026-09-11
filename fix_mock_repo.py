with open('app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt', 'r') as f:
    text = f.read()

new_methods = """
    override fun getUpcomingSeries(): Flow<List<Series>> = flow { emit(emptyList()) }
    override fun getUpcomingAnime(): Flow<List<Series>> = flow { emit(emptyList()) }
    override fun getNewReleasesAnime(): Flow<List<Series>> = flow { emit(emptyList()) }
"""

inject_point = "    override suspend fun searchMulti(query: String)"

if inject_point in text:
    text = text.replace(inject_point, new_methods + inject_point)
    with open('app/src/main/java/com/example/data/repository/MockMediaRepositoryImpl.kt', 'w') as f:
        f.write(text)
    print("Fixed MockMediaRepositoryImpl")
else:
    print("Not found in MockMediaRepositoryImpl")
