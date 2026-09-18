import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    base_height = 10.0,
    base_radius = 8.0,
    cam_radius = 15.0,
    cam_height = 12.0,
    hub_radius = 5.0,
    bolt_hole_diameter = 4.0,
    chamfer = 0.8,
    slot_width = 8.0,
    slot_height = 4.0,
    slot_depth = 5.0
)

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, measures.base_height)
    .lineTo(measures.base_radius, measures.base_height)
    .threePointArc((measures.cam_radius, measures.base_height + measures.cam_height/2), (measures.cam_radius, measures.base_height + measures.cam_height))
    .lineTo(0, measures.base_height + measures.cam_height)
    .close()
)

lever = profile.revolve()
lever = lever.faces(">Z").workplane().hole(measures.bolt_hole_diameter)
lever = lever.edges().chamfer(measures.chamfer)
lever = lever.faces(">Z").workplane().rect(measures.slot_width, measures.slot_height).cutBlind(-measures.slot_depth)

result = lever
