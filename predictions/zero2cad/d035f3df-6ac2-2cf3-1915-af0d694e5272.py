import cadquery as cq

# Parameters
base_width = 50.0
base_height = 30.0
base_thickness = 10.0
top_diameter = 40.0
loft_height = 80.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
rib_width = 5.0
rib_height = 15.0
rib_thickness = 3.0
rib_offset = 12.0

# Base rectangular profile
base_profile = cq.Workplane("XY").rect(base_width, base_height)

# Lofted body from rectangle to circle
loft_body = (
    base_profile
    .workplane(offset=loft_height)
    .circle(top_diameter / 2)
    .loft(combine=True)
)

# Fillet all edges for safety
loft_body = loft_body.edges().fillet(fillet_radius)

# Mounting holes on the rectangular base (bottom face)
hole_positions = [(-hole_spacing / 2, 0), (hole_spacing / 2, 0)]
loft_body = (
    loft_body
    .faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Internal rib for stiffness (centered on X axis, offset in Y)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, rib_offset, loft_height / 2))
)

# Combine rib with lofted body
result = loft_body.union(rib)
