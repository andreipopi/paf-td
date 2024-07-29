arg(a).
arg(b).
arg(c).
p(a,10000).
p(b,10000).
p(c,9000).
p(1,a,c,4000).
p(2,c,a,10000).
p(3,b,c,8000).
p(4,c,b,4000).
att(a,c).
att(c,a).
att(b,c).
att(c,b).

%P-EXTsem(S)
% S corresponding to an extension.
%:- not in(A), query(A).

% in the EXT problem, it is enough to get one answer per subgraph,
% so the fastest way is to get solutions only for the minimal S,
% i.e. requiring in(A) only if A in S (query(A)).
%in(A) :- query(A).

%P-ACCsem(a)
% for the ACC problem this is not enoough, because the above code fixes the extension
% but we want to check among all of them, if any includes the query(a).
{in(A)} :- arg(A), a(A).
:-not in(A), query(A).

%conflict-free
:- atck(A,B), in(A), in(B).
%def(A):- arg(A), arg(B), att(B, A), atck(B,A), in(B), not in(A).

%Skeptical acceptance
%:- query(A), in(A). %no solutions should be left, which means no solution was found where the query is not in.
% credolous acceptance
%:- query(A), not in(A). %remove all solutions where the query is not in: if a solution is left then that is enough for a YES answer.

% SUBGRAPHS 
{a(A)}:- arg(A).
{atck(A,B)}:- att(A,B).


:- arg(A), p(A,10000), not  a(A).
% no subgraphs such that only one part of an attack in
:- att(A,B), atck(A,B), not a(A).
:- att(A,B), atck(A,B), not a(B).
% no subraph such that both attack sides in, and attack with p=1 not in
:- att(A,B), p(ID, A,B, 10000), a(A), a(B), not atck(A,B).
 
okatck(A,B) :- att(A,B), a(A), a(B).


% sort available ARGS to be able to iteratively multiply
lower_than(X,Y):- X<Y, arg(X), arg(Y).
%item(1, lower_than(X,Y)) :- lower_than(X,Y).
nsucc(X,Z):- lower_than(X,Y), lower_than(Y,Z), arg(X), arg(Y), arg(Z).
notimsuc(X,Y) :- lower_than(X,Z), lower_than(Z,Y).
imsuc(X,Y):- lower_than(X,Y), not notimsuc(X,Y).
min(Y):- not lower_than(_,Y), arg(Y).
max(X):- not lower_than(X,_), arg(X).
multupto(P,X) :- min(X), p(X,P), arg(X), a(X). %contribution if in subgraph
multupto((10000-P),X) :- min(X), p(X,P), arg(X), not a(X). %contribution not in subgraph
%item(1, multupto(P,X)) :- multupto(P,X).
multupto((P/10000),X) :- multupto(Pprime,Y), arg(X), imsuc(Y,X), Pprime* N =P, p(X,N), a(X).
multupto((P/10000),X) :- multupto(Pprime,Y), arg(X), imsuc(Y,X), Pprime* (10000-N) =P, p(X,N), not a(X).


% sort available ATTs to be able to iteratively multiply
lt(X,Y):- X<Y, att(A,B), att(D,C), okatck(A,B), okatck(D,C), p(X,A,B,_), p(Y,D,C,_).
%item(1, lower_than(X,Y)) :- lower_than(X,Y).
nsuccatt(X,Z):- lt(X,Y), lt(Y,Z), p(X,A,B,_), p(Y,D,C,_),  p(Z,E,F,_), att(A,B), att(D,C), att(E,F), okatck(A,B),okatck(D,C), okatck(E,F).
notimsucatt(X,Y) :- lt(X,Z), lt(Z,Y).
imsucatt(X,Y):- lt(X,Y), not notimsucatt(X,Y).
minatt(Y):- not lt(_,Y), p(Y,A,B,_), att(A,B), okatck(A,B).
maxatt(X):- not lt(X,_), p(X,A,B,_), att(A,B), okatck(A,B).

multuptoatt(P,X) :- minatt(X), p(X,A,B,P), att(A,B), atck(A,B). %positive contribution. (only okatck hot considered, see lines above)
multuptoatt((10000-P),X) :- minatt(X), p(X,A,B,P), att(A,B), not atck(A,B).%negative contribution for attack.
%item(1, multupto(P,X)) :- multupto(P,X).
multuptoatt((P/10000),X) :- multuptoatt(Pprime,Y), att(A,B), imsucatt(Y,X), Pprime* N =P, p(X,A,B,N), atck(A,B).
multuptoatt((P/10000),X) :- multuptoatt(Pprime,Y), att(A,B), imsucatt(Y,X), Pprime* (10000-N) =P, p(X,A,B,N), not atck(A,B).

finalprobarg(P):-  multupto(P,X), max(X). 
finalprobatt(P):- multuptoatt(P,X), maxatt(X).


res((P*Pprime)/10000) :- finalprobarg(P), finalprobatt(Pprime).
res((10000*Pprime)/10000) :- not finalprobatt(_), finalprobarg(Pprime). %can happen that there was no attack contribution. 
%Maybe think if there are other cases?


#show a/1.
#show atck/2.
%#show finalprobarg/1.
%#show finalprobatt/1.
#show res/1.
#show in/1.
#show def/1.
%#show min/1.
%#show max/1.
%#show multupto/2.

