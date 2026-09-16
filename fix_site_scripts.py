import re
with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    c = f.read()

replacement = """                var targetId = "${targetServerId ?: ""}";
                var isMainSite = window.location.href.includes('topcinema') || window.location.href.includes('witanime') || window.location.href.includes('brstej') || window.location.href.includes('animeluxe') || window.location.href.includes('anime4up') || window.location.href.includes('animerco') || window.location.href.includes('almeshkah');
                if (targetId && !window._serverClicked && isMainSite) {
                    var clicked = false;
                    // Site specific click logic based on ID format
                    if (targetId.includes('|')) {
                        var parts = targetId.split('|');
                        if (parts.length === 4) { // det.animerco.org
                            var el = document.querySelector('a[data-post="'+parts[0]+'"][data-nume="'+parts[1]+'"]');
                            if (el) { el.click(); clicked = true; }
                        }
                    } else if (window.location.href.includes('topcinema') || window.location.href.includes('brstej')) {
                        var el = document.querySelector('[data-embed-id="'+targetId+'"]') || document.querySelector('[data-id="'+targetId+'"]');
                        if (el) { el.click(); clicked = true; }
                    } else if (targetId.startsWith('server_')) { // z1.almeshkah.net
                        var el = document.getElementById(targetId);
                        if (el) { el.click(); clicked = true; }
                    } else { // witanime.you and others
                        var el = document.querySelector('[data-server-id="'+targetId+'"]') || document.querySelector('[data-id="'+targetId+'"]') || document.querySelector('[data-embed-id="'+targetId+'"]');
                        if (el) { el.click(); clicked = true; }
                    }
                    if (clicked) {
                        window._serverClicked = true;
                        return; // Wait for iframe to load
                    }
                }
                
                // Watch for new iframes after click
                if (window._serverClicked || !targetId || !isMainSite) {"""

# Replace the old logic
pattern = re.compile(r'var targetId = "\$\{targetServerId \?: ""\}";\s*if \(targetId && !window\._serverClicked\) \{.*?\/\/ Watch for new iframes after click\s*if \(window\._serverClicked \|\| !targetId\) \{', re.DOTALL)
c = pattern.sub(replacement, c)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(c)
