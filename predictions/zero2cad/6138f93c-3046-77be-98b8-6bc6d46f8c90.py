import cadquery as cq

# Parameters
base_radius = 20.0
top_width = 50.0
top_length = 40.0
total_height = 80.0
step_height = 10.0
counterbore_diameter = 6.0
counterbore_depth = 3.0
through_hole_diameter = 3.0
chamfer_size = 0.5
rib_thickness = 2.0
rib_height = 15.0
rib_spacing = 20.0

# Build lofted body
wp = cq.Workplane("XY").circle(base_radius)
current_z = step_height
while current_z <= total_height:
    t = current_z / total_height
    width = base_radius * 2 * (1 - t) + top_width * t
    length = base_radius * 2 * (1 - t) + top_length * t
    wp = wp.workplane(offset=step_height).rect(width, length)
    current_z += step_height
result = wp.loft(combine=True)

# Counterbore on top face
result = result.faces(">Z").workplane().cboreHole(through_hole_diameter, counterbore_diameter, counterbore_depth)

# Add ribs on one side
rib = (
    cq.Workplane("YZ")
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
# Position ribs along the side
num_ribs = int(total_height / rib_spacing)
for i in range(num_ribs):
    z_pos = i * rib_spacing + rib_spacing/2
    result = result.union(
        rib.translate((-(top_width/2 + rib_thickness/2), 0, z_pos))
    )

# Chamfer top edges
result = result.edges(">Z").chamfer(chamfer_size)
