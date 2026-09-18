import cadquery as cq

plate_width = 80
plate_depth = 80
plate_thickness = 5
central_aperture_diameter = 30
slot_length = 50
slot_width = 12
slot_offset = 20
hole_diameter = 6
hole_pitch = 20
chamfer_size = 1

# base plate from sketch
base = (
    cq.Workplane('XY')
    .sketch()
    .rect(plate_width, plate_depth)
    .finalize()
    .extrude(plate_thickness)
)

# apply chamfer to vertical edges
base = base.edges('|Z').chamfer(chamfer_size)

# add central aperture
base = base.faces('>Z').workplane().hole(central_aperture_diameter)

# add dual slots
for offset in (-slot_offset, slot_offset):
    base = base.faces('>Z').workplane().center(offset, 0).slot2D(slot_length, slot_width/2, 0).cutThruAll()

# add 4x4 hole matrix
base = base.faces('>Z').workplane().rarray(hole_pitch, hole_pitch, 4, 4, True).hole(hole_diameter)

result = base
