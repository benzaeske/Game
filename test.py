import numpy


speed = 5

up = True
down = False
left = True
right = False

angle = numpy.arctan2(up - down, right - left)
x = round(numpy.cos(angle), 10) * speed
y = round(numpy.sin(angle), 10) * speed


print(angle)
print(x)
print(y)
