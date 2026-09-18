import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        vertical_block = (
            cq.Workplane('XY')
            .box(m.vertical_width, m.vertical_length, m.vertical_thickness)
            .translate((m.vertical_width/2, m.vertical_length/2, m.vertical_thickness/2))
        )
        horiz_near = (
            cq.Workplane('XY')
            .box(m.step_position, m.horizontal_width, m.vertical_thickness)
            .translate((m.vertical_width + m.step_position/2, m.horizontal_width/2, m.vertical_thickness/2))
        )
        horiz_far = (
            cq.Workplane('XY')
            .box(m.horizontal_length - m.step_position, m.horizontal_width, m.horizontal_thick_far)
            .translate((m.vertical_width + m.step_position + (m.horizontal_length - m.step_position)/2, m.horizontal_width/2, m.horizontal_thick_far/2))
        )
        base = vertical_block.union(horiz_near).union(horiz_far)
        # Add mounting holes on vertical arm
        base = (
            base.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .pushPoints([(m.vertical_width/2, y) for y in m.hole_positions])
            .hole(m.mount_hole_diameter)
        )
        # Add slot on far horizontal segment
        base = (
            base.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .rect(m.slot_length, m.slot_width)
            .cutBlind(m.slot_depth)
        )
        # Add ribs on underside (bottom face)
        rib = (
            cq.Workplane('XY')
            .rect(m.rib_width, m.rib_length)
            .extrude(m.rib_thickness)
            .translate((m.rib_center_x, m.rib_center_y, m.rib_thickness/2))
        )
        base = base.union(rib)
        # Chamfer outer edges
        base = base.edges('|Z').chamfer(m.chamfer)
        self.model = base

measures = Measures(
    vertical_width=20.0,
    vertical_length=70.0,
    vertical_thickness=8.0,
    horizontal_width=20.0,
    step_position=40.0,
    horizontal_length=90.0,
    horizontal_thick_far=12.0,
    mount_hole_diameter=5.0,
    hole_positions=[20.0, 35.0, 50.0],
    slot_length=30.0,
    slot_width=5.0,
    slot_depth=6.0,
    rib_width=4.0,
    rib_length=60.0,
    rib_thickness=2.0,
    rib_center_x=30.0,
    rib_center_y=35.0,
    chamfer=0.5,
)

result = LBracket(cq.Workplane('XY'), measures).model