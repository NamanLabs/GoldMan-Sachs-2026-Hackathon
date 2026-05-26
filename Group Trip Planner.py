import sys
from itertools import combinations


def _read_input():
    data = sys.stdin.read().split()
    p = [0]
    def take(n=1):
        vals = data[p[0]:p[0] + n]; p[0] += n
        return vals

    N, D, H = int(take()[0]), int(take()[0]), int(take()[0])

    users = []
    for _ in range(N):
        name = take()[0]
        budget = int(take()[0]); energy = int(take()[0])
        k = int(take()[0])
        tags = set(take(k))
        users.append({'name': name, 'budget': budget,
                      'energy': energy, 'tags': tags, 'active': True})

    A = int(take()[0])
    activities = {}
    for _ in range(A):
        aid = int(take()[0]); aname = take()[0]
        cost = int(take()[0]); dur = int(take()[0])
        ec = int(take()[0]); tag = take()[0]
        activities[aid] = {'id': aid, 'name': aname, 'cost': cost,
                           'duration': dur, 'energy': ec, 'tag': tag}

    E = int(take()[0])
    events = []
    for _ in range(E):
        etype = take()[0]
        if etype == 'DROP':
            day = take()[0]; user = take()[0]
            events.append(f"DROP {day} {user}")
        elif etype == 'WEATHER':
            day = take()[0]; tag = take()[0]
            events.append(f"WEATHER {day} {tag}")
        elif etype == 'FATIGUE':
            day = take()[0]; user = take()[0]; ne = take()[0]
            events.append(f"FATIGUE {day} {user} {ne}")
        elif etype == 'BUDGET':
            day = take()[0]; user = take()[0]; nb = take()[0]
            events.append(f"BUDGET {day} {user} {nb}")
    return N, D, H, users, activities, events


def fmt_day(day, ids, cost, sat):
    """Format one day line exactly as required by the judge."""
    if not ids:
        return f"Day {day}: REST | cost=0 satisfaction=0"
    return (f"Day {day}: "
            f"{' '.join(str(i) for i in sorted(ids))}"
            f" | cost={cost} satisfaction={sat}")

# =========================================================================
# YOUR CODE GOES HERE.
#
# Implement plan_trip(N, D, H, users, activities, events) and return the
# FULL output string (including the trailing newline) that the judge will
# diff against the expected output.
#
# You have these helpers available from the head section:
#   - fmt_day(day, ids, cost, sat)  -> formatted "Day X: ..." line
#   - itertools.combinations
#
# Data shapes:
#   users      : list of dicts {name, budget, energy, tags(set), active(bool)}
#   activities : dict id -> {id, name, cost, duration, energy, tag}
#   events     : list of strings, e.g. "DROP 2 Bob", "WEATHER 3 NATURE",
#                "FATIGUE 2 Alice 5", "BUDGET 4 Alice 20"
# =========================================================================

def plan_trip(N, D, H, users, activities, events):
    lines = []
    lines.append("=== PLAN ===")

    daily_users = {
        d: {u['name']: {k: v for k, v in u.items()} for u in users}
        for d in range(1, D + 1)
    }
    weather_blocks = {d: set() for d in range(1, D + 1)}
    planned_days = {d: {'ids': [], 'cost': 0, 'sat': 0} for d in range(1, D + 1)}

    def plan_day(d, used_act, user_state_dict, w_blocks):
        active_users = [u for u in user_state_dict.values() if u['active']]
        if not active_users:
            return [], 0, 0

        min_b = min(u['budget'] for u in active_users)
        min_e = min(u['energy'] for u in active_users)

        eligible = []
        for a in activities.values():
            if a['id'] not in used_act and a['tag'] not in w_blocks:
                sat = sum(1 for u in active_users if a['tag'] in u['tags'])
                eligible.append({
                    'id': a['id'],
                    'cost': a['cost'],
                    'energy': a['energy'],
                    'duration': a['duration'],
                    'sat': sat
                })

        eligible.sort(key=lambda x: x['id'])

        best_choice = (0, 0, ())

        def dfs(idx, c, e, dur, s, sub_ids):
            nonlocal best_choice
            
            cand = (-s, c, tuple(sub_ids))
            if cand < best_choice:
                best_choice = cand

            for i in range(idx, len(eligible)):
                act = eligible[i]
                if c + act['cost'] <= min_b and \
                   e + act['energy'] <= min_e and \
                   dur + act['duration'] <= H:
                   
                    sub_ids.append(act['id'])
                    dfs(i + 1, c + act['cost'], e + act['energy'], dur + act['duration'], s + act['sat'], sub_ids)
                    sub_ids.pop()

        dfs(0, 0, 0, 0, 0, [])

        return list(best_choice[2]), best_choice[1], -best_choice[0]

    used_act = set()
    for d in range(1, D + 1):
        ids, cost, sat = plan_day(d, used_act, daily_users[d], weather_blocks.get(d, set()))
        planned_days[d] = {'ids': ids, 'cost': cost, 'sat': sat}
        used_act.update(ids)
        lines.append(fmt_day(d, ids, cost, sat))

    for e_idx, event_str in enumerate(events, 1):
        parts = event_str.split()
        etype = parts[0]
        eday = int(parts[1])

        if etype == 'DROP':
            user = parts[2]
            for d in range(eday, D + 1):
                if d in daily_users and user in daily_users[d]:
                    daily_users[d][user]['active'] = False
        elif etype == 'FATIGUE':
            user = parts[2]
            ne = int(parts[3])
            for d in range(eday, D + 1):
                if d in daily_users and user in daily_users[d]:
                    daily_users[d][user]['energy'] = ne
        elif etype == 'BUDGET':
            user = parts[2]
            nb = int(parts[3])
            for d in range(eday, D + 1):
                if d in daily_users and user in daily_users[d]:
                    daily_users[d][user]['budget'] = nb
        elif etype == 'WEATHER':
            tag = parts[2]
            if eday in weather_blocks:
                weather_blocks[eday].add(tag)

        lines.append(f"=== EVENT {e_idx}: {event_str} ===")

        used_act = set()
        for d in range(1, eday):
            if d in planned_days:
                used_act.update(planned_days[d]['ids'])

        start_replan = max(1, eday)
        for d in range(start_replan, D + 1):
            if d in daily_users:
                ids, cost, sat = plan_day(d, used_act, daily_users[d], weather_blocks.get(d, set()))
                planned_days[d] = {'ids': ids, 'cost': cost, 'sat': sat}
                used_act.update(ids)
                lines.append(fmt_day(d, ids, cost, sat))

    return '\n'.join(lines) + '\n'
if __name__ == '__main__':
    _N, _D, _H, _users, _activities, _events = _read_input()
    sys.stdout.write(plan_trip(_N, _D, _H, _users, _activities, _events))
    
