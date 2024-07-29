



{in(A)} :- arg(A).
{out(A)} :- arg(A).
% no guess for undecided

:- in(A), out(A). % not in and out at the same time

defeated(A) :- arg(A), att(B,A), p(_, B,A,1), p(B,1), in(B). % for sure defeated if attacked by an in with prob 1
not_defeated(A) :- arg(A), att(B,A), 1 {not p(_, B,A,1) ;not p(B,1)}, in(B). % "complement" of above
:- defeated(A), not out(A).
:- out(A), not defeated(A).
:- not_defeated(A), out(A).
:- defeated(A), in(A).


attacked(A) :- arg(A), att(B,A), arg(B). 
in_for_sure(A) :-  arg(A), not attacked(A). % must be in if attacked by nothing.
:- in_for_sure(A), not in(A).


%attacked_by_sure_in(A) :-  in(B), arg(A), att(B,A), arg(B), p(B,1), p(_, B,A,1).
%:- attacked_by_sure_in(A), not out(A).


attacked_by_not_out(A) :- not out(B), att(B,A), arg(A), arg(B).

attacked_by_out_only(A) :- not attacked_by_not_out(A), arg(A).
:- not in(A), attacked_by_out_only(A).
:-  in(A), not attacked_by_out_only(A).

%:- not out(C), att(A,C), p(A,1), p(ID,A,C,1).

%out(A) :- 
%out(A) :- arg(A), att(B,A), in(B), p(ID, P), P=1, Pa=1, p(B,Pa).



#show in/1.
#show out/1.
%#show defeated/1.
%#show not_defeated/1.
%#show in_for_sure/1.
%#show attacked/1.  
%#show attacked_by_out_only/1.