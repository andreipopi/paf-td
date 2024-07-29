arg(a).
arg(b).
arg(c).

p(a,10000).
p(b,10000).
p(c,9000).

%we need ids for the attacks in the iterative multiplication.
p(1,a,c,4000).
p(2,c,a,10000).
p(3,b,c,8000).
p(4,c,b,4000).

att(a,c).
att(c,a).
att(b,c).
att(c,b).

extension(b).
query(c).