arg(0).
arg(1).
arg(2).
arg(3).


p(0,1).
p(1,1).
p(2,1).
p(3,1).


%we need ids for the attacks in the iterative multiplication.
p(1,0,1,1).
p(2,1,0,1).
p(3,1,2,1).
p(4,2,3,1).
p(5,0,2,1).


att(0,1).
att(1,0).
att(1,2).

att(2,3).
att(0,2).

query(1).



extension(3).
extension(0).