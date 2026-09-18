import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('YZ',origin=(-39,0,0))
r=w0.sketch().arc((-34,-89),(0,-77),(34,-89)).segment((34,-73)).arc((74,-39),(100,6)).arc((49,36),(34,92)).arc((-87,30),(-34,-89)).assemble().finalize().extrude(115).union(w1.sketch().segment((-97,-41),(-93,-41)).arc((-12,-94),(78,-41)).segment((82,-41)).segment((82,-33)).arc((87,0),(82,33)).segment((82,41)).segment((78,41)).arc((-12,94),(-93,41)).segment((-97,41)).segment((-97,33)).arc((-100,0),(-97,-33)).close().assemble().push([(-12,0)]).circle(55,mode='s').finalize().extrude(79))