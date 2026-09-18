import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    width=60.0,
    depth=40.0,
    thickness=8.0,
    relief_width=20.0,
    relief_depth=30.0,
    relief_thickness=6.0,
    chamfer=0.5,
    rib_height=3.0,
    rib_thickness=2.0,
    hole_diameter=4.0,
    hole_spacing=30.0,
    top_radius=2.0,
)

# Base plate
result = (
    cq.Workplane('XY')
    .rect(params.width, params.depth)
    .extrude(params.thickness)
)

# Reinforcing ribs on top surface
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints([(-params.hole_spacing/2, 0), (params.hole_spacing/2, 0)])
    .rect(params.rib_thickness, params.rib_height)
    .extrude(params.thickness/2)
)

# Mounting holes through ribs
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints([(-params.hole_spacing/2, 0), (params.hole_spacing/2, 0)])
    .hole(params.hole_diameter)
)

# Side relief cut on +Y face
result = (
    result.faces('>Y')
    .workplane()
    .center(0, 0)
    .rect(params.relief_width, params.thickness - params.relief_thickness)
    .cutBlind(-params.relief_depth)
)

# Chamfer inner vertical edges of the relief pocket
result = (
    result.edges('|Y')
    .chamfer(params.chamfer)
)

# Fillet top outer edges for safety
result = (
    result.faces('>Z')
    .edges('|X')
    .fillet(params.top_radius)
)
