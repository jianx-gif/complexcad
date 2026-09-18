import cadquery as cq

total_length = 80.0
outer_radius_start = 20.0
outer_radius_end = outer_radius_start * 0.8
wall_thickness = 2.0
flange_thickness = 4.0
flange_extension = 6.0
chamfer_size = 1.0
hole_diameter = 5.0

profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(outer_radius_start + flange_extension, 0)
    .lineTo(outer_radius_start + flange_extension, flange_thickness)
    .lineTo(outer_radius_start, flange_thickness)
    .lineTo(outer_radius_start, total_length)
    .lineTo(outer_radius_end, total_length)
    .lineTo(0, total_length)
    .close()
)

solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

# Chamfer inlet edge (bottom)
try:
    hollow = hollow.edges('<Z').chamfer(chamfer_size)
except Exception:
    pass
# Chamfer outlet edge (top)
try:
    hollow = hollow.edges('>Z').chamfer(chamfer_size)
except Exception:
    pass

# Add a through hole through the outlet face
hollow = (
    hollow.faces('>Z')
    .workplane(centerOption='CenterOfMass')
    .hole(hole_diameter)
)

result = hollow