GoldMan Sachs hackathon 
3 questions
1. Group Trip Planner
Story
You and your friends are planning a multi-day group trip. Every member has a different daily budget, different interests, and a different energy level. The real world is messy — people drop out, the weather turns bad, some travellers get tired, and budgets get cut at the last minute.

You must build the brain behind a group-trip app that:

Picks the best joint itinerary that respects every participant.
Re-plans the remainder of the trip every time something changes.
Is fully deterministic so its decisions can be reviewed and audited.
Your program will be judged on whether its output exactly matches the reference planner under the rules below.

Problem
You are given a group of N travellers going on a D-day trip with H usable hours per day. You are also given a catalogue of A candidate activities and a chronological list of E real-world events that will interrupt the trip.

Definitions
Interest tags are drawn from the fixed set {ADVENTURE, CULTURE, FOOD, NATURE, SHOPPING, NIGHTLIFE}.
Each traveller has a daily budget (max spend per person per day), an energy level (0–100), and a non‑empty set of liked tags.
Each activity has a positive cost per person, an integer duration in hours, an integer energy cost, and exactly one tag.
An activity is eligible on day d if (a) it has not been chosen on a previous day, and (b) its tag is not weather-blocked on day d.
Feasibility Constraints (The "Fairness" Rules)
Before calculating scores, you must identify all possible subsets of eligible activities that satisfy three strict limits. These limits are "bottlenecked" by the most restricted member of the group:

Financial Fairness:
The total cost of the day's activities cannot exceed the daily budget of the traveler with the lowest budget.
Σ cost(a) ≤ min(u.budget for u in U)

Stamina Fairness:
The total energy cost cannot exceed the current energy level of the weakest (or most tired) active traveler.
Σ energy(a) ≤ min(u.energy for u in U)

Time Constraint:
The total hours spent on activities must fit within the fixed daily limit H.
Σ duration(a) ≤ H

The Objective: Satisfaction Score
The goal is to maximize the collective enjoyment of the group. The satisfaction score for a subset S is calculated as:

satisfaction(S) = Σ over a in S of |{ u ∈ U : tag(a) ∈ u.interests }|
In plain terms: For every activity in your proposed plan, count how many people in the group actually like that activity's category (tag). Sum these counts across all activities in the subset.

Example:
If you pick a "Hike" (NATURE) and 3 out of 5 travelers have NATURE in their interests, that activity adds 3 points to the day's satisfaction score.

The Decision Engine (Lexicographical Tie-Breaking)
Because multiple different combinations of activities might yield the same satisfaction or fit the same constraints, the problem requires a deterministic way to pick exactly one "best" subset. You must compare subsets using a tuple and pick the one that is "smallest" lexicographically:

Primary Priority (Satisfaction): Maximize the satisfaction score. (In the tuple, this is represented as -satisfaction because the rule seeks the "smallest" value, and a larger satisfaction becomes a smaller negative number).
Secondary Priority (Cost): If two subsets provide the same satisfaction, choose the one with the lower total cost.
Tertiary Priority (ID List): If satisfaction and cost are identical, sort the activity IDs in each subset and compare the lists. Choose the subset whose ID list comes first lexicographically (e.g., [1, 4] is smaller than [2, 3]).
Operational Logic
Rest Days: If no activities can fit the constraints, or if the "best" valid subset is an empty set, the day is designated as REST.
State Persistence: Once an activity is chosen for a day, it is removed from the "eligible" pool for all future days.
Replanning: Because events (like someone dropping out or a budget change) alter the constraints (min(u.budget) or min(u.energy)), the optimization must be re-run for all remaining days whenever an event occurs.
Example
Available Activities
ID	Tag	Cost	Energy	Duration	Interested Users	Points
A1	FOOD	$20	20	3	Alice, Bob	2
A2	NATURE	$25	30	4	Alice	1
A3	CULTURE	$30	40	4	Bob	1
Evaluating Possible Subsets (S):
Subset S	Total Cost	Total Energy	Total Duration	Feasible?	Satisfaction
{A1, A2}	$45	50	7	Yes	2 + 1 = 3
{A1, A3}	$50	60	7	Yes	2 + 1 = 3
{A2, A3}	`$55	70	8	No (Cost > $`50)	-
{A1, A2, A3}	$75	90	11	No (Exceeds all)	-
Applying the Lexicographical Rule
We compare the two feasible subsets, {A1, A2} and {A1, A3}:

Satisfaction: Both have a score of 3. (Tie)
Total Cost: {A1, A2} costs 50.
Decision: {A1, A2} is chosen because it is cheaper (50).
Result: The plan for the day is [A1, A2]. If no subsets were feasible (e.g., if all activities cost more than $50), the output would be REST.

Input Format

The input consists of several sections, each on its own line or group of lines. All values are separated by spaces.

N D H
<userLine>          × N
A
<activityLine>      × A
E
<eventLine>         × E
Where: - N is the number of travellers (3 ≤ N ≤ 10) - D is the number of days (1 ≤ D ≤ 7) - H is the number of usable hours per day (1 ≤ H ≤ 24) - Each <userLine> describes one traveller - A is the number of activities (1 ≤ A ≤ 20) - Each <activityLine> describes one activity - E is the number of events (0 ≤ E ≤ 20) - Each <eventLine> describes one event

User Line Example
Alice 100 80 2 ADVENTURE FOOD
name: Alice
dailyBudget: 100
energy: 80
k: 2 (number of interest tags)
tags: ADVENTURE FOOD
Activity Line Example
1 Museum 30 3 20 CULTURE
id: 1
name: Museum
cost: 30
duration: 3
energy: 20
tag: CULTURE
Event Line Examples
WEATHER 2 ADVENTURE
DROP 3 Bob
FATIGUE 2 Alice 50
BUDGET 4 Cara 60
WEATHER: On day 2, all activities with tag ADVENTURE are blocked
DROP: Bob leaves the trip starting on day 3
FATIGUE: Alice's energy is set to 50 from day 2 onward
BUDGET: Cara's daily budget is set to 60 from day 4 onward
Full Example Input
3 2 8
Alice 100 80 2 ADVENTURE FOOD
Bob 80 60 2 CULTURE FOOD
Cara 120 70 2 NATURE FOOD
4
1 Museum 30 3 20 CULTURE
2 Hike 40 5 50 ADVENTURE
3 Cafe 20 2 10 FOOD
4 Park 25 3 15 NATURE
1
WEATHER 2 ADVENTURE
This input describes a 3-person, 2-day trip with 8 hours per day, 4 activities, and 1 event (weather blocks ADVENTURE on day 2).

Constraints

3   ≤ N ≤ 10
1   ≤ D ≤ 7
1   ≤ H ≤ 24
1   ≤ A ≤ 20
0   ≤ E ≤ 20
1   ≤ cost, duration, energy, budget ≤ 10000
0   ≤ user.energy ≤ 100
Names are alphanumeric strings without spaces.

Output Format

Print the initial plan first:

=== PLAN ===
Day 1: <ids ...>|REST | cost=<c> satisfaction=<s>
Day 2: ...
...
Day D: ...
Then, for each event in order (1-indexed), print:

=== EVENT <i>: <original event line verbatim> ===
Day <day>: ...
...
Day D: ...
Activity ids on a day line are printed in ascending order, separated by single spaces. Use the literal word REST when the chosen subset is empty. cost is the per-person cost for that day; satisfaction is the integer satisfaction score.

There must be no trailing whitespace and the file must end with a single newline.

Example
Input
3 2 8
Alice 100 80 2 ADVENTURE FOOD
Bob 80 60 2 CULTURE FOOD
Cara 120 70 2 NATURE FOOD
4
1 Museum 30 3 20 CULTURE
2 Hike 40 5 50 ADVENTURE
3 Cafe 20 2 10 FOOD
4 Park 25 3 15 NATURE
1
WEATHER 2 ADVENTURE
Output
=== PLAN ===
Day 1: 2 3 | cost=60 satisfaction=4
Day 2: 1 4 | cost=55 satisfaction=2
=== EVENT 1: WEATHER 2 ADVENTURE ===
Day 2: 1 4 | cost=55 satisfaction=2
Notes on the example
On Day 1, picking {Hike, Cafe} scores 1(Adv→Alice) + 3(Food→all) = 4, costs 60, fits energy 60 ≤ min(80,60,70)=60, fits time 7 ≤ 8. Any other feasible subset scores ≤ 4 or costs more.
On Day 2, {Museum, Park} scores 1+1=2, costs 55. Hike was already used.
The weather event blocks ADVENTURE only on day 2, but Hike was already consumed on day 1, so the replan reproduces the same Day 2.
Sample Input 0

3 2 8
Alice 100 80 2 ADVENTURE FOOD
Bob 80 60 2 CULTURE FOOD
Cara 120 70 2 NATURE FOOD
4
1 Museum 30 3 20 CULTURE
2 Hike 40 5 50 ADVENTURE
3 Cafe 20 2 10 FOOD
4 Park 25 3 15 NATURE
1
WEATHER 2 ADVENTURE
Sample Output 0

=== PLAN ===
Day 1: 1 3 4 | cost=75 satisfaction=5
Day 2: 2 | cost=40 satisfaction=1
=== EVENT 1: WEATHER 2 ADVENTURE ===
Day 2: REST | cost=0 satisfaction=0
Submissions: 15379
Max Score: 100
Difficulty: Medium
Rate This Challenge:

    
More
 
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

    # TODO 1: build the initial D-day plan, appending one fmt_day(...) per day.

    # TODO 2: for each event (1-indexed), append a header
    #         "=== EVENT i: <event line verbatim> ==="
    #         then mutate state and re-plan days [eventDay..D],
    #         preserving the activity selections of days [1..eventDay-1].

    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    _N, _D, _H, _users, _activities, _events = _read_input()
    sys.stdout.write(plan_trip(_N, _D, _H, _users, _activities, _events))
    
1
import sys
2
from itertools import combinations
3
​
4
​
5
def _read_input():
6
    data = sys.stdin.read().split()
7
    p = [0]
8
    def take(n=1):
9
        vals = data[p[0]:p[0] + n]; p[0] += n
10
        return vals
11
​
12
    N, D, H = int(take()[0]), int(take()[0]), int(take()[0])
13
​
14
    users = []
15
    for _ in range(N):
16
        name = take()[0]
17
        budget = int(take()[0]); energy = int(take()[0])
18
        k = int(take()[0])
19
        tags = set(take(k))
20
        users.append({'name': name, 'budget': budget,
21
                      'energy': energy, 'tags': tags, 'active': True})
22
​
23
    A = int(take()[0])
24
    activities = {}
25
    for _ in range(A):
26
        aid = int(take()[0]); aname = take()[0]
27
        cost = int(take()[0]); dur = int(take()[0])
28
        ec = int(take()[0]); tag = take()[0]
29
        activities[aid] = {'id': aid, 'name': aname, 'cost': cost,
30
                           'duration': dur, 'energy': ec, 'tag': tag}
31
​
32
    E = int(take()[0])
33
    events = []
34
    for _ in range(E):
35
        etype = take()[0]
36
        if etype == 'DROP':
37
            day = take()[0]; user = take()[0]
38
            events.append(f"DROP {day} {user}")
39
        elif etype == 'WEATHER':
40
            day = take()[0]; tag = take()[0]
41
            events.append(f"WEATHER {day} {tag}")
42
        elif etype == 'FATIGUE':
43
            day = take()[0]; user = take()[0]; ne = take()[0]
44
            events.append(f"FATIGUE {day} {user} {ne}")
45
        elif etype == 'BUDGET':
46
            day = take()[0]; user = take()[0]; nb = take()[0]
47
            events.append(f"BUDGET {day} {user} {nb}")
48
    return N, D, H, users, activities, events
49
​
50
​
51
def fmt_day(day, ids, cost, sat):
52
    """Format one day line exactly as required by the judge."""
53
    if not ids:
54
        return f"Day {day}: REST | cost=0 satisfaction=0"
55
    return (f"Day {day}: "
56
            f"{' '.join(str(i) for i in sorted(ids))}"
57
            f" | cost={cost} satisfaction={sat}")
58
​
59
# =========================================================================
60
# YOUR CODE GOES HERE.
61
#
62
# Implement plan_trip(N, D, H, users, activities, events) and return the
63
# FULL output string (including the trailing newline) that the judge will
64
# diff against the expected output.
65
#
66
# You have these helpers available from the head section:
67
#   - fmt_day(day, ids, cost, sat)  -> formatted "Day X: ..." line
68
#   - itertools.combinations
69
#
70
# Data shapes:
71
#   users      : list of dicts {name, budget, energy, tags(set), active(bool)}
72
#   activities : dict id -> {id, name, cost, duration, energy, tag}
73
#   events     : list of strings, e.g. "DROP 2 Bob", "WEATHER 3 NATURE",
74
#                "FATIGUE 2 Alice 5", "BUDGET 4 Alice 20"
75
# =========================================================================
76
​
77
def plan_trip(N, D, H, users, activities, events):
78
    lines = []
79
    lines.append("=== PLAN ===")
80
​
81
    # TODO 1: build the initial D-day plan, appending one fmt_day(...) per day.
82
​
83
    # TODO 2: for each event (1-indexed), append a header
84
    #         "=== EVENT i: <event line verbatim> ==="
85
    #         then mutate state and re-plan days [eventDay..D],
86
    #         preserving the activity selections of days [1..eventDay-1].
87
​
88
    return '\n'.join(lines) + '\n'
89
​
90
if __name__ == '__main__':
91
    _N, _D, _H, _users, _activities, _events = _read_input()
92
    sys.stdout.write(plan_trip(_N, _D, _H, _users, _activities, _events))
93




2. JSON → TypeScript Type Generator
Given a JSON array of objects on stdin, output a deterministic TypeScript type declaration to stdout.

The output must match the expected answer character-for-character (including whitespace, ordering, and newlines).

Use LF (\n) line endings (Unix-style). No \r\n.
Input Format

Line 1: An integer T — the number of test cases (1 ≤ T ≤ 50).
Next 2×T lines: For each test case, two lines:
Line A: A single string — the root type name (e.g., RootType). Contains no spaces or special characters.
Line B: A valid JSON array of objects, always on a single line (compact format). The array contains 0 to 10,000 objects.
Reading the input: Read the first line as the number of test cases. Then for each test case, read one line as the root type name and the next line as the compact JSON string. Parse the JSON using a standard JSON parser.

Constraints

0 ≤ number of objects ≤ 10,000
JSON is valid and the top-level value is always an array.
Every element of the top-level array is a JSON object {...} (never a primitive or array at the top level).
Maximum nesting depth: 10 levels.
Maximum total keys across all objects: 100,000.
Key names: start with a lowercase letter [a-z], followed by zero or more characters from [a-zA-Z0-9_], and the last character is never a digit. In regex: single-char keys match [a-z]; multi-char keys match [a-z][a-zA-Z0-9_]*[a-zA-Z_]. (This ensures no key naturally generates a suffixed collision name like Address2.)
The root type name (line 1 of input) matches [A-Z][a-zA-Z]* (starts with uppercase letter, letters only, no digits or special characters).
No circular references (impossible in JSON).
Array elements are never arrays themselves (no nested arrays like [[1,2],[3,4]]).
If a field's value is an array containing objects in any record, that field's value is never a direct (non-array) object in any other record. (This avoids ambiguity in interface naming between element-level and field-level objects.)
Output Format

For each test case, print the TypeScript .d.ts declaration following the exact formatting rules below.

Separate the output of consecutive test cases with a single line containing exactly --- (three hyphens, no spaces).

No --- before the first test case.
No --- after the last test case.
One trailing newline after the very last closing brace of the last test case (i.e., the entire output ends with }\n or {}\n).
The judge performs a strict string comparison — there is only one correct output for any given input.

Formatting Rules (MUST follow exactly)
These rules guarantee a single deterministic output:

F1. Interfaces
Each type is emitted as export interface <Name> { (one space between name and opening brace).
Closing brace } is on its own line with no indentation.
Non-empty interfaces: opening { on the declaration line, properties on subsequent lines, } alone on last line.
Empty interfaces (no properties): export interface RootType {} (space before {, no space between { and }, all on one line).
F2. Properties
Each property is on its own line, indented with 2 spaces.
Format: <key><optional>: <type>;
<optional> is ? if the field is optional, otherwise empty.
A single space after the colon.
Terminated with a semicolon ;.
Properties are sorted by case-sensitive ASCII order of the key name within each interface.
F3. Type Expressions
Primitive types: string, number, boolean, null.
Union types: components sorted by case-sensitive ASCII comparison of their string representation, joined with | (space-pipe-space).
Sort key is the literal type string as written (e.g., null, number, string, Address, number[], (number | string)[]).
Uppercase letters (A-Z, 65-90) sort before lowercase (a-z, 97-122).
Parenthesis ( (40) sorts before all letters.
Example: number | string (NOT string | number because n < s).
Example: boolean | null | number | string.
Example with interface: Address | null (because A (65) < n (110)).
Example with parens: (number | string)[] | boolean (because ( (40) < b (98)).
Array types:
Single element type: <type>[] (e.g., string[], number[]).
Union element type: (<union>)[] with parentheses (e.g., (number | string)[]).
Empty arrays with no other type info: unknown[].
Object types: Use the generated interface name (e.g., Address).
Nullable object: <InterfaceName> | null (sorted by ASCII, so Address | null since A (65) < n (110)).
F4. Interface Ordering
All interfaces are printed in case-sensitive ASCII order by name (uppercase A-Z before lowercase a-z; digits 0-9 before letters).
Separated by exactly one blank line between each interface.
No leading blank line before the first interface.
One trailing newline after the last closing brace (i.e., the file ends with }\n).
F5. Naming (Deterministic — NO creative freedom)
The root interface uses the exact name given on the first input line.
Every other interface is named after the KEY (property name) in the parent object whose value is that object (or array of objects). The transform is: capitalize the first character of the key; leave all other characters unchanged.
Formula: interfaceName = key[0].toUpperCase() + key.slice(1)
The name is derived ONLY from the immediate parent key — NOT from ancestor path, NOT from the content/shape of the object.
Examples:
Key address holds an object → interface name is Address
Key userProfile holds an object → interface name is UserProfile
Key my_field holds an object → interface name is My_field
Key posts holds an array of objects → interface for the element type is Posts
Key x holds an object → interface name is X
Nested example: { "user": { "profile": { "name": "Alice" } } } → key user produces User, key profile produces Profile (NOT UserProfile).
This is NOT full PascalCase or camelCase conversion. It is ONLY: key[0].toUpperCase() + key.slice(1). No other transformation.
Name collisions: If two different nested paths produce the same interface name after this transformation, OR if a derived name equals the root type name, append a numeric suffix starting at 2 for the collision: Address, Address2, Address3, etc.
The root type name is reserved first (it always gets the unsuffixed name).
Among derived interfaces, collision order is determined by first encounter in a depth-first, alphabetical-key traversal of the merged type tree. The first encountered gets the unsuffixed name (or 2 if root took it), subsequent get incrementing suffixes.
"Depth-first, alphabetical-key" means: at each object level, visit keys in sorted (ASCII) order; for each key, recurse into its children before moving to the next sibling key.
Name assignment uses a global set of used names. For each interface, try the base name; if taken, try base+2, base+3, etc. until an unused name is found. (Since keys never end in a digit, suffixed names like Address2 can never naturally arise from a different key, so this is guaranteed collision-free.)
F6. Type Inference Rules
JSON value(s) observed	TypeScript Type
Any string	string
Any number (int or float)	number
true or false	boolean
null	null
Object {...}	Named interface
Array [...]	See array rules below
Each individual value maps to its type independently. When multiple types are observed for the same key, they form a union (see F7).

F7. Merging Rules (across all objects in the input array)
Union of keys: The output contains every key observed in any object.
Optional (?): A key is optional if it is absent from at least one object in the array.
A key that is present but null is NOT absent — it is present with type null.
Type string computation: For a key with mixed value types, see R1 in the "Rules for Mixed/Complex Types" section below. The summary:
All arrays for that key are merged into ONE type string (using rule 6).
All objects for that key are merged into ONE interface.
Each distinct primitive/null type contributes its type string.
Type union: The field type is the sorted (ASCII) union of all distinct type strings (one for arrays if any, one for objects if any, plus each primitive type observed).
Nested object merge: If a key's value is an object in multiple objects, ALL those objects are merged into a single interface (recursive). The interface appears once in the type union.
Array type string: For arrays, collect ALL elements from ALL arrays for that key across ALL objects. Compute the union of type strings of elements:
If all elements produce one type string → <type>[] (e.g., number[])
If multiple distinct type strings → (<sorted union>)[] (e.g., (number | string)[])
If no elements seen (only empty arrays) → unknown[]
If elements include objects, merge them into one interface (named from parent key); use the interface name as one of the union components.
Array of objects: If array elements include objects, ALL object elements across all arrays for that key are merged into one interface.
F8. Edge Cases
Empty input array []: Output a single empty interface with the given root name.
Object present in some, absent in others: Field is optional, type is the interface name.
Object in some, null in some, absent in some: Field is optional, type is <Interface> | null.
A field that is only ever null: Type is null.
A field that is sometimes missing and sometimes null: Optional with type null → fieldName?: null;
Field is array in some objects, non-array in others: Not optional (if present in all); type is the union of all type strings (e.g., number[] | string).
Path Separation Rule
Each unique path in the type tree produces its own interface, even if two paths produce interfaces with identical shapes.
Example: billing.address and shipping.address are two different interfaces even if they have the same fields.
Names are assigned per-path, with collision suffixes as needed.
Rules for Mixed/Complex Types
These cases are valid input and must be handled. The rules below guarantee a single correct output.

R1. Field has mixed categories across objects (e.g., array in one, primitive in another)
First, separate all observed values into categories: - All arrays for that key (across all objects) are merged together into ONE array type string (using F7.6: merge all elements into one pool). - All objects for that key are merged into ONE interface. - Primitives/null each contribute their type string.

Then compute the field type as the union of: - The single merged array type string (if any arrays exist): e.g., number[], (number | string)[], unknown[] - The single interface name (if any objects exist): e.g., Config - Each distinct primitive type observed: string, number, boolean, null

The union is sorted by ASCII.

Example: field x is [1,2] in obj 1, ["a"] in obj 2, true in obj 3 → - Arrays merged: elements are 1, 2, "a" → type string (number | string)[] - Primitive: boolean - Union sorted by ASCII: ( (40) < b (98) → (number | string)[] | boolean

R2. Array elements mix objects with primitives
Collect ALL elements from ALL arrays for that field across all objects. For each element: - primitives/null → their type (string, number, boolean, null) - objects → merge ALL object elements into a single interface (named from parent key)

The element type is the union of the interface name + all primitive types observed, sorted by ASCII.

Example: field items has value [1, {"a": true}, "hi"] →
- Objects merged → interface Items with { a: boolean; } - Primitives → number, string - Element type: (Items | number | string)[]

R3. Field is object in some, primitive/array in others
The objects at that path are merged into one interface (as usual). The field type is the union of all type strings.

Example: field data is {"x":1} in one object, "raw" in another, absent in a third →
- Interface Data with { x: number; } - Type: Data | string, field is optional (absent in third object) - Output: data?: Data | string;

R4. Field is object in some, null in some, and a primitive in others
Same union rule. The type is the sorted union of all observed type strings.

Example: field meta is {"k":"v"} in one, null in another, 42 in a third →
- Interface Meta with { k: string; } - Type strings: Meta, null, number - ASCII sort: M(77) < n(110); then null vs number: compare char-by-char → n=n, u=u, l(108) < m(109) → null < number - Result: Meta | null | number - Output: meta: Meta | null | number;

Sample Input 0

13
RootType
[{"name":"Alice","age":30,"active":true},{"name":"Bob","age":25,"active":false}]
RootType
[{"id":1,"name":"Alice","email":"alice@example.com"},{"id":2,"name":"Bob"},{"id":3,"name":"Charlie","email":null}]
RootType
[{"id":1,"name":"Alice","address":{"street":"123 Main St","city":"Springfield","zip":"62701"}},{"id":2,"name":"Bob","address":{"street":"456 Oak Ave","city":"Shelbyville"}}]
RootType
[{"id":1,"tags":["admin","user"],"scores":[95,87,92]},{"id":2,"tags":["guest"],"scores":[78,81]},{"id":3,"tags":[],"scores":[88],"metadata":{"source":"import"}}]
RootType
[{"id":1,"value":"hello","items":[1,"two",true]},{"id":"abc","value":42,"items":[null,3]}]
RootType
[{"user":{"profile":{"name":"Alice","avatar":{"url":"https://img.example.com/a.png","width":100,"height":100}},"settings":{"theme":"dark","notifications":true}},"posts":[{"title":"Hello","likes":5},{"title":"World","likes":12,"pinned":true}]},{"user":{"profile":{"name":"Bob","avatar":null},"settings":{"theme":"light","notifications":false,"language":"en"}},"posts":[]}]
RootType
[]
RootType
[{"a":null,"b":1},{"a":null,"b":null},{"b":2}]
RootType
[{"billing":{"address":{"city":"NYC"}},"shipping":{"address":{"city":"LA","zip":"90001"}}}]
Data
[{"config":{"retries":3}},{"config":null},{}]
RootType
[{"data":[1,2,3]},{"data":"raw"}]
RootType
[{"items":[1,{"label":"x"},"hello",{"label":"y","count":5}]}]
Config
[{"config":{"timeout":30},"name":"app"}]
Sample Output 0

export interface RootType {
  active: boolean;
  age: number;
  name: string;
}
---
export interface RootType {
  email?: null | string;
  id: number;
  name: string;
}
---
export interface Address {
  city: string;
  street: string;
  zip?: string;
}

export interface RootType {
  address: Address;
  id: number;
  name: string;
}
---
export interface Metadata {
  source: string;
}

export interface RootType {
  id: number;
  metadata?: Metadata;
  scores: number[];
  tags: string[];
}
---
export interface RootType {
  id: number | string;
  items: (boolean | null | number | string)[];
  value: number | string;
}
---
export interface Avatar {
  height: number;
  url: string;
  width: number;
}

export interface Posts {
  likes: number;
  pinned?: boolean;
  title: string;
}

export interface Profile {
  avatar: Avatar | null;
  name: string;
}

export interface RootType {
  posts: Posts[];
  user: User;
}

export interface Settings {
  language?: string;
  notifications: boolean;
  theme: string;
}

export interface User {
  profile: Profile;
  settings: Settings;
}
---
export interface RootType {}
---
export interface RootType {
  a?: null;
  b: null | number;
}
---
export interface Address {
  city: string;
}

export interface Address2 {
  city: string;
  zip: string;
}

export interface Billing {
  address: Address;
}

export interface RootType {
  billing: Billing;
  shipping: Shipping;
}

export interface Shipping {
  address: Address2;
}
---
export interface Config {
  retries: number;
}

export interface Data {
  config?: Config | null;
}
---
export interface RootType {
  data: number[] | string;
}
---
export interface Items {
  count?: number;
  label: string;
}

export interface RootType {
  items: (Items | number | string)[];
}
---
export interface Config {
  config: Config2;
  name: string;
}

export interface Config2 {
  timeout: number;
}
Submissions: 15253
Max Score: 100
Difficulty: Medium
Rate This Challenge:

    
More
 
1
# Input : line 1 = T; then per case: line A = root name, line B = compact JSON.
2
# Output: per-case blocks joined by a line `---`, ending with one '\n'.
3
​
4
import sys
5
​
6
​
7
def solve(root_name, json_text):
8
    # TODO: implement.
9
    raise NotImplementedError("solve() not implemented")
10
​
11
​
12
def main():
13
    lines = sys.stdin.read().split('\n')
14
    t = int(lines[0])
15
​
16
    blocks = []
17
    for i in range(t):
18
        root_name = lines[1 + 2 * i]
19
        json_text = lines[2 + 2 * i]
20
        blocks.append(solve(root_name, json_text))
21
​
22
    sys.stdout.write('\n---\n'.join(blocks) + '\n')
23
​
24
​
25
if __name__ == '__main__':
26
    main()



3. Multi-Agent Drone Routing in a Temporal Urban Grid
1. Background
In the year 2026, urban logistics have fully transitioned to autonomous drone fleets. However, city regulations have grown increasingly complex. No-Fly Zones (NFZs) are now dynamic areas (e.g., around scheduled stadium events, VIP convoys, or construction sites) that activate and deactivate at specific times.

Your objective is to build a routing engine that manages a fleet of drones to successfully deliver packages while navigating these shifting constraints and optimizing limited battery life.

2. Problem Statement
You are provided with a 2D coordinate grid representing a city. You must develop a system that assigns and routes a fleet of N drones from a central warehouse to complete M deliveries.

Drones start at the warehouse, located at the center of the map: (map_size[0] / 2, map_size[1] / 2)
Each drone can carry multiple packages in a single trip, provided the total weight does not exceed the drone’s max_payload capacity
After completing deliveries, a drone must return to the warehouse or a charging station; mid-air stops are prohibited
All distances are Euclidean (straight-line)
Drones fly in straight lines between consecutive path points
Drones do not collide with one another; multiple drones may occupy the same coordinates simultaneously
3. Constants (Fixed for All Test Cases)
Drone speed: 1 distance unit per timestep
Battery capacity: 500 energy units (per drone, fully charged at start)
Charge rate: 2 energy units per timestep (at charging stations)
Input Format

Your program must accept a JSON file with the following structure:

{
  "map_size": [Width, Height],
  "drones": [
    {"id": "drone_1", "max_payload": 1.0},
    {"id": "drone_2", "max_payload": 0.8}
  ],
  "deliveries": [
    {"id": "d1", "x": 20, "y": 30, "weight": 0.3, "deadline": 200}
  ],
  "charging_stations": [
    {"x": 50, "y": 50, "slots": 2}
  ],
  "no_fly_zones": [
    {
      "shape": "circle",
      "center": [80, 80],
      "radius": 15,
      "T_start": 0,
      "T_end": 150
    },
    {
      "shape": "rectangle",
      "corners": [[120, 120], [140, 160]],
      "T_start": 50,
      "T_end": 300
    }
  ]
}
Field Definitions
map_size: [Width, Height] of the grid. Warehouse is located at (Width/2, Height/2)
drones: List of drones. Each drone includes:
id: Unique identifier
max_payload: Maximum carrying capacity
deliveries: List of delivery requests. Each includes:
id: Delivery identifier
x, y: Coordinates of delivery location
weight: Package weight
deadline: Latest allowable delivery time
charging_stations: List of charging stations:
x, y: Location of the station
slots: Number of drones that can charge simultaneously
no_fly_zones: List of NFZs:
Circle:
center: [x, y]
radius
Rectangle:
corners: [[x_min, y_min], [x_max, y_max]]
T_start and T_end: Active time window

Constraints

1 No-Fly Zones (NFZs)
NFZs are defined as circular or rectangular areas with a specific time window [T_start, T_end]
A drone cannot enter or pass through an NFZ while it is active
NFZs are known upfront; there are no surprise obstacles
A drone may pass through the same area when the NFZ is inactive
NFZ Collision During Transit:

Drones move in straight lines between consecutive path points at a speed of 1. A segment of length d takes d timesteps to traverse.

If a drone departs point A at time t₀ and travels toward point B (distance d), it reaches any intermediate point P at time:

t₀ + dist(A, P)
If an NFZ is active at point P at that time, the path is blocked
If the NFZ deactivates before arrival, the drone may pass through
Waiting Strategy:

If a path is blocked, the drone must wait at its current location
No battery is consumed while waiting
After deactivation, the drone resumes its path
Routing Options:

Detour around active NFZs using waypoints
Wait safely for the NFZ to deactivate
2 Energy Model
Energy consumed per leg is calculated as:

E_leg = distance × (1 + current_payload_weight)
current_payload_weight = total weight of packages on the drone
Payload decreases after deliveries, reducing energy cost
Battery levels must always remain ≥ 0
If a drone cannot complete a trip and return safely, it should not attempt it
3 Charging Stations
Charging stations have limited slots
If all slots are occupied, drones must wait (no battery usage)
Charging rate is 2 energy units per timestep
Drones may leave once sufficient charge is reached (full charge not required)
4 Deliveries & Deadlines
Each delivery has a strict deadline
Arrival must be on or before the deadline
Missed deadlines result in failure (no partial credit)
Packages are picked up at the warehouse and delivered in the field
5 Warehouse & Pickup Rules
PICKUP actions only occur at the warehouse
Upon return, drones are fully recharged to 500 energy units
Drones can make multiple trips:
Warehouse → Recharge → Pickup → Deliver → Repeat
6 Multi-Package Trips
Drones can carry multiple packages if total weight ≤ max_payload
Example route:
Warehouse → Delivery A → Delivery B → ... → Warehouse / Charging Station
Delivery order matters:
Dropping heavier packages first reduces energy costs for later legs
Output Format

Your program must produce a Flight Manifest as a JSON file:

{
  "flight_manifest": [
    {
      "drone_id": "drone_1",
      "path": [
        {
          "x": 50,
          "y": 50,
          "t": 0.0,
          "action": "PICKUP",
          "delivery_ids": ["d1", "d3"]
        },
        {
          "x": 20,
          "y": 30,
          "t": 42.4,
          "action": "DELIVER",
          "delivery_id": "d1"
        },
        {
          "x": 35,
          "y": 60,
          "t": 75.1,
          "action": "DELIVER",
          "delivery_id": "d3"
        },
        {
          "x": 50,
          "y": 50,
          "t": 92.0,
          "action": "RETURN"
        }
      ]
    }
  ]
}
Action Types
PICKUP: Drone picks up packages at the warehouse. Must include delivery_ids (list).
DELIVER: Drone delivers a package. Must include delivery_id.
CHARGE: Drone arrives at a charging station to recharge.
CHARGE_COMPLETE: Drone finishes charging and departs.
WAIT: Drone waits at its current position for an NFZ to deactivate.
WAYPOINT: Intermediate navigation point.
RETURN: Drone returns to warehouse or charging station (end of trip).
Scoring
Your solution is scored using a custom checker. The score formula is:

raw_score = (successful_deliveries × 100) − (total_energy × 0.1) − (makespan × 0.05)
Where:

successful_deliveries: Number of deliveries completed on time (arrived at destination ≤ deadline) without any constraint violations.
total_energy: Sum of energy consumed across all drone legs. Energy per leg = distance × (1 + current_payload_weight).
makespan: The latest timestamp in the entire flight manifest (i.e., when the last drone finishes).
Your score per test case is the raw_score. Higher is better. Invalid solutions (constraint violations) score 0. The leaderboard ranks by total score across all test cases.

Validation Rules (violations → score 0)
A drone's path must start with PICKUP and end with RETURN.
Time must be monotonically non-decreasing along each drone's path.
Travel time between consecutive points must equal distance / speed (speed = 1).
Battery must never go below 0.
Payload weight at any point must not exceed max_payload.
No drone path segment may pass through an active NFZ.
A delivery is only counted if the drone arrives at the exact delivery coordinates on or before the deadline.
Each delivery can only be delivered once.
Sample Input 0

{
  "map_size": [100, 100],
  "drones": [
    {"id": "drone_1", "max_payload": 1.0}
  ],
  "deliveries": [
    {"id": "d1", "x": 70, "y": 60, "weight": 0.3, "deadline": 200},
    {"id": "d2", "x": 30, "y": 80, "weight": 0.4, "deadline": 200}
  ],
  "charging_stations": [],
  "no_fly_zones": []
}
Sample Output 0

{
  "flight_manifest": [
    {
      "drone_id": "drone_1",
      "path": [
        {
          "x": 50,
          "y": 50,
          "t": 0.0,
          "action": "PICKUP",
          "delivery_ids": [
            "d1",
            "d2"
          ]
        },
        {
          "x": 70,
          "y": 60,
          "t": 22.36,
          "action": "DELIVER",
          "delivery_id": "d1"
        },
        {
          "x": 30,
          "y": 80,
          "t": 67.08,
          "action": "DELIVER",
          "delivery_id": "d2"
        },
        {
          "x": 50,
          "y": 50,
          "t": 103.14,
          "action": "RETURN"
        }
      ]
    }
  ]
}
Explanation 0

The drone picks up both packages (total weight 0.7), flies to d1 (distance ≈ 22.36), delivers d1, then flies to d2 (distance ≈ 44.72), delivers d2, and returns to the warehouse (distance ≈ 36.06). Both deliveries arrive well before the deadline of 200.

Successful deliveries: 2/2
Total energy: 22.36×1.7 + 44.72×1.4 + 36.06×1.0 ≈ 38.01 + 62.61 + 36.06 = 136.68
Makespan: 103.14
Raw score: (2×100) − (136.68×0.1) − (103.14×0.05) = 200 − 13.67 − 5.16 = 181.17
Sample Input 1

{
  "map_size": [200, 200],
  "drones": [
    {"id": "drone_1", "max_payload": 1.0}
  ],
  "deliveries": [
    {"id": "d1", "x": 10, "y": 100, "weight": 0.3, "deadline": 200.0},
    {"id": "d2", "x": 10, "y": 10, "weight": 0.3, "deadline": 350.0},
    {"id": "d3", "x": 100, "y": 10, "weight": 0.3, "deadline": 500.0}
  ],
  "charging_stations": [
    {"x": 100, "y": 10}
  ],
  "no_fly_zones": [
    {
      "shape": "circle",
      "center": [100, 55],
      "radius": 15,
      "T_start": 0.0,
      "T_end": 150.0
    }
  ]
}
Sample Output 1

{
  "flight_manifest": [
    {
      "drone_id": "drone_1",
      "path": [
        {
          "x": 100,
          "y": 100,
          "t": 0.0,
          "action": "PICKUP",
          "delivery_ids": [
            "d1",
            "d2",
            "d3"
          ]
        },
        {
          "x": 10,
          "y": 100,
          "t": 90.0,
          "action": "DELIVER",
          "delivery_id": "d1"
        },
        {
          "x": 10,
          "y": 10,
          "t": 180.0,
          "action": "DELIVER",
          "delivery_id": "d2"
        },
        {
          "x": 100,
          "y": 10,
          "t": 270.0,
          "action": "DELIVER",
          "delivery_id": "d3"
        },
        {
          "x": 100,
          "y": 10,
          "t": 270.0,
          "action": "CHARGE"
        },
        {
          "x": 100,
          "y": 10,
          "t": 281.0,
          "action": "CHARGE_COMPLETE"
        },
        {
          "x": 100,
          "y": 100,
          "t": 371.0,
          "action": "RETURN"
        }
      ]
    }
  ]
}
Explanation 1

The warehouse is at (100, 100). Delivery d3 is at (100, 10) — directly south. A circular NFZ with center (100, 55) and radius 15 sits between them on the line x=100, active from T=0 to T=150.

Why going directly to d3 first is invalid: The straight path from (100, 100) to (100, 10) passes through (100, 55) — the NFZ center. The drone would reach that point at approximately T=45, well within the NFZ's active window (T=0 to T=150). Any path segment crossing through this zone while it is active scores 0.

Route strategy — avoid the NFZ by timing: Instead of detouring around the NFZ with waypoints, the drone takes a route that naturally avoids it. It flies west to d1, south to d2, then east to d3. All three legs are far from the NFZ (closest approach is 45 units — well outside radius 15). By the time the drone needs to fly north through x=100 on the return leg (T=281), the NFZ has already expired (T=150). The drone passes through the formerly blocked area safely.

Why charging is needed: The total energy for all four legs is 522 units, which exceeds the battery capacity of 500. Conveniently, d3's location (100, 10) is also a charging station. After delivering d3 at T=270, the drone charges for 11 timesteps (22 energy at rate 2/timestep) to have enough battery (90 units) for the 90-unit return leg.

Leg-by-leg breakdown:

Warehouse (100,100) → d1 (10,100): distance = 90, payload = 0.9, energy = 90 × 1.9 = 171. Arrives T=90 ≤ deadline 200 ✓
d1 (10,100) → d2 (10,10): distance = 90, payload = 0.6, energy = 90 × 1.6 = 144. Arrives T=180 ≤ deadline 350 ✓
d2 (10,10) → d3 (100,10): distance = 90, payload = 0.3, energy = 90 × 1.3 = 117. Arrives T=270 ≤ deadline 500 ✓
Charge at (100,10): 11 timesteps, battery 68 → 90. Departs T=281.
d3 (100,10) → Warehouse (100,100): distance = 90, payload = 0, energy = 90 × 1.0 = 90. NFZ expired at T=150, drone passes through at T≈326 ✓
Score calculation:

Successful deliveries: 3/3
Total energy: 171 + 144 + 117 + 90 = 522
Makespan: 371
Raw score: (3×100) − (522×0.1) − (371×0.05) = 300 − 52.2 − 18.55 = 229.25
This example demonstrates three key concepts: NFZ avoidance (the drone cannot fly south early on), time-based NFZ expiry (the return path is safe because the NFZ deactivated), and charging station usage (the drone recharges mid-trip to complete the return).

Submissions: 14570
Max Score: 100
Difficulty: Advanced
Rate This Challenge:

    
More
 
1
# Start of HEAD
2
import json
3
import sys
4
import math
5
​
6
input_data = json.loads(sys.stdin.read())
7
​
8
map_size = input_data['map_size']
9
warehouse = [map_size[0] / 2, map_size[1] / 2]
10
drones = input_data['drones']
11
deliveries = input_data['deliveries']
12
no_fly_zones = input_data.get('no_fly_zones', [])
13
charging_stations = input_data.get('charging_stations', [])
14
# End of HEAD
15
​
16
# Start of BODY
17
def solve(warehouse, drones, deliveries, no_fly_zones, charging_stations):
18
    """
19
    Schedule drone deliveries to maximize on-time deliveries
20
    while minimizing energy and makespan.
21
​
22
    Args:
23
        warehouse: [x, y] - center of map, pickup/return location
24
        drones: list of {"id": str, "max_payload": float}
25
        deliveries: list of {"id": str, "x": float, "y": float, "weight": float, "deadline": float}
26
        no_fly_zones: list of {"shape": "circle"|"rectangle", "center"/"corners", "radius", "T_start", "T_end"}
27
        charging_stations: list of {"x": float, "y": float}
28
​
29
    Returns:
30
        list of drone entries, each: {"drone_id": str, "path": [steps]}
31
        Each step: {"x": float, "y": float, "t": float, "action": str, ...}
32
        Actions: PICKUP (+delivery_ids), DELIVER (+delivery_id), RETURN, CHARGE, CHARGE_COMPLETE, WAIT, WAYPOINT
33
​
34
    Scoring:
35
        score = (on_time_deliveries * 100) - (total_energy * 0.1) - (makespan * 0.05)
36
        energy per leg = distance * (1 + current_payload_weight)
37
        Battery capacity = 500, recharges on RETURN to warehouse
38
    """
39
    flight_manifest = []
40
​
41
    # TODO: Implement your solution here
42
​
43
    return flight_manifest
44
# End of BODY
45
​
46
# Start of TAIL
47
result = solve(warehouse, drones, deliveries, no_fly_zones, charging_stations)
48
output = {"flight_manifest": result}
49
print(json.dumps(output))
50
# End of TAIL
