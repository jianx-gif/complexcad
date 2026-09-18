import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
housing_length = 100.0
inlet_thread_diameter = 30.0
outlet_thread_pitch = 4.0
outlet_thread_length = 30.0
outlet_thread_pitch = inlet_thread_pitch / 2.0
chamfer_size = 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inlet_thread_diameter / 2.0
housing_radius = inlet_thread_pitch / 2.0
housing_radius = housing_radius - wall_thickness
housing_radius = housing_radius - wall_thickness
housing_radius = housing_radius - housing_radius
result = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, housing_radius)
    .lineTo(housing_radius, housing_radius)
    .lineTo(housing_radius, housing_radius + housing_radius)
    .lineTo(housing_radius + housing_radius, housing_radius + housing_radius)
    .lineTo(housing_radius + housing_radius, housing_radius + housing_radius)
    .lineTo(housing_radius, housing_radius + housing_radius)
    .lineTo(housing_radius, housing_radius)
    .lineTo(housing_radius, 0)
    .close()
    .revolve()
    .shell(-wall_thickness)
    .edges()
    .chamfer(chamfer_size)
)
