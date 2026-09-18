import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
tube_length = 70.0
tube_diameter = outer_diameter - 2 * wall_thickness
tube_diameter = tube_diameter - 2 * wall_thickness
hole_diameter = 4.0
hole_count = 6
hole_spacing = (outer_diameter - 2 * hole_diameter) / (hole_count - 1)
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, tube_length)
    .lineTo(tube_diameter/2, tube_length)
    .lineTo(tube_diameter/2, tube_length + tube_length)
    .lineTo(0, tube_length + tube_length)
    .close()
)
tube = profile.revolve()
tube = tube.edges().chamfer(chamfer_distance)
tube = tube.edges().chamfer(chamfer_distance)
tube = (
    tube.faces(">Z")
    .workplane()
    .circle(hole_diameter/2)
    .cutBlind(-tube_length)
)
tube = tube.edges().chamfer(chamfer_distance)
result = tube
