arg(a).
arg(b).
arg(c).
arg(d).
p(a,0.8).
p(b,1).
p(c,0.9).
p(d,1).
arg(e).
p(e,1).

att(a,d).
att(d,a).
att(b,c).
att(c,b).
att(a,b).
att(b,a).
att(c,d).
att(d,c).
att(e,d).
att(d,e).

p(1,a,d,1).
p(2,d,a,1).
p(3,a,b,0.7).
p(4,b,a,1).
p(5,b,c,1).
p(6,c,b,1).
p(7,d,c,1).
p(8,c,d,1).
p(9,e,d,0.3).
p(10,d,e,0.5).


%p(7,b,d,0.3).
%p(8,d,b,0.6).



extension(a).
extension(c).
extension(e).