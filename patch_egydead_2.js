const fs = require('fs');
const file = 'app/src/main/java/com/example/extensions/EgyDeadExtension.kt';
let code = fs.readFileSync(file, 'utf8');

code = code.replace(
    /function handleWatchPage\(\) \{/g,
    `function handleWatchPage() {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.logDebug('handleWatchPage called');`
);

code = code.replace(
    /function handleDetails\(\) \{/g,
    `function handleDetails() {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.logDebug('handleDetails called');`
);

code = code.replace(
    /function handleSearch\(\) \{/g,
    `function handleSearch() {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.logDebug('handleSearch called');`
);

fs.writeFileSync(file, code);
