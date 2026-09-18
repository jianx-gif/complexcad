import cadquery as cq
base_width = 80.0
base_depth = 40.0
base_thickness = 6.0
edge_chamfer = 1.0
socket_width = 30.0
socket_height = 12.0
socket_depth = 30.0
hole_diameter = 5.0
hole_offset_x = 15.0
hole_offset_y = 10.0
hole_spacing_x = 30.0
hole_spacing_y = 15.0
rib_height = 4.0
rib_width = 30.0
rib_depth = 15.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (base_width, 0),
        (base_width, base_depth),
        (base_width + rib_width, base_depth),
        (base_width + rib_width, base_depth + rib_height),
        (base_width, base_depth + rib_height),
        (base_width, base_depth + rib_height),
        (base_width, base_depth + rib_height),
        (base_width, 0),
        (base_width, 0)
    ])
    .close()
    .extrude(base_thickness)
)
socket = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (socket_width, 0),
        (socket_width, socket_depth),
        (socket_width + rib_width, socket_depth),
        (socket_width + rib_width, socket_depth + rib_height),
        (socket_width + rib_width, socket_depth + rib_height),
        (socket_width, socket_depth + rib_height),
        (socket_width, socket_depth),
        (0, socket_depth),
    ])
    .close()
    .extrude(base_thickness)
)
result = base.union(socket)
result = result.edges("|Z").chamfer(edge_chamfer)
