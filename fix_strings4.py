with open('app/src/main/res/values/strings.xml', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "name=\"movies\"" in line or "name=\"series\"" in line or "name=\"anime\"" in line or "name=\"about\"" in line or "name=\"extensions\"" in line or "name=\"share\"" in line or "name=\"social\"" in line or "name=\"login\"" in line or "name=\"logout\"" in line or "name=\"logout_confirm\"" in line or "name=\"library\"" in line or "name=\"about_app\"" in line or "name=\"help_support\"" in line:
        continue
    new_lines.append(line)

with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.writelines(new_lines)
print("Removed duplicates!")
