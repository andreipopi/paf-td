

%...:- ....,out(a1), out(a2), ...
in(A) :- arg(A), out(B) : att(B,A). %list true if emtpy
%if not empty it makes a list of out(B), ou(B2), out(B3), if all of them true then it means A attacked only by out.

out(B) :- in(A), att(A,B), p(_, A,B,10000), p(A,10000).

% no guess for undecided


#show in/1.
#show out/1.
%#show defeated/1.
%#show not_defeated/1.
%#show in_for_sure/1.
%#show attacked/1.  
%#show attacked_by_out_only/1.