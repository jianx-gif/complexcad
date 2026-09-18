import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('XY',origin=(0,0,92))
r=w0.sketch().circle(27).push([(2,-1)]).circle(19,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-54,-8),(-51,-8)).arc((0,-53),(51,-8)).segment((54,-8)).segment((54,8)).segment((51,8)).arc((0,53),(-51,8)).segment((-54,8)).close().assemble().circle(46,mode='s').finalize().extrude(-152)).union(w1.workplane(offset=-154/2).cylinder(154,45))