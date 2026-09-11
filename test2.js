const regex = /loadIframe\(this,\s*'([^']+)'\)/;
const text = "loadIframe(this, 'https://example.com/iframe')";
console.log(text.match(regex));
