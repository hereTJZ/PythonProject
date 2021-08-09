var window = {};
function getBkn(e) {
for (t = 5381, n = 0, o = e.length; n < o; ++n) t += (t << 5) + e.charAt(n).charCodeAt();
return 2147483647 & t
}