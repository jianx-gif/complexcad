import cadquery as cq

base_length = 80.0
base_width = 60.0
base_thickness = 10.0
fin_height = 5.0
fin_thickness = 2.0
fin_spacing = 3.0
chamfer_distance = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
pocket_length = base_length * 0.4
pocket_width = base_width * 0.6
pocket_depth = base_thickness * 0.5

# Base with central boss
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .circle(base_length * 0.2)
    .extrude(base_thickness)
)

# Pocket subtraction
pocket = (
    cq.Workplane("XY")
    .rect(pocket_length, pocket_width)
    .extrude(pocket_depth)
    .translate((0, 0, base_thickness - pocket_depth))
)
base = base.cut(pocket)

# Number of fins
num_fins = int((base_width - fin_spacing) // (fin_thickness + fin_spacing))

# Single fin prototype
single_fin = (
    cq.Workplane("XY")
    .rect(base_length, fin_thickness)
    .extrude(fin_height)
    .translate((0, 0, base_thickness))
)

# Array fins
offset_y = -base_width/2 + fin_spacing + fin_thickness/2
fins = (
    single_fin.rarray(xSpacing=0, ySpacing=fin_thickness + fin_spacing, xCount=1, yCount=num_fins)
    .translate((0, offset_y, 0))
)

# Combine base and fins into a single solid
result = cq.Workplane().add(base).add(fins).combine()

# Chamfer top edges for airflow guidance
result = result.faces(">Z").edges().chamfer(chamfer_distance)

# Mounting holes on bottom surface
mount_positions = [
    (-mount_hole_spacing/2, -mount_hole_spacing/2),
    (mount_hole_spacing/2, -mount_hole_spacing/2),
    (mount_hole_spacing/2, mount_hole_spacing/2),
    (-mount_hole_spacing/2, mount_hole_spacing/2)
]
result = result.faces("<Z").workplane().pushPoints(mount_positions).hole(mount_hole_dia)
