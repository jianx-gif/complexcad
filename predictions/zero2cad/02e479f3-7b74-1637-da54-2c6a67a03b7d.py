import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 5.0
base_thickness = 8.0
dome_height = 20.0
vent_width = 12.0
vent_height = 30.0
vent_depth = wall_thickness + 2.0
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(inner_radius, base_thickness)
    .lineTo(inner_radius, base_thickness + dome_height)
    .threePointArc((inner_radius + (outer_radius - inner_radius) / 2, base_thickness + dome_height + 5), (outer_radius, base_thickness + dome_height))
    .lineTo(0, base_thickness + dome_height)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)

# Chamfer bottom edge for safety
hollow = hollow.faces("<Z").edges().chamfer(chamfer_size)

# Vent slot cut through side wall
vent = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness / 2, 0)
    .rect(vent_width, vent_height)
    .extrude(vent_depth)
    .translate((0, 0, base_thickness + dome_height / 2 - vent_height / 2))
)

hollow = hollow.cut(vent)

# Mounting holes on base plate (four-hole rectangular pattern)
hole_positions = [
    (-mount_hole_spacing / 2, -mount_hole_offset),
    (mount_hole_spacing / 2, -mount_hole_offset),
    (-mount_hole_spacing / 2, mount_hole_offset),
    (mount_hole_spacing / 2, mount_hole_offset),
]

hollow = (
    hollow.faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)

result = hollow