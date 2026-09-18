import cadquery as cq

# Parameters
handle_length = 80
handle_radius = 12
hand_flat_width = 20
rib_width = 4
rib_height = 8
rib_count = 6
set_screw_diameter = 4
set_screw_thread_dia = 3.5
set_screw_depth = 12
set_screw_offset = 5
chamfer_size = 1.0

# Create handle body by revolving a composite sketch
handle_body = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(handle_radius, 0)
    .threePointArc((handle_radius + 3, handle_length * 0.2), (handle_radius, handle_length * 0.4))
    .lineTo(handle_radius + hand_flat_width, handle_length * 0.4)
    .lineTo(handle_radius + hand_flat_width, handle_length)
    .lineTo(0, handle_length)
    .close()
    .revolve()
)

# Create side ribs manually and pattern them around the axis
ribs = None
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(handle_length)
        .translate((handle_radius + rib_width / 2, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    ribs = rib if ribs is None else ribs.union(rib)

combined = handle_body.union(ribs)

# Add tapped hole for set screw on flat side near top
result = (
    combined
    .faces('>Z')
    .workplane()
    .center(handle_radius + hand_flat_width - set_screw_offset, 0)
    .hole(set_screw_thread_dia, depth=set_screw_depth)
    .faces('>Z')
    .edges()
    .chamfer(chamfer_size)
)
