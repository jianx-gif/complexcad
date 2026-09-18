import cadquery as cq

# Parameters
coupler_length = 80.0
coupler_width = 40.0
coupler_height = 20.0
wall_thickness = 4.0
bore_diameter = 15.0
rib_height = 10.0
rib_thickness = 6.0
rib_depth = 8.0
rib_spacing = 12.0
chamfer_distance = 1.0
mount_hole_diameter = 6.0
mount_hole_spacing = 20.0
mount_hole_offset = 5.0
pocket_depth = 4.0
pocket_length = 30.0

# Base block with wall thickness
outer = cq.Workplane('XY').rect(coupler_width, coupler_height).extrude(coupler_length)
inner = cq.Workplane('XY').rect(coupler_width - 2*wall_thickness, coupler_height - 2*wall_thickness).extrude(coupler_length)
base = outer.cut(inner)

# Central bore through entire length
result = base.faces('>Z').workplane().hole(bore_diameter)

# Apply chamfer on outer vertical edges
result = result.edges('|Z').chamfer(chamfer_distance)

# Function to add ribs on a given side face

def add_ribs(part, face_selector):
    num = int(coupler_length // rib_spacing) + 1
    zs = [(-coupler_length/2) + rib_spacing*i for i in range(num)]
    pts = [(0, z) for z in zs]
    ribs = (
        part.faces(face_selector).workplane(centerOption='CenterOfMass')
            .pushPoints(pts)
            .rect(rib_thickness, rib_height)
            .extrude(rib_depth)
    )
    return ribs

result = add_ribs(result, '>X')
result = add_ribs(result, '<X')

# Mounting holes on both ends (+Z and -Z faces)
for face in ['>Z', '<Z']:
    result = (
        result.faces(face).workplane()
            .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
            .hole(mount_hole_diameter)
    )

# Cable routing pocket on top (Y+) surface
pocket_width = coupler_width - 2*wall_thickness
result = (
    result.faces('>Y').workplane(centerOption='CenterOfMass')
        .rect(pocket_width, pocket_length)
        .cutBlind(-pocket_depth)
)
