from rhine import *
import timeit
from rhine_reader import *

rb = RhineBundle()

rb.rhineGenerate('/var/www/patch/Rhine.txt')


tic = timeit.default_timer()

dist = []

for i in xrange(500):
    dist.append(rb.freshRhine().distance('hello', 'kitty'))


toc = timeit.default_timer()


print toc-tic


