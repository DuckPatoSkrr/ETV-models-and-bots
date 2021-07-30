
show_r(_,_,0,-1).
show_r(X,Y,P,_):-relacion(Y,X,P) | relacion(X,Y,P). %relacion directa
show_r(X,Y,PF,Cont):-NCont is Cont - 1,show_r(X,Z,P1,NCont),show_r(Y,Z,P2,NCont), puntuacion(PF,P1,P2). %relacion compleja

show_r(X,Y,P):-show_r(X,Y,P,2). %maximo numero de complejidad en relaciones

neutro(PF,P):-P > 0, PF is P -0.1, !. %perdida de relacion en complejidad
neutro(PF,PF).

puntuacion(PF,P1,P2):-P1 < P2, neutro(PF,P1),!.
puntuacion(PF,_,P2):- neutro(PF,P2),!.