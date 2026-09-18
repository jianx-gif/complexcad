import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0
dome_radius = 20.0
hole_diameter = 5.0
hole_grid_spacing_x = 15.0
hole_grid_spacing_y = 15.0
mount_tab_length = 20.0
mount_tab_width = 10.0
mount_tab_offset = 5.0
rim_chamfer = 1.0
base_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .translate((0, 0, plate_thickness/2))
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
mount_holes = (
    base_plate
    .faces(">Z")
    .workplane()
    .center(0, mount_tab_offset)
    .rect(mount_tab_length, mount_tab_width)
    .cutBlind(-mount_tab_thickness)
)
result = base_plate
