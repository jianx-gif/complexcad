import cadquery as cq

handle_length = 80.0
start_width = 30.0
start_height = 20.0
end_width = 15.0
end_height = 10.0
rib_width = 5.0
rib_height = 2.0
fillet_radius = 1.5
hole_diameter = 4.0
hole_spacing = 20.0

start_sketch = cq.Sketch().rect(start_width, start_height).circle(hole_diameter/2, mode='s')
end_sketch = cq.Sketch().rect(end_width, end_height).circle(hole_diameter/2, mode='s')

loft_body = (
    cq.Workplane("XY")
    .placeSketch(start_sketch, end_sketch.moved(cq.Location(cq.Vector(0, 0, handle_length))))
    .loft()
)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(handle_length)
)

result = loft_body.union(rib)

result = result.edges().fillet(fillet_radius)

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)
