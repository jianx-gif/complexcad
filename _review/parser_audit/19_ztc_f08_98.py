import cadquery as cq

outer_radius = 30.0
wall_thickness = 2.0
pipe_length = 80.0
knurl_count = 24
knurl_diameter = 2.0
knurl_height = 0.5
hole_diameter = 3.0
hole_pitch = 5.0
hole_angle_step = 20.0
chamfer_size = 0.3

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius - wall_thickness, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, pipe_length)
    .lineTo(outer_radius - wall_thickness, pipe_length)
    .close()
)
pipe = profile.revolve()
pipe = pipe.edges(">Z or <Z").chamfer(chamfer_size)

# Add knurl as radial cylinders around mid-length
mid_z = pipe_length / 2
for i in range(knurl_count):
    angle = i * (360.0 / knurl_count)
    knurl = (
        cq.Workplane("YZ")
        .center(outer_radius - wall_thickness/2, 0)
        .circle(knurl_diameter/2)
        .extrude(knurl_height)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((0, 0, mid_z))
    )
    pipe = pipe.union(knurl)

# Add spiral clearance holes (axial holes through wall with varying Z and rotation)
num_holes = int(pipe_length / hole_pitch)
for i in range(num_holes):
    z = i * hole_pitch + hole_pitch/2
    angle = i * hole_angle_step
    cutter = (
        cq.Workplane("YZ")
        .center(outer_radius - wall_thickness/2, 0)
        .circle(hole_diameter/2)
        .extrude(wall_thickness*2)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((0, 0, z))
    )
    pipe = pipe.cut(cutter)

result = pipe