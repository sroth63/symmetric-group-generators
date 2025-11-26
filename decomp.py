def decomp_cycles(p):
    n = len(p)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if not visited[i] and p[i] != i:
            cycle = [i]
            visited[i] = True
            j = p[i]
            while j != i:
                visited[j] = True
                cycle.append(j)
                j = p[j]
            cycles.append(cycle)
    return cycles


def decomp_transpos(p):
    cycles = decomp_cycles(p)
    transpos = []
    for cycle in cycles:
        if 0 in cycle:
            while cycle[0] != 0:
                cycle = cycle[1:] + cycle[0]
            for a in cycle[1:]:
                transpos.append([0, a])
        else:
            for a in cycle:
                transpos.append([0, a])
            transpos.append([0, cycle[0]])
    return transpos


def decomp_adjacent_transpos(p):
    transpos = decomp_transpos(p)
    adjacent_transpos = []
    for transpo in transpos:
        for i in range(transpo[1]):
            adjacent_transpos.append([i, i + 1])
        for i in range(transpo[1] - 2, -1, -1):
            adjacent_transpos.append([i, i + 1])

    # cleaning phase: removing identical transpositions that are side by side in the list
    cleaning = True
    while cleaning:
        cleaning = False
        i = 0
        while i < len(adjacent_transpos) - 1:
            if adjacent_transpos[i] == adjacent_transpos[i + 1]:
                cleaning = True
                del adjacent_transpos[i : i + 2]
            i += 1

    return adjacent_transpos


def decomp_ct(p):
    n = len(p)
    adjacent_transpos = decomp_adjacent_transpos(p)
    ct = []
    for adjacent_transpo in adjacent_transpos:
        if ct == []:
            ct = [(-adjacent_transpo[0]) % n, "t", adjacent_transpo[0]]
        else:
            ct[-1] = (ct[-1] - adjacent_transpo[0]) % n
            ct = ct + ["t", adjacent_transpo[0]]

    # cleaning phase
    cleaning = True
    while cleaning:
        cleaning = False
        i = 0
        while i < len(ct):
            if ct[i] == 0:
                cleaning = True
                if i == 0 or i == len(ct) - 1:
                    del ct[i]
                else:
                    del ct[i - 1 : i + 2]
            elif ct[i] != "t" and i + 1 < len(ct) and ct[i + 1] != "t":
                cleaning = True
                ct[i] = (ct[i] + ct[i + 1]) % n
                del ct[i + 1]
            i += 1

    return ct
