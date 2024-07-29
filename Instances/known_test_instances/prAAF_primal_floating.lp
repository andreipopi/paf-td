arg(a).
arg(b).
arg(c).
arg(d).


p(a,1).
p(b,1).
p(c,1).
p(d,1).


%we need ids for the attacks in the iterative multiplication.
p(1,a,b,1).
p(2,b,a,1).
p(3,b,c,1).
p(4,c,d,1).
p(5,a,c,1).


att(a,b).
att(b,a).
att(b,c).

att(c,d).
att(a,c).
