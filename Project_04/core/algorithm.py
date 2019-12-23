import time

inf = float('inf')


def alpha_beta_search(state):
    t = time.time()
    v = -inf
    v_act = None
    for action in state.actions():
        s = state.result(action)
        if s.r:
            m = max_value(s, -inf, inf, t)
            if m > v:
                v = m
                v_act = action
        else:
            m = min_value(s, -inf, inf, t)
            if m > v:
                v = m
                v_act = action
    print(v)
    return v_act


def max_value(state, a, b, start_time):
    if state.isTerminal() or time.time()-start_time >= 5:
        return state.utility()
    v = -inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = max(v, max_value(s, a, b, start_time))
        else:
            v = max(v, min_value(s, a, b, start_time))
        a = max(a, v)
        if a >= b:
            return v
    return v


def min_value(state, a, b, start_time):
    if state.isTerminal() or time.time()-start_time >= 5:
        return state.utility()
    v = inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = min(v, min_value(s, a, b, start_time))
        else:
            v = min(v, max_value(s, a, b, start_time))
        b = min(b, v)
        if b <= a:
            return v
    return v
