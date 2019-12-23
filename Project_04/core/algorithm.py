inf = float('inf')


def alpha_beta_search(state):
    m = max(
        state.actions(),
        key=lambda action: max_value(state.result(action), a=-inf, b=inf)
    )
    return m


def max_value(state, a, b):
    if state.isTerminal():
        return state.utility()
    v = -inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = max(v, max_value(s, a, b))
        else:
            v = max(v, min_value(s, a, b))
        if v >= b:
            return v
        a = max(a, v)
    return v


def min_value(state, a, b):
    if state.isTerminal():
        return state.utility()
    v = inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = max(v, min_value(s, a, b))
        else:
            v = max(v, max_value(s, a, b))
        if v >= a:
            return v
        b = max(b, v)
    return v
