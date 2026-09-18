import cadquery as cq

# Parameters
height_vert = 40.0
length_horiz = 30.0
thickness = 10.0
pocket_width = 20.0
pocket_depth = 6.0
hole_diameter = 8.0
fillet_radius = 2.0

class RevolvedLBracket:
    def __init__(self):
        self.build()
    def build(self):
        base = (
            cq.Workplane("YZ")
            .moveTo(0, 0)
            .lineTo(thickness, 0)
            .lineTo(thickness, height_vert)
            .lineTo(thickness + length_horiz, height_vert)
            .lineTo(thickness + length_horiz, height_vert + thickness)
            .lineTo(0, height_vert + thickness)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0))
        )
        filleted = base.edges().fillet(fillet_radius)
        pocket_box = (
            cq.Workplane("XY")
            .box(pocket_depth, pocket_width, thickness)
            .translate((thickness + length_horiz - pocket_depth/2, height_vert + thickness/2, 0))
        )
        with_pocket = filleted.cut(pocket_box)
        hole_cyl = (
            cq.Workplane("YZ")
            .circle(hole_diameter/2)
            .extrude(thickness*2)
            .translate((thickness/2, height_vert/2, 0))
        )
        final = with_pocket.cut(hole_cyl)
        self.model = final

result = RevolvedLBracket().model
