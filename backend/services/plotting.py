import matplotlib.pyplot as plt


def plot_points_vs_time(stats):
    fig, ax = plt.subplots()
    y_ticks = [0, 1000, 2000, 3000, 4000, 5000]
    times = []
    points = []
    for time, point in zip(stats['round_wise_time'], stats['round_wise_points']):
        if time < 150:
            times.append(time)
            points.append(point)
            
    ax.scatter(times, points, marker='.', color='b')
    ax.set_yticks(y_ticks)
    ax.set_xlabel('Round Time (s)')
    ax.set_ylabel('Points')
    ax.set_title('Points vs Time')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    return fig