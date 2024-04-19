travel(X, Y, P, [Y|P], L, Traffic) :-
    road(X, Y, L, T),
    Traffic is T.

travel(X, Y, Visited, Path, Length, Traffic) :-
    road(X, Z, L, T),
    Z \== Y,
    \+ member(Z, Visited),
    travel(Z, Y, [Z|Visited], Path, L1, T1),
    Length is L + L1,
    Traffic is T + T1.

find_path(X, Y, Path, Length, Traffic) :-
    travel(X, Y, [X], Q, Length, Traffic),
    reverse(Q, Path).
    
shortest_path(X, Y, Path, Length, Traffic) :-
    setof([T, P, L], find_path(X, Y, P, L, T), Paths),
    Paths = [[Traffic, Path, Length]|_].

