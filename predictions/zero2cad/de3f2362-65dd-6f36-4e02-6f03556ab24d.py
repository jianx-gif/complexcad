import cadquery as cq

# Parameters
total_length = 80.0
inlet_diameter = 20.0
outlet_width = 50.0
outlet_height = 30.0
step_count = 6
step_height = total_length / step_count
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
slot_width = 5.0
slot_height = 20.0
slot_depth = 10.0

# Build lofted body
builder = cq.Workplane("XY").circle(inlet_diameter / 2)
for i in range(1, step_count + 1):
    t = i / step_count
    width = inlet_diameter + (outlet_width - inlet_diameter) * t
    height = inlet_diameter + (outlet_height - inlet_diameter) * t
    builder = builder.workplane(offset=step_height).rect(width, height)
result = builder.loft(combine=True)

# Add mounting holes on top face
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-mount_hole_spacing / 2, -mount_hole_spacing / 2),
        (mount_hole_spacing / 2, -mount_hole_spacing / 2),
        (-mount_hole_spacing / 2, mount_hole_spacing / 2),
        (mount_hole_spacing / 2, mount_hole_spacing / 2),
    ])
    .hole(mount_hole_diameter)
)

# Add side slot for cable routing
result = (
    result.faces(">X")
    .workplane(centerOption="CenterOfMass")
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)

# Apply chamfer to top edges
result = result.faces(">Z").edges().chamfer(chamfer_distance)
