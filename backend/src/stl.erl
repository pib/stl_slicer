-module(stl).

-ifdef(TEST).
-include_lib("eunit/include/eunit.hrl").
-endif.

-define(FL, float-little).

parse_bin_facet(<<_Normal/bytes:12,
                  P1x:4/FL, P1y:4/FL, P1z:4/FL,
                  P2x:4/FL, P2y:4/FL, P2z:4/FL,
                  P3x:4/FL, P3y:4/FL, P3z:4/FL,
                  Points/bytes:36, _AttrByteCount/bytes:2>>) ->
    [[P1x, P1y, P1z], [P2x, P2y, P2z], [P3x, P3y, P3z]].


%% Tests

-ifdef(TEST).

parse_bin_facet_test() ->
    [[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]] = 
        parse_bin_facet(<<0:12/bytes, 

-endif.
