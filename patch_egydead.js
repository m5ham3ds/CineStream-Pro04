const fs = require('fs');
const file = 'app/src/main/java/com/example/extensions/EgyDeadExtension.kt';
let code = fs.readFileSync(file, 'utf8');

code = code.replace(
    /if \(typeof AndroidBridge !== 'undefined' && serverItems\.length > 0\) \{/g,
    `if (typeof AndroidBridge !== 'undefined' && serverItems.length > 0) {
                                AndroidBridge.logDebug('Found ' + serverItems.length + ' servers');`
);

code = code.replace(
    /\} else if \(serverItems\.length === 0 && typeof AndroidBridge !== 'undefined'\) \{/g,
    `} else if (serverItems.length === 0 && typeof AndroidBridge !== 'undefined') {
                                AndroidBridge.logDebug('No servers found in retry loop');`
);

code = code.replace(
    /if \(serverItems\.length === 0 && typeof AndroidBridge !== 'undefined'\) \{/g,
    `if (serverItems.length === 0 && typeof AndroidBridge !== 'undefined') {
                            AndroidBridge.logDebug('Timeout reached, sending failed');`
);

fs.writeFileSync(file, code);
