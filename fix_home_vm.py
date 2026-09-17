import re

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    content = f.read()

# We will replace loadData() completely.
load_data_pattern = r'fun loadData\(\)\s*\{[\s\S]*?\}\s*\}'
# Actually wait, `loadData()` ends with `} \n } \n }`. We have to parse it carefully or just replace the whole body of the class.
