from rhine import *
import timeit
from rhine_reader import *


rhines = rhineGenerate('Rhine.txt')

tic = timeit.default_timer()
print rhines[1].distance('President Barack Obama', 'Obama')
print rhines[1].distance('President', 'Obama')
print rhines[2].distance('is', 'was')
print rhines[3].distance('Hello', 'Kitty')
print rhines[4].distance('Hello', 'Darkness')
print rhines[0].distance('Hello', 'Puppy')
print rhines[7].closest_entities("Obama")
print rhines[8].synonym_check('President Barack Obama', 'Obama')
a = rhines[9].entity_extraction('Hello Bob')

print a

#for el in a:
#    print el

toc = timeit.default_timer()


print toc-tic


