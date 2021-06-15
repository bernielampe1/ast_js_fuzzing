function f(n) {
    var s = 0;
    if(n == 0) return(s);
    if(n == 1) { s += 1; return(s); }
    else { return(f(n - 1) + f(n - 2)); }
}

print(f(10));

