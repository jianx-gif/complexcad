import cadquery as cq
total_height = 80.0
base_width = 20.0
base_thickness = 10.0
base_width = 90.0
lattice_pitch = 12.0
lattice_bar_thickness = 2.0
chamfer_distance = 0.5
base_width = base_width - 2 * lattice_pitch
base_width = base_width - 2 * lattice_pitch
base_thickness = base_thickness
base_height = total_height - base_width
base_width = base_width - 2 * lattice_pitch
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
base = base.edges().chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .center(base_width/2 - lattice_bar_thickness/2, base_height/2)
    .rect(base_width, base_height)
    .cutBlind(base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(base_width/2 - lattice_bar_thickness/2, base_height/2)
    .rect(lattice_bar_thickness, lattice_bar_thickness)
    .extrude(base_thickness)
)
base = base.union(base)
base = base.edges().chamfer(chamfer_distance)
result = base
