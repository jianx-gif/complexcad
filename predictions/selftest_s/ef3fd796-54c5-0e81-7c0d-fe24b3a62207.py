import cadquery as cq

pipe_outer_radius = 5.0
pipe_thickness = 1.0
elbow_center_radius = 20.0
pipe_inner_radius = pipe_outer_radius - pipe_thickness
gusset_thickness = 2.0
gusset_width = 15.0
gusset_length = 30.0
fillet_radius = 0.5
chamfer_distance = 0.3
hole_diameter = 2.0
hole_count = int(gusset_width // (hole_diameter*2))
hole_pitch = gusset_width / (hole_count + 1) if hole_count > 0 else gusset_width

profile = (
    cq.Workplane("XZ")
    .circle(pipe_outer_radius)
    .circle(pipe_inner_radius)
    .wire()
)

path = (
    cq.Workplane("XY")
    .moveTo(elbow_center_radius, 0)
    .threePointArc((-elbow_center_radius, 0), (0, elbow_center_radius))
    .wire()
)

pipe_elbow = path.sweep(profile)

gusset_base = (
    cq.Workplane("XY")
    .center(elbow_center_radius + pipe_outer_radius, 0)
    .rect(gusset_width, gusset_length)
    .extrude(gusset_thickness)
)

combined = pipe_elbow.union(gusset_base)

result = (
    combined
    .edges("|Z")
    .fillet(fillet_radius)
    .edges("|Y")
    .chamfer(chamfer_distance)
)

if hole_count > 0:
    points = [(i * hole_pitch - gusset_width/2) for i in range(1, hole_count+1)]
    result = (
        result
        .faces(">X")
        .workplane()
        .pushPoints([(x, 0) for x in points])
        .hole(hole_diameter)
    )
