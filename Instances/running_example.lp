arg(a).
arg(d).
p(a,0.8).
p(d,1).
arg(g).
p(g,1).

att(a,d).
att(d,a).
att(g,d).
att(d,g).

p(1,a,d,1).
p(2,d,a,1).
p(9,g,d,0.3).
p(10,d,g,0.5).



query(g).

