// -*- coding: utf-8 -*-
// @Author : 艾登科技
// @Email : aidencaptcha@gmail.com
// @Address : https://github.com/aidencaptcha

function R() {
    for (var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 16, e = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ", n = "", i = 0; i < t; i++)
        n += e.charAt(Math.floor(Math.random() * e.length));
    return n
}

function e(t) {
    t = t.replace(/\r\n/g, "\n");
    for (var e = "", n = 0; n < t.length; n++) {
        var i = t.charCodeAt(n);
        i < 128 ? e += String.fromCharCode(i) : i > 127 && i < 2048 ? (e += String.fromCharCode(i >> 6 | 192),
        e += String.fromCharCode(63 & i | 128)) : (e += String.fromCharCode(i >> 12 | 224),
        e += String.fromCharCode(i >> 6 & 63 | 128),
        e += String.fromCharCode(63 & i | 128))
    }
    return e
}

function r_encode(n) {
    var t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    if (n) {
        var i, r, o, a, s, c, l, u = "", h = 0;
        for (n = e(n); h < n.length; )
            a = (i = n.charCodeAt(h++)) >> 2,
            s = (3 & i) << 4 | (r = n.charCodeAt(h++)) >> 4,
            c = (15 & r) << 2 | (o = n.charCodeAt(h++)) >> 6,
            l = 63 & o,
            isNaN(r) ? c = l = 64 : isNaN(o) && (l = 64),
            u = u + t.charAt(a) + t.charAt(s) + t.charAt(c) + t.charAt(l);
        return u
    }
}


function o(t) {
    var e, n = ["after_mobile", "mobile", "password", "old_password", "after_email", "email", "username"];
    for (var o in t)
        n.includes(o) && (t[o] = (e = t[o],
        R(6) + r_encode(e)));
    return t
}


function get_username(t) {
    var new_t = o(t);
    return new_t
}

