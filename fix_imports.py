with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "r") as f:
    content = f.read()

# move imports after package
lines = content.split('\n')
pkg_line = -1
for i, line in enumerate(lines):
    if line.startswith("package "):
        pkg_line = i
        break

if pkg_line > 0:
    pkg = lines[pkg_line]
    lines.pop(pkg_line)
    lines.insert(0, pkg)
    
with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "w") as f:
    f.write('\n'.join(lines))

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "r") as f:
    content = f.read()

lines = content.split('\n')
pkg_line = -1
for i, line in enumerate(lines):
    if line.startswith("package "):
        pkg_line = i
        break

if pkg_line > 0:
    pkg = lines[pkg_line]
    lines.pop(pkg_line)
    lines.insert(0, pkg)

with open("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt", "w") as f:
    f.write('\n'.join(lines))
