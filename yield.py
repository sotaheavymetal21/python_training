def generator1():
    yield "one"


def generator2():
    yield "two"


def generator(g1, g2):
    yield from g1
    yield from g2


gen = generator(generator1(), generator2())

for x in gen:
    print(x)
