import cadquery as cq

# Parameters
hex_diameter = 80.0
block_thickness = 15.0
recess_diameter = 30.0
recess_depth = 5.0
mount_hole_diameter = 6.0
mount_hole_radius = mount_hole_diameter / 2
hole_pattern_offset = 10.0
hole_pattern_diameter = hex_diameter - 2 * hole_pattern_offset
cbore_radius = 2.5
cbore_outer_radius = 4.0
cbore_depth = 3.0
fillet_radius = 2.0
chamfer_size = 1.0
rib_width = 30.0
rib_thickness = 10.0
rib_height = 3.0

result = (
    cq.Workplane("XY")
    .polygon(6, hex_diameter)
    .extrude(block_thickness)
    .faces(">Z").workplane()
    .circle(recess_diameter / 2)
    .cutBlind(-recess_depth)
    .faces("<Z").workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .faces(">Z").workplane()
    .polygon(6, hole_pattern_diameter)
    .vertices()
    .cboreHole(mount_hole_radius, cbore_outer_radius, cbore_depth)
    .edges("|Z").fillet(fillet_radius)
    .faces(">Z").chamfer(chamfer_size)
)
