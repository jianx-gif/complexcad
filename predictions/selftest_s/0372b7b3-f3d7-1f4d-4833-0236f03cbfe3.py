import cadquery as cq

outer_diameter = 80
wall_thickness = 5
housing_length = 100
inlet_thread_diameter = 30
inlet_thread_pitch = 4
inlet_thread_length = 30
outlet_diameter = 40
chamfer_size = 2

# profile points
r_outer = outer_diameter/2
r_inlet = inlet_thread_diameter/2

# Build 2D profile on XZ plane
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, housing_length)
    .lineTo(r_outer, housing_length)
    .threePointArc((r_outer+10, housing_length-10), (r_outer+10, housing_length-20))
    .lineTo(r_outer+10, inlet_thread_length)
    .lineTo(r_inlet, inlet_thread_length)
    .lineTo(r_inlet, 0)
    .close()
)
solid = profile.revolve()

# shell
shelled = solid.shell(wall_thickness)

# chamfer outlet top edge
result = shelled.faces("+Z").chamfer(chamfer_size)
