import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import seaborn as sns
import datetime

plt.style.use('fivethirtyeight')
date_format = mdates.DateFormatter('%M:%S')

laps = pd.read_csv('./Datasets/lap_times.csv')
drivers = pd.read_csv('./Datasets/drivers.csv')
standings = pd.read_csv('./Datasets/driver_standings.csv')
races = pd.read_csv('./Datasets/races.csv')

df = pd.merge(pd.merge(races,laps,how='inner', on='raceId'), drivers,how='inner', on='driverId')
df = df.drop(['circuitId','driverId','forename', 'surname','url_y','url_x','nationality','dob','driverRef'],axis=1)
df.milliseconds = pd.to_datetime(df.milliseconds, unit= 'ms')

drivers_colors={
    'HAM':'#00D2BE', 'LEC':'#DC0000', 'TSU':'#2B4562', 'PER':'#0600EF', 'RIC':'#FF8700',
    'BOT':'#00D2BE', 'VER':'#0600EF', 'SAI':'#DC0000', 'RAI':'#900000', 'STR':'#006F62',
    'NOR':'#FF8700', 'RUS':'#005AFF', 'OCO':'#0090FF', 'GIO':'#900000', 'VET':'#006F62',  
    'MSC':'#FFFFFF', 'GAS':'#2B4562', 'LAT':'#005AFF', 'ALO':'#0090FF'
}

race = df[df.raceId==1052]
x=race.lap
codes= ["LEC",'HAM','VER','NOR']

lap_times = {}
for code in race.code.value_counts().index:
	if codes:
		if code in codes:
			lap_times[code] = race[race.code == code].milliseconds

def retrieve(i):

	plt.cla()
	for driver, lap_time in lap_times.items():
		plt.plot(x[:i+1],lap_time[:i+1], label=driver, color=drivers_colors[driver])

	plt.xlabel('Laps',fontsize= 14)
	plt.ylabel('Lap time',fontsize= 14)
	plt.title(f'{race.name.value_counts().index[0]} Lap times',fontsize= 14)

	plt.legend(loc= 'upper right', framealpha=1) ####### set the legend to upper right and disable transparancy

	plt.rc('lines', linewidth=2) # changethe linewidth of the plot
	
	plt.tick_params(axis = 'both', which = 'major', labelsize = 9) ##### change both axes labelsize 
	plt.gca().set_xticks(range(race.lap.min(),race.lap.max(),2)) ###### Change x-ticks to suit lap times
	plt.gca().yaxis.set_major_formatter(date_format) ###### change the date format of the y axis
	plt.ylim(race.milliseconds.min(), race.milliseconds.max()) ####### change y axis limits
	return 


def main():
	animation = FuncAnimation(plt.gcf(), retrieve, interval =1000)
	plt.show()

main()