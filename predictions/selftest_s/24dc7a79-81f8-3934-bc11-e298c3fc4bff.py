import cadquery as cq

outer_length = 80.0
outer_width = 40.0
bracket_thickness = 4.0
central_hole_diameter = 20.0
central_hole_depth = 3.0
pocket_length = 30.0
pocket_width = 20.0
pocket_depth = 2.0
pocket_fillet_radius = 2.0
mount_hole_spacing = 60.0
mount_hole_offset_y = 10.0
mount_hole_diameter = 5.0
mount_cbore_diameter = 8.0
mount_cbore_depth = 2.0
rib_thickness = 2.0
rib_height = 6.0
rib_width = 6.0
rib_length = 30.0
gusset_thickness = 2.0

result = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(bracket_thickness)
)
mount_points = [(-mount_hole_spacing/2, mount_hole_offset_y), (mount_hole_spacing/2, mount_hole_offset_y)]
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(mount_points)
    .cboreHole(mount_hole_diameter, mount_cbore_diameter, mount_cbore_depth)
)
result = (
    result.faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter/2)
    .cutBlind(central_hole_depth)
)
result = (
    result.faces('>Z')
    .workplane()
    .sketch()
    .rect(pocket_length, pocket_width)
    .edges()
    .fillet(pocket_fillet_radius)
    .finalize()
    .cutBlind(pocket_depth)
)
rib_offsets = [-outer_length/4, outer_length/4]
for x_off in rib_offsets:
    result = (
        result.faces('<Z')
        .workplane()
        .center(x_off, 0)
        .rect(rib_width, rib_length)
        .extrude(-rib_height)
    )
for direction in ['>X', '<X']:
    result = (
        result.faces(direction)
        .workplane(centerOption='CenterOfBoundBox')
        .polyline([
            (0, 0),
            (0, outer_width/2),
            (gusset_thickness, 0)
        ])
        .close()
        .extrude(bracket_thickness)
    )
