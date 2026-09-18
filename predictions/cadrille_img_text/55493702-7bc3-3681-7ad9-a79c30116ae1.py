import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('ZX',origin=(0,4,0))
r=w0.sketch().segment((-89,-88),(89,-88)).segment((89,8)).arc((0,-67),(-89,8)).close().assemble().finalize().extrude(200).union(w1.sketch().arc((-59,-38),(51,11),(59,89)).arc((28,29),(-34,1)).arc((-45,-2),(-51,-13)).arc((-55,-26),(-59,-38)).assemble().finalize().extrude(41))