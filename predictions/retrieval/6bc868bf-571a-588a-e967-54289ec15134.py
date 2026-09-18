import cadquery as cq

# Parameters
hex_flat = 80.0
hex_length = 80.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 6.0
rib_width = 20.0
rib_height = 10.0
rib_thickness = 2.0

# Base hexagonal solid
outer = cq.Workplane('XY').polygon(6, hex_flat).extrude(hex_length)

# Thin-walled conduit
hollow = outer.shell(-wall_thickness)

# Chamfer outer longitudinal edges
chamfered = hollow.edges('|Z').chamfer(chamfer_distance)

# Internal rib positioned near +X inner wall
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((hex_flat/2 - wall_thickness, 0, 0))
)

# Combine rib with conduit
with_rib = chamfered.union(rib)

# Drill opposite side holes through +X and -X walls
with_holes = (
    with_rib.faces('>X').hole(hole_diameter)
            .faces('<X').hole(hole_diameter)
)

result = with_holes
