import cadquery as cq

handle_length = 80
outer_radius = 10
inner_radius = 6
mount_hole_diameter = 5
mount_hole_spacing = 50
counterbore_diameter = 8
counterbore_depth = 5
chamfer_distance = 0.8
rib_thickness = 1.5
rib_width = 2
rib_margin = 10
grip_recess_extra = 1
grip_recess_depth = 4

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(handle_length)
)

hole_positions = [(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)]
body_with_holes = (
    base
    .faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(mount_hole_diameter, counterbore_diameter, counterbore_depth)
)

inner_recess = (
    cq.Workplane("XY")
    .circle(inner_radius + grip_recess_extra)
    .extrude(grip_recess_depth)
    .translate((0, 0, handle_length/2 - grip_recess_depth/2))
)
body_with_recess = body_with_holes.cut(inner_recess)

body_top_chamfer = (
    body_with_recess
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)
body_chamfered = body_top_chamfer.faces("<Z").edges().chamfer(chamfer_distance)

rib_profile = (
    cq.Workplane("XZ")
    .rect(rib_thickness, handle_length - 2 * rib_margin)
    .extrude(rib_width)
    .translate((outer_radius - (outer_radius - inner_radius)/2 - rib_thickness/2, 0, rib_margin))
)

rib_rotated = rib_profile.rotate((0, 0, 0), (0, 0, 1), 90)
result = body_chamfered.union(rib_profile).union(rib_rotated)
