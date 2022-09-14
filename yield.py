def generator1():
    yield "one"


def generator2():
    yield "two"


def generator3():
    yield "three"


def generator100():
    yield "one hundred"


def generator(g1, g2, g3, g4):
    yield from g1
    yield from g2
    yield from g3
    yield from g4


gen = generator(generator1(), generator2(), generator3(), generator100())

for x in gen:
    print(x)
