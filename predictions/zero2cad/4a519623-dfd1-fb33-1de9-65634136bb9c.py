import cadquery as cq

# Parameters
channel_width = 80.0
channel_height = 60.0
wall_thickness = 5.0
length = 100.0
chamfer_size = 2.0
hole_diameter = 6.0
hole_spacing = 40.0
rib_width = 10.0
rib_height = 8.0
rib_spacing = 20.0

# Base solid: outer block
outer = cq.Workplane('XY').rect(channel_width, channel_height).extrude(length)

# Inner void to create C‑section (open on +X side)
inner_width = channel_width - wall_thickness
inner_height = channel_height - 2 * wall_thickness
inner = (
    cq.Workplane('XY')
    .rect(inner_width, inner_height)
    .translate((wall_thickness / 2, 0, 0))
    .extrude(length)
)

# Subtract inner void
result = outer.cut(inner)

# Chamfer outer edges (all edges parallel to Z)
result = result.edges("|Z").chamfer(chamfer_size)

# Add mounting holes on the top flange (face +Y)
result = (
    result.faces('>Y')
    .workplane()
    .rarray(0, hole_spacing, 1, 2)
    .hole(hole_diameter)
)

# Add internal ribs on the inner web (face -X)
rib_count = int((length - rib_spacing) // rib_spacing) + 1
result = (
    result.faces('<X')
    .workplane()
    .rarray(0, rib_spacing, 1, rib_count)
    .rect(rib_width, rib_height)
    .cutBlind(-wall_thickness)
)
