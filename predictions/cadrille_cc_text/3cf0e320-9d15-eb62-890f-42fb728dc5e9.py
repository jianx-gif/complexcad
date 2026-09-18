import cadquery as cq
import math
module = 2.0
module = 2.0
module = 2.0
module = 1.0
key_width = 20.0
key_depth = 6.0
key_length = module * module
chamfer_size = 0.8
shaft_diameter = 10.0
mount_hole_diameter = 4.0
mount_hole_radius = 30.0
profile = (
    cq.Workplane("XY")
    .polyline([
        (module, 0),
        (module, 0),
        (module, module),
        (module, 0),
        (module, 0),
    ])
    .close()
)
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
mod = module
profile = (
    profile
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(key_width, key_depth)
    .cutBlind(-key_depth)
)
mod = (
    end
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m.mount_hole_diameter)
)
mod = (
    end
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
result = (
    end
    .edges("|Z")
    .chamfer(chamfer_size)
)
