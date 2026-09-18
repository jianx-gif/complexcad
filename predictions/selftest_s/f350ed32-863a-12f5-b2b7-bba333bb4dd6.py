import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=60.0,
    depth=30.0,
    thickness=6.0,
    nub_width=20.0,
    nub_depth=10.0,
    nub_height=2.0,
    slot_width=5.0,
    slot_length=45.0,
    slot_offset_y=8.0,
    slot_fillet_radius=1.0,
    outer_chamfer=0.5,
    hole_diameter=3.0,
    hole_offset_y=10.0,
    hole_spacing_x=40.0
)

# Base plate
result = (
    cq.Workplane('XY')
    .rect(m.width, m.depth)
    .extrude(m.thickness)
    # Raised central nub
    .faces('>Z').workplane()
    .rect(m.nub_width, m.nub_depth)
    .extrude(m.nub_height)
    # Symmetrical slots
    .faces('>Z').workplane()
    .rect(m.slot_width, m.slot_length)
    .center(0, m.slot_offset_y)
    .cutBlind(-m.thickness)
    .faces('>Z').workplane()
    .rect(m.slot_width, m.slot_length)
    .center(0, -m.slot_offset_y)
    .cutBlind(-m.thickness)
    # Fillet slot edges
    .edges('|Y and >Z').fillet(m.slot_fillet_radius)
    # Outer chamfer
    .edges('|X and >Z').chamfer(m.outer_chamfer)
    # Mounting holes
    .faces('<Z').workplane()
    .pushPoints([(-m.hole_spacing_x/2, m.hole_offset_y), (m.hole_spacing_x/2, m.hole_offset_y)])
    .hole(m.hole_diameter)
)
