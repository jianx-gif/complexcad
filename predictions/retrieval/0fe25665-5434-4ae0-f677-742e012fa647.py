
import cadquery as cq

outer_radius = 30.0
inner_radius = 20.0
lip_width = 2.0
groove_width = 2.0
flange_radius = outer_radius + 5.0
flange_thickness = 5.0
shaft_length = 60.0
chamfer_distance = 0.8
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0

groove_start = shaft_length - flange_thickness - lip_width - groove_width - lip_width

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, shaft_length - flange_thickness)
    .lineTo(flange_radius, shaft_length - flange_thickness)
    .lineTo(flange_radius, shaft_length)
    .lineTo(0, shaft_length)
    .lineTo(inner_radius + lip_width, shaft_length)
    .lineTo(inner_radius + lip_width, groove_start + lip_width + groove_width)
    .lineTo(inner_radius, groove_start + lip_width + groove_width)
    .lineTo(inner_radius, groove_start)
    .lineTo(inner_radius + lip_width, groove_start)
    .lineTo(inner_radius + lip_width, 0)
    .close()
)

result = (
    profile.revolve(360)
    .edges().chamfer(chamfer_distance)
    .faces(">Z").workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)
