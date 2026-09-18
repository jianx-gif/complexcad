import cadquery as cq
# create a solid with a hole then shell
solid = cq.Workplane('XY').box(30,30,30).faces('>Z').hole(10)
result = solid.shell(-2)
