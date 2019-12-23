inf = float('inf')


def alpha_beta_search(state):
    m = max(
        state.actions(),
        key=lambda action: max_value(
            state.result(action), a=-inf, b=inf, depth=2)
    )
    return m


def max_value(state, a, b, depth):
    if state.isTerminal() or depth == 0:
        return state.utility()
    v = -inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = max(v, max_value(s, a, b, depth-1))
        else:
            v = max(v, min_value(s, a, b, depth-1))
        if v >= b:
            return v
        a = max(a, v)
    return v


def min_value(state, a, b, depth):
    if state.isTerminal() or depth == 0:
        return state.utility()
    v = inf
    for action in state.actions():
        s = state.result(action)
        if s.r:
            v = min(v, min_value(s, a, b, depth-1))
        else:
            v = min(v, max_value(s, a, b, depth-1))
        if v <= a:
            return v
        b = min(b, v)
    return v
