import cadquery as cq

base_width = 80.0
base_height = 50.0
base_thickness = 8.0
central_bore_diameter = 12.0
counterbore_diameter = 20.0
counterbore_depth = 4.0
mount_hole_diameter = 5.0
mount_hole_offset_x = 15.0
mount_hole_offset_y = 15.0
rib_thickness = 6.0
rib_height = 20.0
rib_spacing = 30.0
chamfer_size = 1.0
fillet_radius = 2.0
notch_width = 6.0
notch_height = 20.0

base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)

base = (
    base
    .faces("<X")
    .workplane()
    .rect(notch_width, notch_height)
    .cutBlind(-base_thickness)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .hole(counterbore_diameter, depth=counterbore_depth)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .hole(central_bore_diameter)
)

mount_pts = [
    (-base_width/2 + mount_hole_offset_x, -base_height/2 + mount_hole_offset_y),
    ( base_width/2 - mount_hole_offset_x, -base_height/2 + mount_hole_offset_y),
    (-base_width/2 + mount_hole_offset_x,  base_height/2 - mount_hole_offset_y),
    ( base_width/2 - mount_hole_offset_x,  base_height/2 - mount_hole_offset_y)
]
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(mount_pts)
    .hole(mount_hole_diameter)
)

rib_positions = [(-rib_spacing/2, 0), (rib_spacing/2, 0)]
ribs = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .pushPoints(rib_positions)
    .rect(rib_thickness, base_height - 20)
    .extrude(rib_height)
)

result = base.union(ribs)

result = result.edges("|Z").chamfer(chamfer_size)
