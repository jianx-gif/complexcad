
import cadquery as cq

vertical_height = 70.0
vertical_width = 40.0
vertical_thickness = 10.0
horizontal_length = 60.0
horizontal_thickness = 10.0
draft_angle = 5.0
gusset_height = 20.0
gusset_thickness = 5.0
hole_diameter = 5.0
countersink_diameter = 8.0
hole_depth = 4.0
hole_edge_margin = 10.0
fillet_radius = 0.2
num_holes = 5

class BracketL:
    def __init__(self):
        self.model = None
        self.build()
    def build(self):
        vertical = (
            cq.Workplane("XY")
            .rect(vertical_width, vertical_thickness)
            .extrude(vertical_height)
        )
        horizontal = (
            vertical.faces(">X")
            .workplane(centerOption='CenterOfBoundBox')
            .rect(vertical_thickness, horizontal_length)
            .extrude(horizontal_thickness, taper=-draft_angle)
        )
        base = vertical.union(horizontal)
        gusset = (
            cq.Workplane("YZ")
            .polyline([(0, 0), (0, gusset_height), (gusset_thickness, 0)])
            .close()
            .extrude(gusset_thickness)
            .translate((-vertical_width/2, 0, 0))
        )
        combined = base.union(gusset)
        spacing = (vertical_height - 2*hole_edge_margin) / (num_holes - 1)
        points = [(0, hole_edge_margin + i*spacing) for i in range(num_holes)]
        drilled = (
            combined.faces(">Y")
            .workplane(centerOption='CenterOfBoundBox')
            .pushPoints(points)
            .cboreHole(hole_diameter, countersink_diameter, hole_depth)
        )
        self.model = drilled.edges().first().fillet(fillet_radius)

result = BracketL().model
