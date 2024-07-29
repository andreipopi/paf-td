arg(a).
arg(b).
arg(c).

%p(a,9800).
%p(b,10000).
%p(c,9000).

%we need ids for the attacks in the iterative multiplication, in the D-FLAT/Clingo approach.
%p(1,a,c,4000).
%p(2,c,a,10000).
%p(3,b,c,8000).
%p(4,c,b,4000).

p(a,1).
p(b,1).
p(c,0.9).

%we need ids for the attacks in the iterative multiplication, in the D-FLAT/Clingo approach.
p(1,a,c,0.4).
p(2,c,a,1).
p(3,b,c,0.8).
p(4,c,b,0.4).

att(a,c).
att(c,a).
att(b,c).
att(c,b).
%att(e,f).

%att(a,b).
%p(7,a,b,0.3).
arg(d).
p(d,0.2).
arg(e).
p(e,0.2).
%p(5,e,f,0.1).
%att(b,e).
%p(6,b,e,1).

%arg(e).
%arg(f).
%arg(g).
%p(e,0.2).
%p(f,1).
%%p(5,e,f,1).
%p(g,1).

query(c).