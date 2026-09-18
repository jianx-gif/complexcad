import cadquery as cq

# Parameters
body_length = 80.0
outer_diameter = 40.0
inner_diameter = 20.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
inlet_diameter = 22.0
inlet_length = 15.0
outlet_diameter = 18.0
outlet_length = 12.0
chamfer_size = 1.0
hole_diameter = 6.0
hole_spacing_x = 20.0
hole_spacing_y = 10.0
hole_rows = 2
hole_cols = 3
rib_width = 8.0
rib_height = 4.0
rib_length = 20.0
rib_offset = 10.0

# Base body cylinder
body = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(body_length)
)

# Central bore
bore = (
    cq.Workplane("XY")
    .circle(inner_diameter / 2.0)
    .extrude(body_length)
)
body = body.cut(bore)

# Inlet port (cut from front face)
inlet = (
    cq.Workplane("XY")
    .circle(inlet_diameter / 2.0)
    .extrude(inlet_length)
)
body = body.cut(inlet)

# Outlet port (cut from back face)
outlet = (
    cq.Workplane("XY")
    .circle(outlet_diameter / 2.0)
    .extrude(outlet_length)
    .translate((0, 0, body_length - outlet_length))
)
body = body.cut(outlet)

# Chamfer on inlet and outlet edges
body = body.edges("<<Z").chamfer(chamfer_size)

# Patterned through holes on top face
body = (
    body.faces(">Z")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)

# External rib for stiffness (attached to side)
rib = (
    cq.Workplane("YZ")
    .rect(rib_height, rib_length)
    .extrude(rib_width)
    .translate((outer_diameter / 2.0 - rib_width / 2.0, 0, body_length / 2.0))
)
body = body.union(rib)

result = body