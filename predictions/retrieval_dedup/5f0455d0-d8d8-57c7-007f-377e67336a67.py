
import cadquery as cq

handle_length = 80.0
handle_width = 30.0
handle_height = 30.0
handle_fillet_radius = 5.0
snap_beam_thickness = 4.0
snap_beam_height = 10.0
snap_beam_length = 20.0
through_hole_diameter = 6.0
chamfer_distance = 1.0

base = cq.Workplane("XY").box(handle_length, handle_width, handle_height)
base = base.edges().fillet(handle_fillet_radius)

beam = (
    base.faces("<X")
    .workplane()
    .rect(snap_beam_thickness, snap_beam_height)
    .extrude(snap_beam_length)
)

combined = base.union(beam)

result = (
    combined
    .faces("<X")
    .workplane()
    .hole(through_hole_diameter)
)

result = result.edges("|X").chamfer(chamfer_distance)
