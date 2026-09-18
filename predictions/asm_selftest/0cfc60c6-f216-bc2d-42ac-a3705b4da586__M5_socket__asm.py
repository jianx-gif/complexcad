parts = [base]
parts.append(place(fastener("bearing", 20, 0), axis=(0, 0, 1), point=(0, 0, 2.5), seat=-1.5, flip=False))
parts.append(place(fastener("washer", 'M5', 1), axis=(0, 0, 1), point=(10, 10, 3.6), seat=3.8, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 14, 1), axis=(0, 0, 1), point=(10, 10, 3.6), seat=4.9, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 1), axis=(0, 0, 1), point=(10, 10, 3.6), seat=-3.6, flip=True))
parts.append(place(fastener("washer", 'M5', 2), axis=(0, 0, 1), point=(30, 10, 3.6), seat=1.4, flip=False))
parts.append(place(fastener("screw", 'M5-0.8', 12, 2), axis=(0, 0, 1), point=(30, 10, 3.6), seat=2.5, flip=False))
parts.append(place(fastener("nut", 'M5-0.8', 'M5', 2), axis=(0, 0, 1), point=(30, 10, 3.6), seat=-3.6, flip=True))
