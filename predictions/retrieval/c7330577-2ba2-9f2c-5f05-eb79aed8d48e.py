import cadquery as cq

outer_diameter = 60
wall_thickness = 5
sleeve_length = 40
base_thickness = 8
base_diameter = 70
thread_pitch = 4
thread_depth = 2
slot_width = 8
slot_height = wall_thickness + 1
slot_length = sleeve_length - 10
chamfer_size = 1
mounting_hole_dia = 5
mounting_hole_radius = (base_diameter / 2) - 12

outer_radius = outer_diameter / 2
inner_radius = outer_radius - wall_thickness
base_radius = base_diameter / 2

profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (0, base_thickness),
        (outer_radius, base_thickness),
        (outer_radius, base_thickness + sleeve_length),
        (inner_radius, base_thickness + sleeve_length),
        (inner_radius, base_thickness),
        (0, base_thickness),
    ])
    .close()
)
body = profile.revolve()
body = body.chamfer(chamfer_size)

thread_profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (thread_depth, thread_depth / 2),
        (0, thread_depth),
    ])
    .close()
)
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=sleeve_length, radius=inner_radius - thread_depth / 2)
thread_path = helix_wire.translate((0, 0, base_thickness))
thread_solid = thread_profile.sweep(thread_path)
body = body.cut(thread_solid)

slot_center_z = base_thickness + sleeve_length / 2
slot = (
    cq.Workplane("XZ")
    .center(0, slot_center_z)
    .rect(slot_width, slot_length)
    .extrude(slot_height * 2)
    .translate((outer_radius - slot_height, 0, 0))
)
slot2 = slot.rotate((0, 0, 0), (0, 0, 1), 90)
body = body.cut(slot)
body = body.cut(slot2)

mounting_points = [
    (mounting_hole_radius, 0),
    (-mounting_hole_radius, 0),
    (0, mounting_hole_radius),
    (0, -mounting_hole_radius),
]
body = (
    body.faces("<Z")
    .workplane()
    .pushPoints(mounting_points)
    .hole(mounting_hole_dia)
)

result = body