# -*- coding: utf-8 -*-
#2024.1.6 管理列表

cars=['bmw','audi','toyota','subaru']
cars.sort()
print(cars)

cars=['bmw','audi','toyota','subaru']
cars.sort(reverse=True)
print(cars)

print('\nhere is the sorted list')
print(sorted(cars))

print('\nhere is the original list again')
print(cars)

cars=['bmw','audi','toyato','subaru']
len(cars)
print(len(cars))

#homework
travel_places=['cq','sc','xj','xa','bj']
print(travel_places)
print(sorted(travel_places))
print(travel_places)
print(sorted(travel_places,reverse=True))

travel_places.reverse()
print(travel_places)
travel_places.reverse()
print(travel_places)
travel_places.sort()
print(travel_places)
travel_places.sort(reverse=True)
print(travel_places)

like=['game','longboard','book','sunny','miko','car']
print(like[0].title())
like.append(cars)
print(like)

new_like = like.pop()
print(new_like)
new_like = new_like[:2]
like[-1] = new_like
print(like)