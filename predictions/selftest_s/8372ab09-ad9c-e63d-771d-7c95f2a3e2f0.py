import cadquery as cq

hub_diameter = 30
hub_height = 15
arm_length = 40
arm_width = 20
hole_diameter = 4
hole_spacing = 10
holes_per_arm = 3
chamfer_dist = 0.5

# central hub
result = cq.Workplane('XY').circle(hub_diameter / 2).extrude(hub_height)
# positive X arm
arm_pos_x = cq.Workplane('XY').center(arm_length / 2, 0).rect(arm_length, arm_width).extrude(hub_height)
result = result.union(arm_pos_x)
# negative X arm
arm_neg_x = cq.Workplane('XY').center(-arm_length / 2, 0).rect(arm_length, arm_width).extrude(hub_height)
result = result.union(arm_neg_x)
# positive Y arm
arm_pos_y = cq.Workplane('XY').center(0, arm_length / 2).rect(arm_width, arm_length).extrude(hub_height)
result = result.union(arm_pos_y)
# negative Y arm
arm_neg_y = cq.Workplane('XY').center(0, -arm_length / 2).rect(arm_width, arm_length).extrude(hub_height)
result = result.union(arm_neg_y)
# chamfer top perimeter edges for safety
result = result.faces('>Z').edges().chamfer(chamfer_dist)
# through-hole patterns on each arm outer face
for direction in ['>X', '<X', '>Y', '<Y']:
    result = result.faces(direction).workplane().rarray(hole_spacing, 0, holes_per_arm, 1).hole(hole_diameter)
