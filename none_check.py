from typing import Union

# # sample.py
a: int
a = None  # mypy では error になる

b: Union[int, None]
b = None
