import cadquery as cq
# Parameters
beam_length = 80.0
beam_depth = 30.0
flange_width = 60.0
web_thickness = 4.0
flange_thickness = 6.0
pattern_count = 5
spacing = 20.0
chamfer_len = 1.0
# Derived half-beam dimensions
half_flange_x = flange_width / 2.0
# Points for half I-beam profile (right side)
pts_half = [
    (0, -beam_depth/2),
    (0, -beam_depth/2 + flange_thickness),
    (half_flange_x, -beam_depth/2 + flange_thickness),
    (half_flange_x, beam_depth/2 - flange_thickness),
    (0, beam_depth/2 - flange_thickness),
    (0, beam_depth/2)
]
# Create base half-beam, mirror to full, extrude along Z, then chamfer vertical edges
base_beam = (
    cq.Workplane("XY")
    .polyline(pts_half)
    .close()
    .mirrorY()
    .extrude(beam_length)
    .edges("|Z")
    .chamfer(chamfer_len)
)
# Build zigzag array of beams
beam_parts = []
for i in range(pattern_count):
    offset_x = i * spacing
    offset_y = (spacing/2) if i % 2 == 0 else -(spacing/2)
    part = base_beam.translate((offset_x, offset_y, 0))
    beam_parts.append(part)
# Create connectors between adjacent beams (rectangular ribs)
connector_parts = []
for i in range(pattern_count-1):
    x1 = i * spacing
    x2 = (i+1) * spacing
    mid_x = (x1 + x2) / 2.0
    connector = (
        cq.Workplane('XY')
        .box(spacing - 2*web_thickness, web_thickness, beam_length)
        .translate((mid_x, 0, 0))
    )
    connector_parts.append(connector)
# Union all components into a single solid
result = beam_parts[0]
for part in beam_parts[1:]:
    result = result.union(part)
for conn in connector_parts:
    result = result.union(conn)
