const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

var n;
rl.on('line', (input) => {
    n = parseInt(input);
    console.log(n)
});


var spf = Array(n)
for (var i = 2; i < n; i++)
    spf[i] = i
for (var i = 2; i < n; i++) {
    if (spf[i] < i)
        continue;
    for (var j = 2 * i; j < n; j += i)
        spf[j] = Math.min(spf[j], i)
    console.log(i)
}