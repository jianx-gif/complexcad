
import cadquery as cq

outer_diameter = 80
wall_thickness = 4
shell_length = 60
gasket_clearance = 0.5
gasket_pocket_length = 20
port_diameter = 15
port_offset = 10
chamfer_size = 1.5
rib_width = 8
rib_height = 12
rib_depth = 2
tab_thickness = 6
tab_height = 20
tab_width = 12
overlap = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
half_length = shell_length / 2.0

profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, -half_length)
    .lineTo(outer_radius, half_length)
    .lineTo(inner_radius, half_length)
    .lineTo(inner_radius, -half_length)
    .close()
)

base_shell = profile.revolve()

pocket_radius = inner_radius - gasket_clearance - 1.0
pocket = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(pocket_radius)
    .extrude(gasket_pocket_length)
    .rotate((0, 0, 0), (1, 0, 0), 90)
)

port_cyl = (
    cq.Workplane("XY")
    .center(0, port_offset)
    .circle(port_diameter / 2.0)
    .extrude(wall_thickness + 2.0)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((outer_radius - wall_thickness / 2.0, 0, 0))
)

rib_groove = (
    cq.Workplane("XY")
    .box(rib_depth, rib_width, rib_height)
    .translate((inner_radius - rib_depth / 2.0, 0, 0))
)

tab_center_x = outer_radius - overlap + tab_thickness / 2.0
mount_tab = (
    cq.Workplane("XY")
    .box(tab_thickness, tab_height, tab_width)
    .translate((tab_center_x, -half_length + tab_height / 2.0, 0))
    .edges("|Z")
    .chamfer(chamfer_size)
)

result = (
    base_shell
    .cut(pocket)
    .cut(port_cyl)
    .cut(rib_groove)
    .union(mount_tab)
)
