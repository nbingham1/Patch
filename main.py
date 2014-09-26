from rhine import *
import timeit


rhine = Rhine('5454cb1ff1324684a0293846cabf395c')       #nak54
rhine1 = Rhine('c3b8a2ee76034dd99f33cf30f108fa40')      #nicholasakramer@gmail

tic = timeit.default_timer()
print rhine.distance('Democrat', 'Republican')
print rhine1.distance('Hello', 'Goodbye')
print rhine.distance('Hello', 'Kitty')
print rhine1.distance('Hello', 'Darkness')
print rhine.distance('Hello', 'Puppy')


toc = timeit.default_timer()


print toc-tic


