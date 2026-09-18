import cadquery as cq
knob_head_radius = 20.0
knob_head_height = 12.0
central_hole_diameter = 8.0
central_hole_radius = 15.0
central_hole_count = 6
central_hole_radius = central_hole_diameter / 2.0
mounting_hole_radius = 2.0
mounting_hole_circle_radius = 15.0
mounting_hole_count = 4
mounting_hole_radius = 15.0
slot_radial_offset = 10.0
chamfer_depth = 1.0
base = (
    cq.Workplane("XY")
    .circle(knob_head_radius)
    .extrude(knob_head_height)
)
base = base.edges().chamfer(chamfer_depth)
base = base.edges().fillet(central_hole_radius)
base = (
    base.faces(">Z")
    .workplane()
    .hole(central_hole_radius * 2)
)
base = base.faces(">Z").edges().chamfer(chamfer_depth)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=mounting_hole_radius, startAngle=0, angle=360, count=mounting_hole_count)
    .hole(mounting_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-mounting_hole_count/2, 0), (mounting_hole_radius, 0)])
    .hole(mounting_hole_diameter)
)
base = base.edges().chamfer(chamfer_depth)
result = base
