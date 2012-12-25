-module(slicer_backend_app).

-behaviour(application).

-ifdef(TEST).
-include_lib("eunit/include/eunit.hrl").
-endif.

%% Application callbacks
-export([start/2, stop/1]).

%% ===================================================================
%% Application callbacks
%% ===================================================================

start(_StartType, _StartArgs) ->
    slicer_backend_sup:start_link().

stop(_State) ->
    ok.


%% Tests

-ifdef(TEST).

simple_test() ->
    ok = application:start(slicer_backend),
    ?assertNot(undefined == whereis(slicer_backend_sup)).

-endif.
