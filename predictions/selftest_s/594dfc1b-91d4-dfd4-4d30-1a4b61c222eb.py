import cadquery as cq

outer_diameter = 80.0
wall_thickness = 4.0
head_height = 20.0
dome_height = 30.0
dome_steps = 6
step_height = dome_height / dome_steps
port_width = 15.0
port_depth = 25.0
port_chamfer = 1.0
mount_hole_diameter = 6.0
mount_hole_distance = 30.0
rib_height = 10.0

# Base cylinder (head body)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(head_height)
)

# Lofted dome on top of base
radius_start = outer_diameter / 2
radius_end = (outer_diameter / 2) - wall_thickness * 2

dome = (
    base.faces("+Z")
    .workplane()
    .circle(radius_start)
)

for i in range(1, dome_steps + 1):
    t = i / dome_steps
    radius_i = radius_start - t * (radius_start - radius_end)
    dome = dome.workplane(offset=step_height).circle(radius_i)

dome = dome.loft(combine=True)

# Central reinforcing rib inside dome
rib = (
    dome.faces("+Z")
    .workplane()
    .circle((outer_diameter / 2) - wall_thickness * 3)
    .extrude(rib_height)
)

cylinder_with_rib = dome.union(rib)

# Rectangular port on side (+Y) with chamfer
port_center_y = (outer_diameter / 2) - wall_thickness - port_width / 2
port = (
    cq.Workplane("XY")
    .center(0, port_center_y)
    .rect(port_width, port_width)
    .extrude(port_depth)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .edges("|Y")
    .chamfer(port_chamfer)
)

cylinder_with_port = cylinder_with_rib.cut(port)

# Mounting holes on the bottom planar face using a global workplane
result = (
    cylinder_with_port
    .workplane()
    .pushPoints([
        (mount_hole_distance, 0),
        (-mount_hole_distance, 0),
        (0, mount_hole_distance),
        (0, -mount_hole_distance),
    ])
    .hole(mount_hole_diameter)
)
