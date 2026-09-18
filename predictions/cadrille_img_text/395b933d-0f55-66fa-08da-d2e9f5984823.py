import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,59,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-59,-67),(-59,-66)).segment((-51,-66)).segment((-51,-73)).arc((55,83),(-59,-67)).assemble().circle(93,mode='s').finalize().extrude(-133).union(w1.sketch().arc((19,-96),(57,-77),(100,-67)).arc((98,-55),(97,-43)).arc((54,-67),(19,-96)).assemble().finalize().extrude(-183))