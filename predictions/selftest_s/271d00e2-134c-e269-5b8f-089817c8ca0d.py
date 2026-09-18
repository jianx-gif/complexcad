import cadquery as cq
from types import SimpleNamespace as Measures

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        profile = (
            cq.Workplane('XZ')
            .moveTo(m.inner_radius, 0)
            .lineTo(m.inner_radius, m.height - m.taper_height)
            .lineTo(m.outer_radius, m.height)
            .lineTo(m.outer_radius, 0)
            .close()
        )
        socket = profile.revolve()
        socket = socket.edges().chamfer(m.bottom_chamfer)
        hole_center = cq.Vector(m.outer_radius - m.side_hole_depth/2, 0, m.height/2)
        hole_dir = cq.Vector(-1, 0, 0)
        hole_cyl = cq.Solid.makeCylinder(m.side_hole_diameter/2, m.side_hole_depth, hole_center, hole_dir)
        socket = socket.cut(hole_cyl)
        cell = (
            cq.Workplane('XY')
            .polygon(6, m.honeycell_diameter)
            .extrude(m.honeycell_height)
        )
        lattice = (
            cq.Workplane('XY')
            .rarray(m.honeycell_spacing, m.honeycell_spacing * 0.866, m.honey_cells_x, m.honey_cells_y)
            .add(cell)
            .combine()
        )
        lattice = lattice.translate((0, 0, m.height/2))
        overlap_radius = (m.inner_radius + m.outer_radius) / 2
        cavity = cq.Workplane('XY').circle(overlap_radius).extrude(m.height)
        honeycomb = cavity.intersect(lattice).union()
        bridge = cq.Workplane('XY').circle(m.inner_radius + 0.5).extrude(m.height)
        result_solid = socket.union(honeycomb).union(bridge)
        self.model = result_solid

m = Measures(
    height=60.0,
    inner_radius=20.0,
    outer_radius=30.0,
    taper_height=15.0,
    bottom_chamfer=2.0,
    side_hole_diameter=8.0,
    side_hole_depth=10.0,
    honeycell_diameter=5.0,
    honeycell_height=55.0,
    honeycell_spacing=6.0,
    honey_cells_x=12,
    honey_cells_y=12,
)

result = XMountSocket(cq.Workplane('XY'), m).model