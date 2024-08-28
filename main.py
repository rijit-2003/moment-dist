# Major Project Under S.M. Sir
# Moment Distribution


# import matplotlib.pyplot as plt

# Given data
L_AB = float(input("Enter length of span AB (meters): "))
L_BC = float(input("Enter length of span BC (meters): "))
load_type_AB = input("Enter load type for span AB (p for point load, u for UDL): ")
load_type_BC = input("Enter load type for span BC (p for point load, u for UDL): ")

M_AB = 0.0
M_BA = 0.0
M_BC = 0.0
M_CB = 0.0

# Step 1: Calculate Fixed End Moments (FEM) for AB
if load_type_AB == 'p':
    P = float(input("Enter point load P (kN): "))
    a = float(input("Enter distance a from A (meters): "))
    M_AB = -P * a * (L_AB - a) * (L_AB - a) / (L_AB ** 2)
    M_BA = P * a * a * (L_AB - a) / (L_AB ** 2)
elif load_type_AB == 'u':
    w = float(input("Enter UDL w (kN/m): "))
    M_AB = -w * L_AB ** 2 / 12.0
    M_BA = w * L_AB ** 2 / 12.0
else:
    print("Invalid load type for span AB.")
    exit(1)

# Step 2: Calculate Fixed End Moments (FEM) for BC
if load_type_BC == 'p':
    P = float(input("Enter point load P (kN): "))
    a = float(input("Enter distance a from B (meters): "))
    M_BC = -P * a * (L_BC - a) * (L_BC - a) / (L_BC ** 2)
    M_CB = P * a * a * (L_BC - a) / (L_BC ** 2)
elif load_type_BC == 'u':
    w = float(input("Enter UDL w (kN/m): "))
    M_BC = -w * L_BC ** 2 / 12.0
    M_CB = w * L_BC ** 2 / 12.0
else:
    print("Invalid load type for span BC.")
    exit(1)

# Step 3: Distribution Factors (Assuming equal stiffness for simplicity)
DF_BA = 0.5
DF_BC = 0.5

# Iterative Moment Distribution
unbalanced_moment_B = M_BA + M_BC
tolerance = 0.001  # Convergence criteria
carryover_A = 0.0
carryover_C = 0.0
n = 10

while n > 0:
    n -= 1
    # Distribute the unbalanced moment
    M_BA += DF_BA * unbalanced_moment_B * (-1)
    M_BC += DF_BC * unbalanced_moment_B * (-1)

    # Carryover moments to A and C
    carryover_A = -unbalanced_moment_B * DF_BA / 2.0
    carryover_C = -unbalanced_moment_B * DF_BC / 2.0

    # Update moments at A and C
    M_AB += carryover_A
    M_CB += carryover_C

    # Recalculate unbalanced moment at B
    unbalanced_moment_B = M_BA + M_BC

# Final Moments
print("Final Moments:")
print(f"M_AB (at A due to span AB): {M_AB} kNm")
print(f"M_BA (at B due to span AB): {M_BA} kNm")
print(f"M_BC (at B due to span BC): {M_BC} kNm")
print(f"M_CB (at C due to span BC): {M_CB} kNm")
