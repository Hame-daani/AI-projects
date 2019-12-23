import time
from functools import lru_cache

inf = float('inf')


@lru_cache(maxsize=None)
def alpha_beta_search(state):
    t = time.time()
    v = -inf
    v_act = None
    state.evaluate()
    for action in range(len(state.actions)):
        s = state.results[action]
        if s.r:
            m = max_value(s, -inf, inf, start_time=0, depth=1)
            if m > v:
                v = m
                v_act = state.actions[action]
        else:
            m = min_value(s, -inf, inf, start_time=0, depth=1)
            if m > v:
                v = m
                v_act = state.actions[action]
    print(f"{v} in {time.time()-t:.2f}")
    return v_act


@lru_cache(maxsize=None)
def max_value(state, a, b, depth=inf, start_time=None):
    if start_time:
        if time.time()-start_time >= 20:
            #print("time reached", end='\r')
            return state.utility()
    if state.isTerminal() or depth == 0:
        return state.utility()
    v = -inf
    state.evaluate()
    for action in range(len(state.actions)):
        s = state.results[action]
        if s.r:
            v = max(v, max_value(s, a, b, depth, start_time))
        else:
            v = max(v, min_value(s, a, b, depth-1, start_time))
        a = max(a, v)
        if a >= b:
            return v
    return v


@lru_cache(maxsize=None)
def min_value(state, a, b, depth=inf, start_time=None):
    if start_time:
        if time.time()-start_time >= 20:
            #print("time reached", end='\r')
            return state.utility()
    if state.isTerminal() or depth == 0:
        return state.utility()
    v = inf
    state.evaluate()
    for action in range(len(state.actions)):
        s = state.results[action]
        if s.r:
            v = min(v, min_value(s, a, b, depth, start_time))
        else:
            v = min(v, max_value(s, a, b, depth-1, start_time))
        b = min(b, v)
        if b <= a:
            return v
    return v
