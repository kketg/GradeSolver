import sys
import json
import scipy.optimize as sci
import random

n = len(sys.argv)

if n != 2:
    print("Usage: python main.py <grade-file>")

filename = sys.argv[1]

with open(filename) as f:
    dict = json.loads(f.read())
    grades_d = dict["grades"]
    thresholds = dict["thresholds"]
    grades = [(g, float(grades_d[g]["percent"]), float(grades_d[g]["weight"])) for g in grades_d if 0 <= grades_d[g]["weight"] <= 100]
    weightsum = sum(g[2] for g in grades)
    if weightsum != 100:
        print("Weights must add up to 100")
        exit(1)

print("Grades")
for g in grades:
    print(f"{g[0]}:\t{(g[1] if 0 <= g[1] <= 100 else "____"):04}\t{g[2]}")
print("")

currentgrade = sum([(g[1]/100.0) * g[2] for g in grades if 0 <= g[1] <= 100.0])
print(f"Current Total: {currentgrade}")
print()

missinggrades = [(g[0], g[2]) for g in grades if g[1] < 0]

print("Missing Grades:")
for mg in missinggrades:
    print(f"{mg[0]}\t:    {mg[1]}")
print()

# x - Grades and their weights (name, weight)
# result - the final grade desired
def solve(x, result):
    minimize = [1] * len(x)
    
    def constraint(vars):
        return sum([x[i][1] * vars[i] for i in range(len(vars))]) + currentgrade - result
    def objective(vars):
        return sum(vars)
    minimal = sci.minimize(objective, minimize, bounds = [(0.0,1.0) for _ in range(len(x))], constraints=[{'type': 'eq', 'fun': constraint}], method='SLSQP')
    guesses = [[random.uniform(0.05,0.95) for _ in range(len(x))] for _ in range(3)]
    others = [
        sci.minimize(objective, guess, bounds = [(0.0,1.0) for _ in range(len(x))], constraints=[{'type': 'eq', 'fun': constraint}], method='SLSQP')
        for guess in guesses
    ]

    if minimal.success:
        return (minimal.x, [o.x for o in others if o.success])
    else:
        print(f"Error while solving equation: {minimal.message}")
        return [0 for _ in x]


for name in thresholds:
    val = float(thresholds[name])
    remaining_weights = sum([g[1] for g in missinggrades])
    if val > currentgrade + remaining_weights:
        print(f"\nGetting a(n) {name} ({val}) is impossible")
        continue
    if val <= currentgrade:
        continue

    (res, others) = solve(missinggrades, val)
    print(f"To get a(n) {name} ({val}):")
    print(f"\tYou need at minimum: ")
    for i in range(len(missinggrades)):
        n, weight = missinggrades[i]
        print(f"\t\t{n} ({weight}):\t{float(res[i]):.3f}")
    print(f"\tSome other possible results are: ")
    for i in range(len(others)):
        s = f"\t\t"
        for j in range(len(missinggrades)):
            n, weight = missinggrades[j]
            s += f"{n}: {float(others[i][j]):.3f}\t"
        print(s)
    print()