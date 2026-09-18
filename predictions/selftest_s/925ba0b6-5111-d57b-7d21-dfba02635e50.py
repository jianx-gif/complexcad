import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    clip_height=30.0,
    arm_thickness=4.0,
    flange_radius=12.0,
    flange_thickness=3.0,
    base_radius=6.0,
    chamfer=0.6,
    hole=Measures(
        diameter=3.0,
        cbore_diameter=5.5,
        cbore_depth=2.5,
    ),
    slot=Measures(
        width=6.0,
        depth=3.0,
    ),
)

profile = (
    cq.Workplane("XZ")
    .moveTo(params.base_radius, 0)
    .lineTo(params.base_radius, params.clip_height - params.flange_thickness)
    .lineTo(params.base_radius + params.arm_thickness, params.clip_height - params.flange_thickness)
    .lineTo(params.base_radius + params.arm_thickness, params.clip_height)
    .threePointArc((params.flange_radius, params.clip_height + params.flange_thickness/2), (params.flange_radius, params.clip_height + params.flange_thickness))
    .lineTo(params.base_radius, params.clip_height + params.flange_thickness)
    .close()
)

solid = profile.revolve()

solid = (
    solid
    .faces(">Z").workplane()
    .polarArray(radius=params.flange_radius - params.flange_thickness/2, count=2, startAngle=0, angle=360)
    .cboreHole(params.hole.diameter, params.hole.cbore_diameter, params.hole.cbore_depth)
)

slot_center_x = params.base_radius + params.arm_thickness/2
solid = (
    solid
    .faces(">Y").workplane()
    .center(slot_center_x, 0)
    .rect(params.slot.width, params.slot.depth)
    .cutBlind(-params.slot.depth)
)

result = solid.edges("|Z").chamfer(params.chamfer)
