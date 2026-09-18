import cadquery as cq

# Parameters
base_radius = 30.0
tip_radius = 2.0
total_length = 80.0
step_height = 10.0
radius_decrement = (base_radius - tip_radius) / (total_length / step_height)
chamfer_distance = 0.5
hole_diameter = 5.0
hole_offset = 15.0
flange_thickness = 5.0
flange_radius = base_radius + 5.0

# Initial loft between base and first step
first_radius = base_radius - radius_decrement
result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=step_height)
    .circle(first_radius)
    .loft(combine=True)
)

current_radius = first_radius
current_height = step_height
while current_height < total_length - step_height:
    next_radius = current_radius - radius_decrement
    result = (
        result.faces(">Z")
        .workplane()
        .circle(current_radius)
        .workplane(offset=step_height)
        .circle(next_radius)
        .loft(combine=True)
    )
    current_radius = next_radius
    current_height += step_height

# Add mounting flange at base
flange = (
    cq.Workplane("XY")
    .polygon(6, flange_radius * 2)
    .extrude(flange_thickness)
)
result = result.union(flange)

# Add side mounting holes (two opposite)
hole_cyl = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2)
    .extrude(total_length + flange_thickness)
)
hole1 = hole_cyl.translate((hole_offset, 0, 0))
hole2 = hole_cyl.translate((-hole_offset, 0, 0))
result = result.cut(hole1).cut(hole2)

# Apply chamfer to all edges
result = result.edges().chamfer(chamfer_distance)
