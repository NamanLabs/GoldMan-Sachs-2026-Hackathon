# Start of HEAD
import json
import sys
import math

input_data = json.loads(sys.stdin.read())

map_size = input_data['map_size']
warehouse = [map_size[0] / 2, map_size[1] / 2]
drones = input_data['drones']
deliveries = input_data['deliveries']
no_fly_zones = input_data.get('no_fly_zones', [])
charging_stations = input_data.get('charging_stations', [])
# End of HEAD

# Start of BODY
def solve(warehouse, drones, deliveries, no_fly_zones, charging_stations):
    import itertools

    flight_manifest = []
    dist_cache = {}

    def dist(p1, p2):
        key = (p1[0], p1[1], p2[0], p2[1])
        if key not in dist_cache:
            dist_cache[key] = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        return dist_cache[key]

    processed_nfz = []
    for nfz in no_fly_zones:
        item = {
            'shape': nfz['shape'],
            'T_start': nfz['T_start'],
            'T_end': nfz['T_end']
        }
        if nfz['shape'] == 'circle':
            cx, cy = nfz['center']
            item.update({'cx': cx, 'cy': cy, 'r': nfz['radius'] + 1e-7})
        else:
            c = nfz['corners']
            item.update({
                'xmin': min(c[0][0], c[1][0]) - 1e-7,
                'xmax': max(c[0][0], c[1][0]) + 1e-7,
                'ymin': min(c[0][1], c[1][1]) - 1e-7,
                'ymax': max(c[0][1], c[1][1]) + 1e-7
            })
        processed_nfz.append(item)

    departure_cache = {}

    def get_earliest_departure(p1, p2, t_start):
        key = (p1[0], p1[1], p2[0], p2[1], round(t_start, 1))
        
        if key in departure_cache and departure_cache[key] >= t_start:
            return departure_cache[key]

        d = dist(p1, p2)
        if d == 0:
            return t_start

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        current_t = t_start

        min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])

        for _ in range(8): 
            changed = False
            for nfz in processed_nfz:
                if nfz['T_end'] <= current_t:
                    continue

                entry = None
                exitp = None

                if nfz['shape'] == 'circle':
                    cx, cy, r = nfz['cx'], nfz['cy'], nfz['r']
                    if cx + r < min_x or cx - r > max_x or cy + r < min_y or cy - r > max_y:
                        continue

                    fx = p1[0] - cx
                    fy = p1[1] - cy
                    a = dx * dx + dy * dy
                    b = 2 * (fx * dx + fy * dy)
                    c = fx * fx + fy * fy - r * r
                    disc = b * b - 4 * a * c

                    if disc < 0:
                        continue

                    disc = math.sqrt(disc)
                    t1 = (-b - disc) / (2 * a)
                    t2 = (-b + disc) / (2 * a)

                    if t2 < 0 or t1 > 1:
                        continue

                    entry = max(0.0, t1) * d
                    exitp = min(1.0, t2) * d

                else:
                    xmin, xmax, ymin, ymax = nfz['xmin'], nfz['xmax'], nfz['ymin'], nfz['ymax']
                    if xmax < min_x or xmin > max_x or ymax < min_y or ymin > max_y:
                        continue

                    tmin, tmax = 0.0, 1.0

                    if abs(dx) < 1e-12:
                        if p1[0] < xmin or p1[0] > xmax:
                            continue
                    else:
                        tx1 = (xmin - p1[0]) / dx
                        tx2 = (xmax - p1[0]) / dx
                        tmin = max(tmin, min(tx1, tx2))
                        tmax = min(tmax, max(tx1, tx2))

                    if abs(dy) < 1e-12:
                        if p1[1] < ymin or p1[1] > ymax:
                            continue
                    else:
                        ty1 = (ymin - p1[1]) / dy
                        ty2 = (ymax - p1[1]) / dy
                        tmin = max(tmin, min(ty1, ty2))
                        tmax = min(tmax, max(ty1, ty2))

                    if tmin > tmax or tmax < 0 or tmin > 1:
                        continue

                    entry = max(0.0, tmin) * d
                    exitp = min(1.0, tmax) * d

                enter_time = current_t + entry
                exit_time = current_t + exitp

                if enter_time < nfz['T_end'] and exit_time > nfz['T_start']:
                    current_t = nfz['T_end'] - entry + 1e-3
                    changed = True
                    break

            if not changed:
                departure_cache[key] = current_t
                return current_t

        departure_cache[key] = float('inf')
        return float('inf')

    def evaluate_sequence(drone, sequence, start_time):
        t = start_time
        # Battery fallback handled properly
        battery = drone.get('battery_capacity', drone.get('battery', 500.0)) 
        curr_pos = warehouse

        payload = sum(n['data']['weight'] for n in sequence if n['type'] == 'DELIVERY')
        if payload > drone['max_payload']:
            return False, None

        actions = [{
            "x": warehouse[0],
            "y": warehouse[1],
            "t": t,
            "action": "PICKUP",
            "delivery_ids": [n['data']['id'] for n in sequence if n['type'] == 'DELIVERY']
        }]

        total_energy = 0

        for node in sequence:
            if node['type'] == 'DELIVERY':
                target_pos = (node['data']['x'], node['data']['y'])
            else:
                target_pos = warehouse

            t_dep = get_earliest_departure(curr_pos, target_pos, t)
            if t_dep == float('inf'):
                return False, None

            if t_dep > t:
                actions.append({
                    "x": curr_pos[0],
                    "y": curr_pos[1],
                    "t": t_dep,
                    "action": "WAIT"
                })
                t = t_dep

            d = dist(curr_pos, target_pos)
            energy = d * (1.0 + payload)

            if battery < energy:
                return False, None

            t += d
            battery -= energy
            total_energy += energy
            curr_pos = target_pos

            if node['type'] == 'DELIVERY':
                if t > node['data']['deadline']:
                    return False, None

                actions.append({
                    "x": curr_pos[0],
                    "y": curr_pos[1],
                    "t": t,
                    "action": "DELIVER",
                    "delivery_id": node['data']['id']
                })
                payload -= node['data']['weight']
            else:
                actions.append({
                    "x": warehouse[0],
                    "y": warehouse[1],
                    "t": t,
                    "action": "RETURN"
                })

        return True, (actions, t, total_energy)

    unassigned = sorted(
        deliveries,
        key=lambda x: (x['deadline'], dist(warehouse, (x['x'], x['y'])))
    )

    drone_times = {d['id']: 0.0 for d in drones}
    drone_actions = {d['id']: [] for d in drones}

    while unassigned:
        target = unassigned[0]

        valid_drones = [d for d in drones if d['max_payload'] >= target['weight']]

        if not valid_drones:
            unassigned.pop(0)
            continue

        valid_drones.sort(key=lambda d: drone_times[d['id']])
        assigned = False

        for drone in valid_drones:
            d_time = drone_times[drone['id']]
            
            # PERFECT TLE KILLER: Drones free time ke hisaab se sorted hain. 
            # Agar sabse pehla drone hi time par nahi pahunch sakta, toh baaki koi bhi nahi pahunch payega. 
            # Seedha break karo aur target ko drop kardo.
            if d_time + dist(warehouse, (target['x'], target['y'])) > target['deadline']:
                break
                
            # Aas-paas ke packages ka cluster banao (Max 15 items scan karega)
            pool = unassigned[1:min(16, len(unassigned))]
            pool.sort(key=lambda x: dist((target['x'], target['y']), (x['x'], x['y'])))
            
            combo = [target]
            curr_w = target['weight']
            
            # Payload capacity ke hisaab se combo me packages add karo (Max 4 items ek flight me)
            for pkg in pool:
                if curr_w + pkg['weight'] <= drone['max_payload']:
                    combo.append(pkg)
                    curr_w += pkg['weight']
                if len(combo) >= 4: 
                    break

            best_seq = None
            best_res = None
            best_score = -1e18

            # --- THE TSP (Optimal Routing) ENGINE ---
            # Yeh loop ensure karega ki agar 4 items ka combo possible nahi hai battery/deadline ki wajah se,
            # toh 3 ka best route dekhe, fir 2 ka.
            for L in range(len(combo), 0, -1):
                found_valid = False
                
                for subset in itertools.combinations(combo, L):
                    # Target ko skip nahi karna, warna loop anant (infinite) chal jayega
                    if target not in subset:
                        continue

                    # Ab is subset ke saare possible raste (permutations) check karo
                    for perm in itertools.permutations(subset):
                        seq = [{'type': 'DELIVERY', 'data': p} for p in perm]
                        
                        success, res = evaluate_sequence(drone, seq + [{'type': 'WAREHOUSE'}], d_time)

                        if success:
                            found_valid = True
                            # Score calculation: Pura focus Number of Deliveries maximize karne par
                            score = L * 10000 - res[2]*0.1 - res[1]*0.05
                            if score > best_score:
                                best_score = score
                                best_seq = seq + [{'type': 'WAREHOUSE'}]
                                best_res = res

                # Agar is size 'L' par koi valid chota rasta mil gaya, toh aur packages drop mat karo
                if found_valid:
                    break

            # Assignment successful ho gaya
            if best_seq:
                drone_times[drone['id']] = best_res[1]
                drone_actions[drone['id']].extend(best_res[0])

                # Jo-jo deliver ho gaye unko unassigned list se hata do
                for n in best_seq:
                    if n['type'] == 'DELIVERY' and n['data'] in unassigned:
                        unassigned.remove(n['data'])
                
                assigned = True
                break

        if not assigned:
            unassigned.pop(0) # Package impossible hai, chhod do usko aage badho

    for d_id, acts in drone_actions.items():
        if acts:
            flight_manifest.append({
                "drone_id": d_id,
                "path": acts
            })

    return flight_manifest
# End of BODY

# Start of TAIL
result = solve(warehouse, drones, deliveries, no_fly_zones, charging_stations)
output = {"flight_manifest": result}
print(json.dumps(output))
# End of TAIL
