import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,24,0))
w1=cq.Workplane('YZ',origin=(86,0,0))
r=w0.sketch().arc((-38,-90),(1,-94),(38,-85)).arc((58,-69),(75,-49)).arc((86,-18),(89,15)).segment((75,15)).arc((43,-29),(-9,-43)).segment((-9,-50)).segment((-20,-50)).segment((-20,-43)).arc((-27,-42),(-34,-40)).arc((-29,-66),(-38,-90)).assemble().finalize().extrude(-27).union(w1.sketch().circle(100).circle(93,mode='s').finalize().extrude(-108))