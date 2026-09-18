import cadquery as cq
plate_width = 80.0
plate_depth = 80.0
plate_thickness = 5.0
central_aperture_diameter = 30.0
hole_diameter = 6.0
slot_length = 50.0
slot_width = 12.0
slot_offset = 20.0
chamfer_size = 1.0
hole_pitch = 20.0
hole_diameter = 6.0
hole_count = 6
hole_spacing = (plate_width - 2 * hole_pitch) / (hole_count - 1)
hole_positions = [(0, 0), (plate_width / 2 - hole_pitch) for i in range(hole_count)]
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-plate_thickness)
)
