import cadquery as cq
from types import SimpleNamespace as Measures

leg_length = 80.0
leg_width = 60.0
thickness = 10.0
cutout_length = 30.0
cutout_width = 30.0
chamfer_distance = 6.0
central_hole_diameter = 8.0
mount_hole_diameter = 5.0
mount_hole_spacing = 20.0
mount_hole_edge_offset = 10.0
rib_height = 5.0
rib_thickness = 5.0
rib_spacing = 15.0

measures = Measures(
    leg_length=leg_length,
    leg_width=leg_width,
    thickness=thickness,
    cutout_length=cutout_length,
    cutout_width=cutout_width,
    chamfer_distance=chamfer_distance,
    central_hole_diameter=central_hole_diameter,
    mount_hole_diameter=mount_hole_diameter,
    mount_hole_spacing=mount_hole_spacing,
    mount_hole_edge_offset=mount_hole_edge_offset,
    rib_height=rib_height,
    rib_thickness=rib_thickness,
    rib_spacing=rib_spacing,
)

class LBracket:
    def __init__(self, workplane, m):
        self.workplane = workplane
        self.m = m
        self.model = None
        self.build()

    def build(self):
        m = self.m
        profile = (
            cq.Workplane("XY")
            .moveTo(0, 0)
            .lineTo(m.leg_length, 0)
            .lineTo(m.leg_length, m.leg_width)
            .lineTo(m.cutout_length, m.leg_width)
            .lineTo(m.cutout_length, m.cutout_width)
            .lineTo(0, m.cutout_width)
            .close()
        )
        solid = profile.extrude(m.thickness)
        solid = solid.edges("|Z").chamfer(m.chamfer_distance)
        hole_x = m.leg_length / 2
        hole_y = m.leg_width / 2
        solid = (
            solid.faces(">Z")
            .workplane()
            .center(hole_x - m.leg_length/2, hole_y - m.leg_width/2)
            .hole(m.central_hole_diameter)
        )
        num_holes_long = int((m.leg_length - 2*m.mount_hole_edge_offset) / m.mount_hole_spacing) + 1
        for i in range(num_holes_long):
            x = m.mount_hole_edge_offset + i*m.mount_hole_spacing
            solid = (
                solid.faces(">Z")
                .workplane()
                .center(x - m.leg_length/2, -m.leg_width/2 + m.mount_hole_edge_offset)
                .hole(m.mount_hole_diameter)
            )
        num_holes_short = int((m.leg_width - 2*m.mount_hole_edge_offset) / m.mount_hole_spacing) + 1
        for i in range(num_holes_short):
            y = m.mount_hole_edge_offset + i*m.mount_hole_spacing
            solid = (
                solid.faces(">Z")
                .workplane()
                .center(-m.leg_length/2 + m.mount_hole_edge_offset, y - m.leg_width/2)
                .hole(m.mount_hole_diameter)
            )
        rib_positions = []
        start = m.cutout_length + m.rib_spacing
        x = start
        while x < m.leg_length - m.rib_spacing:
            rib_positions.append(x)
            x += m.rib_spacing
        for rib_x in rib_positions:
            rib = (
                cq.Workplane("XY")
                .center(rib_x - m.leg_length/2, m.leg_width/2)
                .rect(m.rib_thickness, m.rib_height)
                .extrude(m.thickness)
            )
            solid = solid.union(rib)
        self.model = solid

result = LBracket(cq.Workplane("XY"), measures).model
