import cadquery as cq

# Parameters
body_length = 80.0
outer_diameter = 40.0
wall_thickness = 3.0
flange_diameter = 60.0
flange_thickness = 5.0
inlet_diameter = 20.0
outlet_diameter = 25.0
chamfer_size = 2.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_offset = 10.0
rib_thickness = 2.0
rib_height = 15.0
rib_spacing = 20.0
pocket_width = 12.0
pocket_height = 20.0
pocket_depth = 4.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
flange_radius = flange_diameter / 2.0
inner_radius = outer_radius - wall_thickness
inlet_radius = inlet_diameter / 2.0
outlet_radius = outlet_diameter / 2.0

# Base body loft between two offset circles
body = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .workplane(offset=body_length)
    .center(outer_radius * 0.5, 0)
    .circle(outer_radius)
    .loft()
)

# Shell to create wall thickness
body = body.shell(-wall_thickness)

# Chamfer on outlet edge (top face)
body = body.faces(">Z").edges().chamfer(chamfer_size)

# Inlet port cut through body
inlet_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(inlet_radius)
    .extrude(body_length + 2)
)
body = body.cut(inlet_cut)

# Outlet port cut through body
outlet_cut = (
    cq.Workplane("XY")
    .center(outer_radius * 0.5, 0)
    .circle(outlet_radius)
    .extrude(body_length + 2)
)
body = body.cut(outlet_cut)

# Flange at inlet side (negative Z direction)
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .translate((0, 0, -flange_thickness))
)
body = body.union(flange)

# Mounting holes on flange (four-hole rectangular pattern)
hole_positions = [
    (-mount_hole_spacing/2, -mount_hole_offset),
    (mount_hole_spacing/2, -mount_hole_offset),
    (-mount_hole_spacing/2, mount_hole_offset),
    (mount_hole_spacing/2, mount_hole_offset),
]
for x, y in hole_positions:
    hole = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(mount_hole_diameter/2)
        .extrude(flange_thickness + 2)
    )
    body = body.cut(hole)

# Internal ribs for stiffness (radial ribs spaced along length)
num_ribs = int(body_length // rib_spacing)
for i in range(num_ribs):
    z_pos = (i + 0.5) * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(inner_radius - rib_thickness/2, 0)
        .rect(rib_thickness, rib_height)
        .extrude(rib_thickness)
        .translate((0, 0, z_pos))
    )
    body = body.union(rib)

# Side pocket for cable routing (cut into side wall)
pocket = (
    cq.Workplane("XY")
    .center(-outer_radius + wall_thickness/2, 0)
    .rect(pocket_width, pocket_height)
    .extrude(pocket_depth)
    .translate((0, 0, body_length/2))
)
body = body.cut(pocket)

result = body