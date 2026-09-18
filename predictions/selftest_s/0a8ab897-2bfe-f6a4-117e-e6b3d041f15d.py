import cadquery as cq
import math
jaw_length = 80.0
jaw_height = 20.0
jaw_thickness = 5.0
chamfer_angle_deg = 30.0
chamfer_distance = jaw_thickness * math.tan(math.radians(chamfer_angle_deg))
hole_diameter = 5.5
hole_spacing_x = 60.0
hole_spacing_y = 10.0
hole_offset_x = (jaw_length - hole_spacing_x) / 2.0
hole_offset_y = (jaw_height - hole_spacing_y) / 2.0
hole_positions = [
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, hole_offset_y),
]
slot_width = 8.0
slot_length = jaw_length * 0.6
rib_height = 5.0
rib_thickness = 2.0
result = (
    cq.Workplane("XY")
    .sketch()
    .rect(jaw_length, jaw_height)
    .rect(slot_width, slot_length, mode="s")
    .finalize()
    .extrude(jaw_thickness)
    .faces(">Z").edges("|X").chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .faces("<Z")
    .workplane()
    .sketch()
    .rect(jaw_length * 0.6, rib_height)
    .finalize()
    .extrude(rib_thickness)
)
