import time

inf = float('inf')


def alpha_beta_search(board):
    t = time.time()
    v = -inf
    v_act = None
    for action in board.actions():
        board.do_move(action)
        if board.turn == 'A':
            m = max_value(board, -inf, inf, depth=5, start_time=t)
            if m > v:
                v = m
                v_act = action
        else:
            m = min_value(board, -inf, inf, depth=5, start_time=t)
            if m > v:
                v = m
                v_act = action
        board.undo_move(action)
    print(f"{v} in {time.time()-t:.2f}")
    return v_act


def max_value(board, a, b, depth=inf, start_time=None):
    if start_time:
        if time.time()-start_time >= 10:
            #print("time reached", end='\r')
            return board.utility()
    if board.isTerminal() or depth == 0:
        return board.utility()
    v = -inf
    for action in board.actions():
        board.do_move(action)
        if board.turn == 'A':
            v = max(v, max_value(board, a, b, depth, start_time))
        else:
            v = max(v, min_value(board, a, b, depth-1, start_time))
        board.undo_move(action)
        if v >= b:
            return v
        a = max(a, v)
    return v


def min_value(board, a, b, depth=inf, start_time=None):
    if start_time:
        if time.time()-start_time >= 10:
            #print("time reached", end='\r')
            return board.utility()
    if board.isTerminal() or depth == 0:
        return board.utility()
    v = inf
    for action in board.actions():
        board.do_move(action)
        if board.turn == 'H':
            v = min(v, min_value(board, a, b, depth, start_time))
        else:
            v = min(v, max_value(board, a, b, depth-1, start_time))
        board.undo_move(action)
        if v <= a:
            return v
        b = min(b, v)
    return v
