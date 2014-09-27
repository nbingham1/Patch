from rhine import *
import timeit
from rhine_reader import *


rhines = rhineGenerate('Rhine.txt')

tic = timeit.default_timer()
print rhines[1].distance('Democrat', 'Republican')
print rhines[2].distance('Hello', 'Goodbye')
print rhines[3].distance('Hello', 'Kitty')
print rhines[4].distance('Hello', 'Darkness')
print rhines[0].distance('Hello', 'Puppy')
toc = timeit.default_timer()


print toc-tic


