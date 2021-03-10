'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readline() {
    return inputString[currentLine++];
}

function main() {
    var n = parseInt(readline())
    var spf = Array(n)
    for (var i = 2; i < n; i++) {
        var p = true;
        for (var j = 2; j < i; j++)
            if (i % j == 0)
                p = false;
        if (p)
            console.log(i);
    }
}