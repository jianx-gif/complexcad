parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-15, -20, 20), seat=10, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-15, -20, 20), seat=11.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 24, 0), axis=(0, 0, 1), point=(-15, -20, 20), seat=12.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-15, -20, 20), seat=-20, flip=True))
