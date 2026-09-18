import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
cavity_diameter = 30.0
cavity_depth = 6.0
cavity_clearance = 6.0
cavity_clearance = 5.0
screw_hole_diameter = 4.0
counterbore_diameter = 6.5
counterbore_depth = 3.0
screw_spacing = 10.0
fillet_radius = 2.0
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z").workplane()
    .center(0, 0)
    .circle(cavity_diameter / 2)
    .extrude(cavity_depth)
)
sketch = (
    base
    .faces(">Z").workplane()
    .center(0, 0)
    .rect(screw_hole_diameter, screw_spacing)
    .cutBlind(-cavity_depth)
)
sketch = (
    sketch
    .faces(">Z").workplane()
    .center(0, 0)
    .circle(cavity_clearance)
    .cutBlind(-cavity_depth)
)
result = (
    sketch
    .faces(">Z").workplane()
    .center(0, 0)
    .cboreHole(screw_hole_diameter, counterbore_diameter, counterbore_depth)
)
