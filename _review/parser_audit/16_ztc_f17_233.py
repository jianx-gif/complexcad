import cadquery as cq

panel_width = 80.0
panel_height = 50.0
panel_thickness = 5.0
hole_diameter = 10.0
hole_spacing = 13.0
edge_fillet_radius = 2.0
rib_height = 3.0
rib_width = 8.0
rib_spacing = 20.0
corner_hole_dia = 6.0
corner_hole_offset = 5.0

# Base panel with a central hexagonal cutout to avoid trivial profile
base = (
    cq.Workplane("XY")
    .rect(panel_width, panel_height)
    .extrude(panel_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .polygon(6, panel_width * 0.3)
    .cutBlind(-panel_thickness)
)

# Rolled edge via fillet on outer perimeter edges
base = base.edges(">Z or <Z").fillet(edge_fillet_radius)

# Linear series of six holes, centered horizontally, positioned above bottom edge
hole_start_y = -panel_height/2 + corner_hole_offset + hole_diameter/2 + 5.0
base = (
    base.workplane(offset=panel_thickness/2)
    .center(- (hole_spacing * 2.5), hole_start_y)
    .rarray(hole_spacing, 0, 6, 1)
    .hole(hole_diameter)
)

# Corner mounting countersunk holes
corner_positions = [
    (-panel_width/2 + corner_hole_offset, -panel_height/2 + corner_hole_offset),
    ( panel_width/2 - corner_hole_offset, -panel_height/2 + corner_hole_offset),
    (-panel_width/2 + corner_hole_offset,  panel_height/2 - corner_hole_offset),
    ( panel_width/2 - corner_hole_offset,  panel_height/2 - corner_hole_offset),
]
base = (
    base.workplane(offset=panel_thickness/2)
    .pushPoints(corner_positions)
    .cboreHole(corner_hole_dia, corner_hole_dia*1.5, 2.0)
)

# Reinforcing ribs on back side, evenly spaced
rib_count = int((panel_width - 2 * corner_hole_offset) // rib_spacing)
rib_positions = [ -panel_width/2 + corner_hole_offset + rib_spacing/2 + i * rib_spacing for i in range(rib_count) ]
result = base
for x in rib_positions:
    rib = (
        cq.Workplane("XY")
        .center(x, 0)
        .rect(rib_width, panel_height - 2*corner_hole_offset)
        .extrude(-rib_height)
    )
    result = result.union(rib)
