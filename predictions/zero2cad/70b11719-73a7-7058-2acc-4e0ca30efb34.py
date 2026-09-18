import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
shoulder_length = 30.0
shoulder_height = 15.0
hole_diameter = 4.5
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_size = 1.0
rib_thickness = 4.0
rib_height = 6.0
rib_spacing = 20.0

base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_length)
    .extrude(bracket_thickness)
)

shoulder = (
    cq.Workplane("XY")
    .center(0, bracket_length/2 - shoulder_length/2)
    .rect(bracket_width, shoulder_length)
    .extrude(shoulder_height)
)

bracket = base.union(shoulder)

hole_positions = [
    (0, bracket_length/2 - hole_offset_from_end - i*hole_spacing) for i in range(3)
]

for x, y in hole_positions:
    bracket = (
        bracket
        .faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .hole(hole_diameter)
    )

rib_count = int((bracket_length - 2*hole_offset_from_end) // rib_spacing) + 1
for i in range(rib_count):
    y_pos = -bracket_length/2 + hole_offset_from_end + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(0, y_pos)
        .rect(rib_thickness, rib_height)
        .extrude(bracket_thickness)
    )
    bracket = bracket.union(rib)

bracket = bracket.edges("|Z").chamfer(chamfer_size)

result = bracket