import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# === FUNCTIONS ===

def load_mission_csv(file_path):
    """Load mission waypoints from CSV file."""
    df = pd.read_csv(file_path, skip_blank_lines=True)
    df.columns = df.columns.str.strip().str.lower()

    if "longitude" in df.columns and "latitude" in df.columns:
        waypoints = list(zip(df["longitude"], df["latitude"]))
    elif "x" in df.columns and "y" in df.columns:
        waypoints = list(zip(df["x"], df["y"]))
    else:
        raise ValueError(f"Columns not recognized in the CSV file: {df.columns.tolist()}")

    return waypoints

def calculate_total_distance(start, waypoints):
    """Calculate total round-trip distance of the mission."""
    total_distance = 0
    current_position = start
    for waypoint in waypoints:
        distance = np.linalg.norm(np.array(waypoint) - np.array(current_position))
        total_distance += distance
        current_position = waypoint
    total_distance += np.linalg.norm(np.array(current_position) - np.array(start))
    return total_distance

def find_nearest_waypoint(waypoints, drone_position=(0, 0)):
    """Find the index of the closest waypoint to the drone's position."""
    distances = [np.linalg.norm(np.array(wp) - np.array(drone_position)) for wp in waypoints]
    return np.argmin(distances)

def plot_paths(original_waypoints, optimized_waypoints):
    """Plot the original and optimized waypoint paths side-by-side."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- Original path ---
    x_orig, y_orig = zip(*original_waypoints)
    axes[0].plot(x_orig, y_orig, marker='o', linestyle='-', color='gray', label="Original Path")
    axes[0].scatter(x_orig[0], y_orig[0], color='orange', s=100, marker='s', label="Start")
    axes[0].set_title("Original Mission Path")
    axes[0].set_xlabel("X" if abs(x_orig[0]) < 100 else "Longitude")
    axes[0].set_ylabel("Y" if abs(y_orig[0]) < 100 else "Latitude")
    axes[0].legend()
    axes[0].grid(True)

    # --- Optimized path ---
    x_opt, y_opt = zip(*optimized_waypoints)
    axes[1].plot(x_opt, y_opt, marker='o', linestyle='-', color='blue', label="Optimized Path")
    axes[1].scatter(x_opt[0], y_opt[0], color='purple', s=100, marker='s', label="Optimal Start")
    axes[1].set_title("Optimized Mission Path")
    axes[1].set_xlabel("X" if abs(x_opt[0]) < 100 else "Longitude")
    axes[1].set_ylabel("Y" if abs(y_opt[0]) < 100 else "Latitude")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()

# === MAIN EXECUTION ===

if __name__ == "__main__":
    # 1. Load CSV path
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "waypoints_detailed.csv"))
    
    # 2. Load waypoints
    print("📌 Step 1: Loading CSV...")
    waypoints_original = load_mission_csv(csv_path)

    # 3. Calculate original total distance
    print("📌 Step 2: Calculating original distance...")
    original_distance = calculate_total_distance(waypoints_original[0], waypoints_original)

    # 4. Optimize path (reorder waypoints based on closest to (0,0))
    print("📌 Step 3: Finding optimal start point...")
    optimal_index = find_nearest_waypoint(waypoints_original, drone_position=(0, 0))
    optimized_waypoints = waypoints_original[optimal_index:] + waypoints_original[:optimal_index]
    
    print("📌 Step 4: Calculating optimized distance...")
    optimized_distance = calculate_total_distance(optimized_waypoints[0], optimized_waypoints)

    # 5. Estimate time assuming constant speed
    drone_speed = 5  # m/s
    original_time_sec = original_distance / drone_speed
    optimized_time_sec = optimized_distance / drone_speed
    time_saved = original_time_sec - optimized_time_sec

    # 6. Print results
    print("\n=== COMPARISON RESULTS ===")
    print(f"Original distance       : {original_distance:.2f} meters")
    print(f"Optimized distance      : {optimized_distance:.2f} meters")
    print(f"Original time estimate  : {original_time_sec:.2f} seconds")
    print(f"Optimized time estimate : {optimized_time_sec:.2f} seconds")
    print(f"⏱️  Estimated time saved  : {time_saved:.2f} seconds")

    # 7. Show both waypoint orders as table
    df_original = pd.DataFrame(waypoints_original, columns=["Longitude", "Latitude"])
    df_optimized = pd.DataFrame(optimized_waypoints, columns=["Longitude", "Latitude"])
    df_original["Order"] = "Original"
    df_optimized["Order"] = "Optimized"
    combined = pd.concat([df_original, df_optimized])
    
    print("\n--- Waypoint Order Comparison ---")
    print(combined.reset_index(drop=True).to_string(index=False))

    # 8. Plot both paths
    plot_paths(waypoints_original, optimized_waypoints)
