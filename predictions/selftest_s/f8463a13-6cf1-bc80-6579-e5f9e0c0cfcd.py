import cadquery as cq
from types import SimpleNamespace as Measures

# Define parameters
total_height = 60.0  # mm (max 100)
outer_radius_bottom = 30.0
outer_radius_top = 20.0  # taper
wall_thickness = 4.0
valve_cut_radius = 12.0
valve_cut_depth = 8.0
bolt_hole_dia = 5.0
bolt_head_dia = 9.0
bolt_head_angle = 90  # degrees for countersink
bolt_pattern_radius = 22.0
chamfer_size = 1.0

measures = Measures(
    total_height=total_height,
    outer_radius_bottom=outer_radius_bottom,
    outer_radius_top=outer_radius_top,
    wall_thickness=wall_thickness,
    valve_cut_radius=valve_cut_radius,
    valve_cut_depth=valve_cut_depth,
    bolt_hole_dia=bolt_hole_dia,
    bolt_head_dia=bolt_head_dia,
    bolt_head_angle=bolt_head_angle,
    bolt_pattern_radius=bolt_pattern_radius,
    chamfer_size=chamfer_size,
)

class GasValveBracket:
    def __init__(self, workplane, m):
        self.workplane = workplane
        self.m = m
        self.build()
    def build(self):
        m = self.m
        # Create 2D profile on XZ plane for revolve
        profile = (
            cq.Workplane('XZ')
            .moveTo(m.outer_radius_bottom, 0)
            .lineTo(m.outer_radius_bottom, m.total_height)
            .lineTo(m.outer_radius_top, m.total_height)
            .lineTo(m.outer_radius_top - m.wall_thickness, m.total_height)
            .lineTo(m.outer_radius_bottom - m.wall_thickness, 0)
            .close()
        )
        # Revolve to create bracket shell
        shell = profile.revolve()
        # Add chamfer on outer edge (top and bottom edges)
        shell = shell.edges('>Z or <Z').chamfer(m.chamfer_size)
        # Create valve pocket by cutting a cylinder from the side at mid-height
        pocket = (
            cq.Workplane('XY')
            .center(m.outer_radius_bottom - m.wall_thickness/2, m.total_height/2)
            .circle(m.valve_cut_radius)
            .extrude(m.valve_cut_depth)
        )
        # Position pocket to intersect outer wall
        pocket = pocket.translate((0,0,0))  # already aligned
        bracket = shell.cut(pocket)
        # Add four countersunk bolt holes on the top flange
        top_face = bracket.faces('>Z')
        # Create pattern points
        import math
        angles = [0, 90, 180, 270]
        for a in angles:
            x = m.bolt_pattern_radius * math.cos(math.radians(a))
            y = m.bolt_pattern_radius * math.sin(math.radians(a))
            top_face = top_face.workplane(offset=0).center(x, y)
            # create countersunk hole using cone + cylinder
            depth = m.total_height  # enough to go through
            # cylinder for through hole
            cyl = cq.Solid.makeCylinder(m.bolt_hole_dia/2, depth)
            # cone for countersink
            csk_radius = m.bolt_head_dia/2
            csk_height = csk_radius / math.tan(math.radians(m.bolt_head_angle/2))
            cone = cq.Solid.makeCone(csk_radius, 0, csk_height)
            hole = cyl.fuse(cone)
            bracket = bracket.cut(hole)
        self.model = bracket

result = GasValveBracket(cq.Workplane('XY'), measures).model
