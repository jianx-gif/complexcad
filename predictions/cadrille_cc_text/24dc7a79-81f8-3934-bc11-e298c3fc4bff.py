import cadquery as cq
outer_length = 80.0
outer_width = 40.0
bracket_thickness = 4.0
central_hole_diameter = 20.0
central_hole_depth = 3.0
central_hole_diameter = central_hole_diameter + 2.0
central_fillet_radius = 2.0
mount_hole_diameter = 5.0
mount_cbore_diameter = 8.0
mount_cbore_depth = 2.0
mount_cbore_spacing = 60.0
mount_hole_spacing = 60.0
mount_hole_offset_y = 10.0
pocket_length = 30.0
pocket_width = 20.0
pocket_depth = 2.0
pocket_fillet_radius = 2.0
mount_hole_diameter = 5.0
mount_cbore_diameter = 8.0
mount_cbore_depth = 2.0
mount_cbore_spacing = mount_cbore_spacing
mount_cbore_depth = mount_cbore_depth
outer = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(bracket_thickness)
)
outer = (
    outer
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter / 2)
    .cutBlind(-bracket_thickness)
)
mount_face = outer.faces(">Z").workplane()
mount_face = mount_face.workplane()
mount_pts = [
    (mount_hole_offset_y, mount_hole_offset_y),
    (-mount_hole_offset_y, mount_hole_offset_y),
    (-mount_hole_offset_y, -mount_hole_offset_y),
    (mount_hole_offset_y, -mount_hole_offset_y),
]
mount_pts = [
    (mount_hole_offset_y, -mount_hole_offset_y),
    (-mount_hole_offset_y, -mount_hole_offset_y),
]
result = (
    mount_pts
    .faces(">Z")
    .workplane()
    .pushPoints(mount_pts)
    .cboreHole(mount_hole_diameter, mount_cbore_diameter, mount_cbore_depth)
)
