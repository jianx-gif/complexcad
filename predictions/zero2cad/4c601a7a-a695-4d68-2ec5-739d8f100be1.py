import cadquery as cq

# Parameters
clip_length = 80.0
clip_width = 30.0
clip_thickness = 5.0
wall_thickness = 2.0
snap_height = 12.0
snap_thickness = 1.5
snap_extension = 5.0
snap_chamfer = 0.3
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset_y = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(clip_length, clip_width)
    .extrude(clip_thickness)
)

# Snap‑fit protrusion on the +Y side
snap = (
    base.faces(">Y")
    .workplane()
    .center(0, 0)
    .polyline([
        (0, 0),
        (snap_thickness, 0),
        (snap_thickness, snap_height),
        (0, snap_height - snap_thickness)
    ])
    .close()
    .extrude(snap_extension)
)

# Combine base and snap
combined = base.union(snap)

# Chamfer all edges for safety
combined = combined.edges().chamfer(snap_chamfer)

# Add two mounting holes on the top face
result = (
    combined.faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, hole_offset_y), (hole_spacing/2, hole_offset_y)])
    .hole(hole_diameter)
)
