import cadquery as cq
import math

# Parameters
base_length = 80.0
base_width = 30.0
base_thickness = 5.0
lip_length = 40.0
lip_max_height = 15.0
lip_tip_thickness = 6.0
lip_taper_angle = 30.0
clearance_hole_diameter = 4.0
clearance_hole_offset = 10.0
fillet_radius = 2.0
chamfer_distance = 1.0
rib_width = 5.0
rib_height = 4.0
rib_spacing = 12.0

# Helper to create tapered lip profile

def lip_profile(length, max_height, tip_thick, taper_angle):
    half = math.radians(taper_angle / 2)
    tip_x_offset = length * math.tan(half)
    pts = [
        (0, 0),
        (0, max_height),
        (length - tip_x_offset, max_height),
        (length, tip_thick),
        (length, 0),
        (0, 0),
    ]
    return cq.Workplane('XZ').polyline(pts).close()

# Base plate with edge tag for later fillet
base = (
    cq.Workplane('XY')
    .rect(base_length, base_width)
    .extrude(base_thickness)
    .edges('|Z')
    .tag('base_vert_edges')
)

# Lip creation and positioning (overlap 0.5 mm into base for solid union)
lip_sketch = lip_profile(lip_length, lip_max_height, lip_tip_thickness, lip_taper_angle)
lip = (
    lip_sketch
    .extrude(base_width)
    .translate((0, -base_width/2, 0))
    .translate((base_length/2 - 0.5, 0, 0))
)

# Assemble base and lip
assembly = base.union(lip)

# Clearance hole through lip tip
hole_x = base_length/2 + lip_length - clearance_hole_offset
assembly = (
    assembly
    .faces('>Z')
    .workplane(centerOption='CenterOfBoundBox')
    .center(hole_x - base_length/2, 0)
    .hole(clearance_hole_diameter)
)

# Fillet base vertical edges (external)
assembly = assembly.edges(tag='base_vert_edges').fillet(fillet_radius)

# Chamfer the lip tip edge (vertical edge at furthest X)
assembly = assembly.edges('>>X and |Z').chamfer(chamfer_distance)

# Reinforcing ribs on back side of base
rib_count = int((base_length - 20) // rib_spacing)
for i in range(rib_count):
    rib_x = -base_length/2 + 10 + i * rib_spacing
    rib = (
        cq.Workplane('XY')
        .center(rib_x, 0)
        .rect(rib_width, rib_height)
        .extrude(base_thickness)
    )
    assembly = assembly.union(rib)

result = assembly