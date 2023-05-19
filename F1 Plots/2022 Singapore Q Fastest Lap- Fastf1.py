import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import fastf1
import fastf1.plotting


def setup_fastf1():
	fastf1.plotting.setup_mpl()
	fastf1.Cache.enable_cache("./cache")

def fetch_data(date=2022, race=1, session='Q'):
	session = fastf1.get_session(date, race, session)
	session.load()
	return session

def plot_formate():
	fig = plt.figure(figsize=(14,10), facecolor='#15151d')
	plt.rcParams['grid.color'] = '#444444'
	plt.style.use('seaborn')
	plt.style.use('dark_background')
	plt.rcParams['axes.facecolor'] = '#15151d'
	plt.rcParams['grid.color'] = '#444444'
	plt.rc('lines', linewidth=2)

	return fig

def animate(i, laps, colors, drivers, x, y):
	plt.cla()

	for index, lap in enumerate(laps):
		plt.plot(lap[x][1:i+1], lap[y][1:i+1], color = colors[index], label= drivers[index])
		try:
			plt.text(lap[x][i+1], lap[y][i+1], lap[y][i+1], color = colors[index], fontsize=10, fontweight='bold')
		except ValueError:
			pass

	plt.xlabel('Distance [m]', fontsize=16, color='#ffff55', fontweight='bold')
	plt.ylabel('Speed [km/h]',  fontsize=16, color='#ffff55', fontweight='bold')
	plt.title('Singapore Grand Prix - Fastest lap\nLeclerc VS Hamilton', color='#bbbbbb', fontsize=22, fontweight='bold')
	plt.yticks(fontsize=14, color='#ffff55')
	plt.xticks(fontsize=14, color='#ffff55')
	plt.legend(loc= 'upper right', labelcolor='linecolor',fontsize=12)
	plt.ylim(0,360)

def main():
	setup_fastf1()
	session = fetch_data(race='Singapore')
	drivers = ['LEC',"HAM"]
	x, y= 'Distance', "Speed"
	laps = [session.laps.pick_driver(driver).pick_fastest().get_car_data().add_distance() for driver in drivers]
	colors=  [fastf1.plotting.team_color(session.get_driver(driver).TeamName) for driver in drivers]
	animation = FuncAnimation(plot_formate(), animate , fargs=(laps, colors, drivers, x, y), interval =1)
	plt.show()

main()