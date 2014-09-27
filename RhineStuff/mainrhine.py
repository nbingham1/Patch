from rhine import *
import timeit
from rhine_reader import *

rb = RhineBundle()

rb.rhineGenerate('Rhine.txt')


tic = timeit.default_timer()

dist = []

for i in xrange(500):
    dist.append(rb.freshRhine().distance('hello', 'kitty'))


toc = timeit.default_timer()


print toc-tic


