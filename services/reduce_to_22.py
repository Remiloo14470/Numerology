

def reduce_to_22(n: int) -> int:
    while n > 22:
        n = sum(int(d) for d in str(n))
    return n