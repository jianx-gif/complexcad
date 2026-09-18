import cadquery as cq

# parameters
bracket_width = 60.0
bracket_depth = 20.0
base_thickness = 8.0
leg_height = 30.0
leg_thickness = 8.0
rib_width = 4.0
rib_height = 6.0
rib_spacing = 10.0
rib_offset = 2.0
rib_start = 5.0
hole_diameter = 6.0
chamfer_size = 1.0

# base L-shaped profile
base_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(bracket_width, 0)
    .lineTo(bracket_width, base_thickness)
    .lineTo(leg_thickness, base_thickness)
    .lineTo(leg_thickness, base_thickness + leg_height)
    .lineTo(0, base_thickness + leg_height)
    .close()
)

# extrude base profile
base = base_profile.extrude(bracket_depth)

# apply chamfer to outer vertical edges of base before adding ribs
base = base.edges("|Z").chamfer(chamfer_size)

# calculate number of ribs
num_ribs = int((leg_height - 2 * rib_start) / rib_spacing) + 1

# generate rib solids in a loop and union them
rib_union = None
for i in range(num_ribs):
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(bracket_depth)
        .translate((leg_thickness + rib_offset, base_thickness + rib_start + i * rib_spacing, 0))
    )
    rib_union = rib if rib_union is None else rib_union.union(rib)

combined = base if rib_union is None else base.union(rib_union)

# through pin hole centered on top flange
result = (
    combined.faces(">Z").workplane()
    .center(bracket_width / 2, base_thickness / 2)
    .hole(hole_diameter)
)
