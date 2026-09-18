import cadquery as cq

block_length = 80.0
block_width = 80.0
block_thickness = 15.0
recess_diameter = 30.0
recess_depth = 10.0
rib_outer_diameter = 40.0
rib_inner_diameter = 30.0
rib_height = 5.0
hole_diameter = 5.0
hole_circle_radius = 30.0
hole_count = 12
fillet_radius = 3.0
chamfer_size = 0.5

result = (
    cq.Workplane('XY')
    .box(block_length, block_width, block_thickness)
    .faces('>Z').workplane()
    .circle(recess_diameter / 2).cutBlind(-recess_depth)
    .faces('>Z').workplane()
    .circle(rib_outer_diameter / 2).extrude(rib_height)
    .faces('>Z').workplane()
    .circle(rib_inner_diameter / 2).cutBlind(-rib_height)
    .faces('>Z').workplane()
    .polarArray(hole_circle_radius, 0, 360, hole_count).hole(hole_diameter)
    .edges('|Z').fillet(fillet_radius)
    .faces('>Z').chamfer(chamfer_size)
)
