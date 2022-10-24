import six

value = 4.3
if isinstance(value, float):
    print("True")
else:
    print("False")


value = "Yes String"
if isinstance(value, six.string_types):
    print("True")
else:
    print("False")
