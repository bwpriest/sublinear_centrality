"""test.py - demo of using a c++ class from within Python"""
from sen.hash import TwoUnivHash as Foo

# We'll create a Foo object with a value of 5...
f = Foo(5,2)

# Calling f.bar() will print a message including the value...
print('f=Foo(5,2)')
f.members()

# Now we'll use foobar to add a value to that stored in our Foo object, f
print("f.hash(22) = {}".format(f.hash(22)))

# Now we'll do the same thing - but this time demonstrate that it's a normal
# Python integer...

x = f.hash(2)
print("Type of x; where x = f.hash(2) is {}".format(type(x)))
