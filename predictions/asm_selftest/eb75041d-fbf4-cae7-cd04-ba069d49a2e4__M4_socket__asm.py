parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, -1, 0), point=(0, -4.982, 10), seat=3.782, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 14, 0), axis=(0, -1, 0), point=(0, -4.982, 10), seat=4.682, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, -1, 0), point=(0, -4.982, 10), seat=-4.982, flip=True))
