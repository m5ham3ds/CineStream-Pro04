with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

import re
print("Functions in Repo:")
funcs = re.findall(r'override fun \w+', text)
for fn in funcs: print(fn)
