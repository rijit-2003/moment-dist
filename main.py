# Major Project Under S.M. Sir
# Moment Distribution

import numpy as np
import matplotlib.pyplot as plt

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
    M_AB = -P * a * (L_AB - a) * (L_AB - a) / (L_AB ** 2)a
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


React_A = (P * (L_AB - a) - M_AB - M_BA) / L_AB
React_BA = 50-React_A
React_BC = (w*L_BC*L_BC*0.5-M_BC-M_CB)/L_BC
React_C = w*L_BC-React_BC

print("Reaction Forces:")
print(f"React_A (at A due to span AB): {React_A} kNm")
print(f"React_BA (at B due to span AB): {React_BA} kNm")
print(f"React_BC (at B due to span BC): {React_BC} kNm")
print(f"React_C (at C due to span BC): {React_C} kNm")

x_vals=[0,a,L_AB]
y_vals=[React_A,React_A-P,React_BC]
x=[L_AB,L_AB+L_BC]
y=[React_BC,-React_C]

figsize = (10,6)

plt.figure(figsize=figsize)
plt.step(x_vals,y_vals,where="post")
plt.plot(x,y)
plt.title("Shear Force Diagram\n")
plt.xlabel("Distance (m)")
plt.ylabel("Shear Force (kN)")
plt.grid(True)
plt.show()

#for free moments
# Line segment calculation
# Line passes through (0,0), (2,60), and (5,0)
# y = mx + c

# We can break this down into two segments: one from (0, 0) to (2, 60) and the other from (2, 60) to (5, 0)

# For (0,0) to (2,60)
m1 = 60 / 2  # slope
c1 = 0  # y-intercept

# For (2,60) to (5,0)
m2 = (0 - 60) / (5 - 2)  # slope
c2 = 60 - m2 * 2  # y-intercept

# Generating x values for the line segments
x_values_line_1 = np.linspace(0, 2, 200)
x_values_line_2 = np.linspace(2, 5, 200)

# Calculating y values for the line segments
y_values_line_1 = m1 * x_values_line_1 + c1
y_values_line_2 = m2 * x_values_line_2 + c2

# Parabola calculation (from previous code)
# Coefficients matrix
A = np.array([
    [25, 5, 1],
    [100, 10, 1],
    [56.25, 7.5, 1]
])

# Constants vector
B = np.array([0, 0, 75])

# Solving for [a, b, c]
coefficients = np.linalg.solve(A, B)
a, b, c = coefficients

# Generating x values for the parabola
x_values_parabola = np.linspace(5, 10, 400)
# Calculating y values for the parabola
y_values_parabola = a * x_values_parabola**2 + b * x_values_parabola + c

# Plotting the combined graph
plt.figure(figsize=(10, 6))

# Plot the line segments
plt.plot(x_values_line_1, y_values_line_1, color='blue', label='Line Segment 1')
plt.plot(x_values_line_2, y_values_line_2, color='green', label='Line Segment 2')

# Plot the parabola
plt.plot(x_values_parabola, y_values_parabola, color='red', label=f'Parabola Segment')

# Marking key points
plt.scatter([0, 2, 5, 7.5, 10], [0, 60, 0, 75, 0], color='black')

# Customizing plot
plt.title('Free Moment Diagram\n')
plt.xlabel('x-coordinate')
plt.ylabel('y-coordinate')
plt.grid(True)
plt.legend()
plt.show()


#end moments diagram
xs=[0,L_AB,L_AB+L_BC]
ys=[-M_AB,M_BA,M_CB]

plt.figure(figsize=figsize)
plt.plot(xs,ys)
plt.title('End Moment Diagram\n')
plt.xlabel('x-coordinate')
plt.ylabel('y-coordinate')
plt.grid(True)
plt.show()
