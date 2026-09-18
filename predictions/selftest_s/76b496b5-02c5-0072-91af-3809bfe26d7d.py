import cadquery as cq

horizontal_length = 70.0
vertical_length = 80.0
leg_thickness = 12.0
bracket_depth = 10.0
rib_width = 6.0
rib_height = 8.0
rib_depth = 4.0
rib_spacing = 15.0
rib_count = 3
hole_diameter = 5.0
hole_spacing_x = 20.0
hole_spacing_y = 25.0
hole_rows = 2
hole_cols = 3
chamfer_size = 1.0

class LBracket:
    def __init__(self, wp):
        self.wp = wp
        self.build()
    def build(self):
        pts = [
            (0, 0),
            (horizontal_length, 0),
            (horizontal_length, leg_thickness),
            (leg_thickness, leg_thickness),
            (leg_thickness, vertical_length + leg_thickness),
            (0, vertical_length + leg_thickness)
        ]
        base = (
            self.wp
            .polyline(pts)
            .close()
            .extrude(bracket_depth)
        )
        ribs = (
            base
            .faces(">X")
            .workplane(centerOption='CenterOfBoundBox')
            .moveTo(leg_thickness/2 + rib_depth/2, rib_height/2)
            .rect(rib_width, rib_height)
            .rarray(0, rib_spacing, 1, rib_count)
            .extrude(rib_depth)
        )
        holes = (
            ribs
            .faces(">Z")
            .workplane(centerOption='CenterOfBoundBox')
            .moveTo(
                horizontal_length/2 - (hole_spacing_x*(hole_cols-1))/2,
                leg_thickness/2
            )
            .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
            .hole(hole_diameter)
        )
        final = (
            holes
            .faces(">Z")
            .edges()
            .chamfer(chamfer_size)
        )
        self.model = final

result = LBracket(cq.Workplane("XY")).model
