import cadquery as cq

outer_radius = 40.0
housing_height = 60.0
wall_thickness = 3.0
port_thread_diameter = 20.0
port_thread_length = 25.0
port_chamfer = 1.0
inlet_width = 30.0
inlet_height = 12.0
inlet_position_z = 30.0
rib_thickness = 2.0
rib_height = 15.0
edge_chamfer = 0.5

class FuelPumpInletHousing:
    def __init__(self):
        self.outer_radius = outer_radius
        self.height = housing_height
        self.wall_thickness = wall_thickness
        self.port_dia = port_thread_diameter
        self.port_len = port_thread_length
        self.port_chamfer = port_chamfer
        self.inlet_w = inlet_width
        self.inlet_h = inlet_height
        self.inlet_z = inlet_position_z
        self.rib_thick = rib_thickness
        self.rib_h = rib_height
        self.edge_chamfer = edge_chamfer

    def base_cylinder(self):
        return cq.Workplane("XY").cylinder(self.height, self.outer_radius)

    def shell_body(self, solid):
        return solid.shell(self.wall_thickness)

    def port_cut(self, body):
        body = (
            body.faces("+Z")
            .hole(self.port_dia, depth=self.port_len)
            .faces("+Z")
            .edges()
            .chamfer(self.port_chamfer)
        )
        return body

    def inlet_cut(self, body):
        body = (
            body.faces("+X")
            .workplane(centerOption='CenterOfMass')
            .transformed(offset=(0, 0, self.inlet_z))
            .rect(self.inlet_w, self.inlet_h)
            .cutBlind(-self.wall_thickness * 2)
        )
        return body

    def internal_ring_rib(self, body):
        outer_rib = cq.Workplane("XY").cylinder(self.rib_h, self.outer_radius - self.wall_thickness/2)
        inner_rib = cq.Workplane("XY").cylinder(self.rib_h, self.outer_radius - self.wall_thickness - self.rib_thick)
        rib = outer_rib.cut(inner_rib)
        rib = rib.translate((0, 0, (self.height - self.rib_h) / 2))
        return body.union(rib)

    def add_edge_chamfers(self, body):
        body = body.edges().chamfer(self.edge_chamfer)
        return body

    def build(self):
        solid = self.base_cylinder()
        solid = self.shell_body(solid)
        solid = self.port_cut(solid)
        solid = self.inlet_cut(solid)
        solid = self.internal_ring_rib(solid)
        solid = self.add_edge_chamfers(solid)
        return solid

result = FuelPumpInletHousing().build()