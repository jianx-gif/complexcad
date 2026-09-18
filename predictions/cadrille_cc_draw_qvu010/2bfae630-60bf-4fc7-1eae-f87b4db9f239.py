import cadquery as cq
outer_diameter = 40.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 12
hole_radius = inner_radius + wall_thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(outer_diameter / 2.0, outer_diameter / 2.0)
    .lineTo(0, outer_diameter / 2.0)
    .close()
)
solid = profile.revolve()
hollow = solid.shell(-wall_thickness)
chamfered = hollow.edges().chamfer(chamfer_distance)
hole_positions = [
    (hole_spacing / 2.0, hole_spacing / 2.0),
    (hole_spacing / 2.0, hole_spacing / 2.0),
    (-hole_spacing / 2.0, hole_spacing / 2.0),
    (hole_spacing / 2.0, hole_spacing / 2.0)
]
result = (
    hollow
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
