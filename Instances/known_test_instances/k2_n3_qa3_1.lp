arg(a).
arg(b).
arg(c).
arg(d).
arg(e).
arg(f).

p(e,0.8).
p(b,0.6).
p(d,0.7).
p(a,0.4).
p(c,1).
p(f,1).

att(a,d).
att(d,c).
att(a,f).

p(1,a,d,1).
p(2,d,c,0.2).
p(3,a,f,0.6).

query(f).