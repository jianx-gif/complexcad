import cadquery as cq

outer_radius = 30
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
guide_length = 80
rib_thickness = 2
rib_height = 8
rib_base_height = 30
side_hole_diameter = 4
side_hole_position = 40
mounting_hole_diameter = 3
mounting_hole_spacing = 20
num_mounting_holes = 2
chamfer_size = 0.5

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_base_height)
    .lineTo(inner_radius - rib_thickness, rib_base_height)
    .lineTo(inner_radius - rib_thickness, rib_base_height + rib_height)
    .lineTo(inner_radius, rib_base_height + rib_height)
    .lineTo(inner_radius, guide_length)
    .lineTo(outer_radius, guide_length)
    .lineTo(outer_radius, 0)
    .close()
)

result = profile.revolve(360)

result = (
    result
    .faces(">X")
    .first()
    .workplane()
    .center(0, side_hole_position)
    .hole(side_hole_diameter)
)

mount_positions = [
    (0, side_hole_position - mounting_hole_spacing / 2),
    (0, side_hole_position + mounting_hole_spacing / 2),
]

result = (
    result
    .faces(">X")
    .first()
    .workplane()
    .pushPoints(mount_positions)
    .hole(mounting_hole_diameter)
)

result = result.edges(">Z").chamfer(chamfer_size)
