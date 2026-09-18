import cadquery as cq

# Parameters
outer_diameter = 60.0
wall_thickness = 5.0
height = 15.0
cavity_radius = 12.0
chamfer_distance = 1.5
mount_hole_diameter = 4.0
mount_offset = 10.0
ring_thickness = 4.0
ring_height = 8.0
ring_offset_radius = outer_diameter/2 + ring_thickness/2 + 2.0

# Hexagonal frame base
hex_profile = (
    cq.Workplane("XY")
    .polygon(6, outer_diameter)
    .extrude(height)
)

# Central circular cavity
cavity = (
    cq.Workplane("XY")
    .circle(cavity_radius)
    .extrude(height)
)
frame_with_cavity = hex_profile.cut(cavity)

# Chamfer on outer edges (approximate 15° chamfer)
frame_chamfered = (
    frame_with_cavity
    .edges()
    .chamfer(chamfer_distance)
)

# Mounting holes placed near three alternating vertices
mounting_holes = (
    frame_chamfered
    .faces("<Z")
    .workplane()
    .pushPoints([
        (mount_offset, outer_diameter/2 * 0.57735),
        (-mount_offset, -outer_diameter/2 * 0.57735),
        (mount_offset, -outer_diameter/2 * 0.57735),
    ])
    .hole(mount_hole_diameter)
)

# Revolve-generated toroidal pocket intersecting top surface
ring_profile = (
    cq.Workplane("XZ")
    .rect(ring_thickness, ring_height)
    .translate((ring_offset_radius + ring_thickness/2, 0, 0))
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Position pocket so it penetrates the top face
ring_positioned = ring_profile.translate((0, 0, height - ring_height/2))

result = mounting_holes.cut(ring_positioned)
