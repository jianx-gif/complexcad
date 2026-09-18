import cadquery as cq

body_outer_radius = 25
body_inner_radius = 20
body_length = 60
wall_thickness = body_outer_radius - body_inner_radius
inlet_radius = 10
inlet_chamfer = 2
flow_port_radius = 6
flow_port_z = 30
pocket_radius = 8
pocket_depth = 4
mount_hole_radius = 3
mount_spacing = 30
rib_width = 8
rib_height = 12
rib_thickness = 3
rib_z = body_length/2

base = (
    cq.Workplane("XZ")
    .polyline([
        (body_inner_radius, 0),
        (body_outer_radius, 0),
        (body_outer_radius, body_length),
        (body_inner_radius, body_length),
        (body_inner_radius, 0)
    ])
    .close()
    .revolve()
)

with_inlet = (
    base.faces("<Z").first()
    .workplane()
    .circle(inlet_radius)
    .cutBlind(-wall_thickness)
    .faces("<Z").first()
    .edges()
    .chamfer(inlet_chamfer)
)

flow_cutter = (
    cq.Workplane("YZ")
    .center(0, flow_port_z)
    .circle(flow_port_radius)
    .extrude(body_outer_radius * 2)
)

with_flow = with_inlet.cut(flow_cutter)

with_pocket = (
    with_flow.faces(">Z").first()
    .workplane()
    .circle(pocket_radius)
    .cutBlind(-pocket_depth)
)

mount_cutter = (
    cq.Workplane("YZ")
    .pushPoints([(-mount_spacing/2, 0), (mount_spacing/2, 0)])
    .circle(mount_hole_radius)
    .extrude(body_outer_radius * 2)
)

with_mounts = with_pocket.cut(mount_cutter)

rib = (
    cq.Workplane("YZ")
    .transformed(offset=(body_outer_radius - rib_thickness/2, 0, 0))
    .center(0, rib_z)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

result = with_mounts.union(rib)
