import cadquery as cq

jaw_width = 80.0
jaw_height = 30.0
jaw_thickness = 10.0
hole_diameter = 5.0
hole_spacing = 20.0
num_holes = 3
undercut_depth = 5.0
undercut_offset = 10.0
rib_width = 5.0
rib_height = 20.0
rib_thickness = jaw_thickness / 2.0
chamfer_distance = 1.0

base = (
    cq.Workplane("XY")
    .rect(jaw_width, jaw_height)
    .extrude(jaw_thickness)
)

rib = (
    base.faces(">Y")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

combined = base.union(rib)

undercut = (
    combined.faces("<Z")
    .workplane(invert=True)
    .rect(jaw_width - 2 * undercut_offset, jaw_height - 2 * undercut_offset)
    .cutBlind(-undercut_depth)
)

chamfered = (
    undercut.faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)

result = (
    chamfered.faces(">Z")
    .workplane()
    .center(-jaw_width / 2 + hole_spacing, 0)
    .rarray(hole_spacing * 2, 0, num_holes, 1)
    .hole(hole_diameter)
)
