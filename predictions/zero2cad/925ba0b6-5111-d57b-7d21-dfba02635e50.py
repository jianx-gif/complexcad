import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 40.0
ring_thickness = 20.0
rib_height = 8.0
rib_width = 6.0
counterbore_diameter = 16.0
counterbore_depth = 8.0
through_hole_diameter = 10.0
chamfer_distance = 2.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_outer_radius = outer_radius + rib_height
rib_inner_radius = outer_radius - rib_width

# Base ring profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(rib_inner_radius, 0)
    .lineTo(rib_inner_radius, ring_thickness - rib_width)
    .threePointArc((rib_outer_radius, ring_thickness - rib_width / 2), (rib_outer_radius, ring_thickness))
    .lineTo(inner_radius, ring_thickness)
    .close()
)
ring = profile.revolve()

# Counterbore holes (two opposite)
hole_radius = (inner_radius + outer_radius) / 2.0
hole_positions = [(hole_radius, 0), (-hole_radius, 0)]
ring = (
    ring
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(through_hole_diameter, counterbore_diameter, counterbore_depth)
)

# Chamfer outer cylindrical edge
ring = ring.edges("|Z").chamfer(chamfer_distance)

result = ring