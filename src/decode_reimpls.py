def stage1_decode1(data, consts):
    """Reimplementation of the stage1_decode1 function in python, with dynamic constants"""

    """
        function Onn(d) {
            var w = 1019633;
            var c = d.length;
            var t = [];
            for (var n = 0; n < c; n++) {
                t[n] = d.charAt(n)
            };
            for (var n = 0; n < c; n++) {
                var e = w * (n + 82) + (w % 49761);
                var b = w * (n + 575) + (w % 41455);
                var g = e % c;
                var p = b % c;
                var o = t[g];
                t[g] = t[p];
                t[p] = o;
                w = (e + b) % 1671836;
            };
            return t.join('')
        };
    """
    w = consts[0]
    c = len(data)
    t = []
    for n in range(c):
        t.append(data[n])
    
    for n in range(c):
        e = w * (n + consts[3]) + (w % consts[4])
        b = w * (n + consts[5]) + (w % consts[6])
        g = e % c
        p = b % c
        o = t[g]
        t[g] = t[p]
        t[p] = o
        w = (e+b) % consts[7]

    return ''.join(t)


def stage1_decode2(data, consts):
    """Reimplmentation of the stage1_decode2 function in python, with dynamic constants"""

    """
    function foo() {
        var a = 10,
            o = 71,
            f = 44;
        var r = "abcdefghijklmnopqrstuvwxyz";
        var n = [88, 70, 65, 80, 85, 89, 71, 82, 79, 75, 76, 66, 74, 60, 90, 94, 81, 87, 86, 72];
        var q = [];
        for (var j = 0; j < n.length; j++) q[n[j]] = j + 1;
        var v = [];
        a += 23;
        o += 22;
        f += 52;
        for (var p = 0; p < arguments.length; p++) {
            var h = arguments[p].split(" ");
            for (var w = h.length - 1; w >= 0; w--) {
                var x = null;
                var b = h[w];
                var u = null;
                var y = 0;
                var l = b.length;
                var t;
                for (var z = 0; z < l; z++) {
                    var m = b.charCodeAt(z);
                    var e = q[m];
                    if (e) {
                        x = (e - 1) * o + b.charCodeAt(z + 1) - a;
                        t = z;
                        z++;
                    } else if (m == f) {
                        x = o * (n.length - a + b.charCodeAt(z + 1)) + b.charCodeAt(z + 2) - a;
                        t = z;
                        z += 2;
                    } else {
                        continue;
                    }
                    if (u == null) u = [];
                    if (t > y) u.push(b.substring(y, t));
                    u.push(h[x + 1]);
                    y = z + 1;
                }
                if (u != null) {
                    if (y < l) u.push(b.substring(y));
                    h[w] = u.join("");
                }
            }
            v.push(h[0]);
        }
        var s = v.join("");
        var i = [92, 39, 32, 10, 96, 42].concat(n);
        var k = String.fromCharCode(46);
        for (var j = 0; j < i.length; j++) s = s.split(k + r.charAt(j)).join(String.fromCharCode(i[j]));
        return s.split(k + "!").join(k);
    }
    """
    # [10, 71, 44, 88, 70, 65, 80, 85, 89, 71, 82, 79, 75, 76, 66, 74, 60, 90, 94, 81, 87, 86, 72, 0, 1, 23, 22, 52, 0, 1, 0, 0, 0, 1, 1, 1, 2, 2, 1, 1, 0, 92, 39, 32, 10, 96, 42, 46, 0]
    

    # var a = 10,
    #     o = 71,
    #     f = 44;
    # var r = "abcdefghijklmnopqrstuvwxyz";
    # var n = [88, 70, 65, 80, 85, 89, 71, 82, 79, 75, 76, 66, 74, 60, 90, 94, 81, 87, 86, 72];
    a = consts[0]
    o = consts[1]
    f = consts[2]
    r = "abcdefghijklmnopqrstuvwxyz"
    n = consts[3:23]
    # var q = [];
    # for (var j = 0; j < n.length; j++) q[n[j]] = j + 1;
    
    q = [0] * 256 # Not `q = [0] * (max(n)+1)` ???
    for j in range(len(n)):
        q[n[j]] = j + 1

    # var v = [];
    # a += 23;
    # o += 22;
    # f += 52;
    v = []
    a += consts[25]
    o += consts[26]
    f += consts[27]

    # Assume single argument in python reimplementation
    arguments = [data]
    
    #for (var p = 0; p < arguments.length; p++) {
    for p in range(len(arguments)):
        # var h = arguments[p].split(" ");
        h = arguments[p].split(" ")
        
        #for (var w = h.length - 1; w >= 0; w--) {
        # Suspect...
        for w in range(len(h) - 1, -1, -1):
            # var x = null;
            # var b = h[w];
            # var u = null;
            # var y = 0;
            # var l = b.length;
            # var t;
            x = None
            b = h[w]
            u = None
            y = 0
            l = len(b)
            t = None #?

            #for (var z = 0; z < l; z++) {
            z = 0;
            while z < l:
                # var m = b.charCodeAt(z);
                # var e = q[m];
                m = ord(b[z])
                e = q[m]

                # if (e) {
                #     x = (e - 1) * o + b.charCodeAt(z + 1) - a;
                #     t = z;
                #     z++;
                # } else if (m == f) {
                #     x = o * (n.length - a + b.charCodeAt(z + 1)) + b.charCodeAt(z + 2) - a;
                #     t = z;
                #     z += 2;
                # } else {
                #     continue;
                # }
                if e:
                    x = (e - 1) * o + ord(b[z+1]) - a
                    t = z
                    z += 1
                elif m == f:
                    x = o * (len(n) - a + ord(b[z+1])) + ord(b[z+2]) - a
                    t = z
                    z += 2
                else:
                    # To behave like a C for loop on continue.
                    z += 1
                    continue

                # if (u == null) u = [];
                if u is None:
                    u = []

                # if (t > y) u.push(b.substring(y, t));
                if t > y:
                    u.append(b[y:t])

                
                #u.push(h[x + 1]);
                u.append(h[x+1])

                #y = z + 1;
                y = z + 1

                # To behave like a C for loop
                z += 1
            
            # if (u != null) {
            #     if (y < l) u.push(b.substring(y));
            #     h[w] = u.join("");
            # }
            if u is not None:
                if y < l:
                    u.append(b[y:])
                h[w] = ''.join(u)
        
        # v.push(h[0]);
        v.append(h[0])
    
    # var s = v.join("");
    s = "".join(v)
    # var i = [92, 39, 32, 10, 96, 42].concat(n);
    i = consts[41:47]
    i.extend(n)

    # var k = String.fromCharCode(46);
    k = chr(46)
    # for (var j = 0; j < i.length; j++) s = s.split(k + r.charAt(j)).join(String.fromCharCode(i[j]));
    for j in range(len(i)):
        s = s.replace(k + r[j], chr(i[j]))
    # return s.split(k + "!").join(k);
    return s.replace(k + "!", k)

def stage2_decode_identifiers(data, key, consts):
    """Reimplmentation of the stage2_decode_identifiers function in python, with dynamic constants"""

    """
    function _$af401859(data, key) {
        var o = data.length;
        var w = [];
        for (var r = 0; r < o; r++) {
            w[r] = data.charAt(r)
        };
        for (var r = 0; r < o; r++) {
            var u = key * (r + 82) + (key % 49761);
            var n = key * (r + 575) + (key % 41455);
            var c = u % o;
            var t = n % o;
            var v = w[c];
            w[c] = w[t];
            w[t] = v;
            key = (u + n) % 1671836
        };
        var h = String.fromCharCode(127);
        var y = '';
        var q = '%';
        var b = '#1';
        var z = '%';
        var m = '#0';
        var k = '#';
        return w.join(y).split(q).join(h).split(b).join(z).split(m).join(k).split(h)
    }
    """
    o = len(data)
    w = []
    for r in range(o):
        w.append(data[r])
    
    for r in range(o):
        u = key * (r + consts[2]) + (key % consts[3])
        n = key * (r + consts[4]) + (key % consts[5])
        c = u % o
        t = n % o
        v = w[c]
        w[c] = w[t]
        w[t] = v
        key = (u + n) % consts[6]

    h = chr(127)
    y = ''
    q = '%'
    b = '#1'
    z = '%'
    m = '#0'
    k = '#'
    return y.join(w).replace(q, h).replace(b, z).replace(m, k).split(h)