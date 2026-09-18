import cadquery as cq

# Parameters
base_width = 80.0  # overall width (max 100)
base_length = 60.0  # overall length
spacer_thickness = 8.0  # thickness of the spacer
corner_radius = 4.0  # radius for top edge fillets
central_hole_diameter = 20.0  # clearance hole diameter
slot_width = 6.0  # width of each blind slot
slot_length = 15.0  # length of each blind slot
slot_depth = 4.0  # blind depth (partial through)
slot_spacing_x = 20.0  # spacing between slot centers in X
slot_spacing_y = 20.0  # spacing between slot centers in Y
num_slots_x = 3  # number of slots along X
num_slots_y = 2  # number of slots along Y
chamfer_distance = 1.0  # small chamfer on outer edges

# Base plate extruded
base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(spacer_thickness)
    # Fillet vertical edges for structural strength
    .edges("|Z")
    .fillet(corner_radius)
    # Chamfer outer top edges for safety
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)

# Add central clearance hole and patterned blind slots
result = (
    base
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
    # Create a grid of blind slots
    .rarray(slot_spacing_x, slot_spacing_y, num_slots_x, num_slots_y)
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)

# Validate geometry (no export)
result