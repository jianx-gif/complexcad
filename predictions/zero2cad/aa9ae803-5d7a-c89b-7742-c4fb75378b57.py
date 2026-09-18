import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 40.0
housing_length = 60.0
flange_thickness = 10.0
flange_diameter = 100.0
groove_width = 5.0
groove_depth = 4.0
groove_position = 30.0
fillet_radius = 2.0
mount_hole_diameter = 15.0
mount_hole_offset = 25.0
rib_thickness = 3.0
rib_height = 10.0
rib_spacing = 15.0

# Base housing cylinder
housing = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(housing_length)
)

# Central bore
bore = (
    cq.Workplane("XY")
    .circle(inner_diameter / 2)
    .extrude(housing_length)
)

housing = housing.cut(bore)

# Flange at bottom
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

housing = housing.union(flange)

# Fillet on outer top edge (horizontal edge)
housing = housing.edges(">Z").fillet(fillet_radius)

# O‑ring groove (radial cut on inner wall)
groove = (
    cq.Workplane("XY")
    .circle(inner_diameter / 2 + groove_width)
    .extrude(groove_depth)
    .translate((0, 0, groove_position))
)

housing = housing.cut(groove)

# Mounting hole through flange (offset from center)
housing = (
    housing.faces("<Z")
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)

# Internal ribs for stiffness (radial ribs inside bore)
num_ribs = int((housing_length - flange_thickness) // rib_spacing)
for i in range(num_ribs):
    z_pos = flange_thickness + rib_spacing * i + rib_spacing / 2
    rib = (
        cq.Workplane("XY")
        .circle(inner_diameter / 2 + rib_thickness)
        .extrude(rib_height)
        .translate((0, 0, z_pos))
    )
    housing = housing.union(rib)

result = housing