from model.entitygroup import SquareGroup

entity_group = SquareGroup(1, 1000, 1000, (0, 200, 0), 33, 33, 5)
entity_group.tick(1.01)
print(entity_group.can_spawn())
print(entity_group._time_period)
entities = entity_group.spawn()
print(entities)
