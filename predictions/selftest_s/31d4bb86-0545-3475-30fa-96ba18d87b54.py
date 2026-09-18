import cadquery as cq

# Parameters
bracket_length = 80.0
channel_width = 30.0
channel_height = 20.0
wall_thickness = 5.0
profile_width = channel_width + 2 * wall_thickness
profile_height = channel_height + 2 * wall_thickness
fillet_radius = 2.0
countersink_angle = 82.0
hole_diameter = 5.0
countersink_diameter = 9.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
rib_height = 6.0
rib_thickness = 4.0
rib_position = 40.0

# Sweep path (straight line along X)
path_wire = (
    cq.Workplane("XY")
    .lineTo(bracket_length, 0)
    .wire()
)

# Sweep profile (rectangle in YZ plane) – pending wire on workplane
profile_wp = cq.Workplane("YZ").rect(profile_width, profile_height)

# Main bracket solid by sweep
bracket = profile_wp.sweep(path_wire)

# Fillet at sweep start (face at X=0)
bracket = bracket.faces("<X").edges().fillet(fillet_radius)

# Chamfer outer edges on +Y side for safety
bracket = bracket.faces(">Y").edges().chamfer(chamfer_size)

# Create U‑shaped channel cut (inner void, open on +Y side)
inner_width = channel_width
inner_height = channel_height
channel_cut = (
    cq.Workplane("YZ")
    .transformed(offset=(0, wall_thickness, 0))
    .rect(inner_width, inner_height)
    .extrude(-bracket_length)
)
bracket = bracket.cut(channel_cut)

# Add reinforcing rib on top face (+Z)
rib = (
    cq.Workplane("XY")
    .center(rib_position, 0)
    .rect(rib_thickness, rib_height)
    .extrude(wall_thickness)
)
bracket = bracket.union(rib)

# Countersunk holes on top face, evenly spaced
hole_positions = [
    (-hole_spacing / 2, hole_offset),
    (0, hole_offset),
    (hole_spacing / 2, hole_offset)
]
bracket = (
    bracket.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

result = bracket