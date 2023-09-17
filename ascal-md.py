# This script creates a Markdown file with the dates for my reconstructed calendar for the specified year.
# Created by Byron Pendason, 2022

from datetime import datetime
import ephem
# Be sure to install ephem with `pip install pyephem`. 

monthNames = ["Æfterra Ġēola", "Solmōnaþ", "Hreðmōnaþ", "Ēosturmōnaþ", "Þrimilcemōnaþ", "Ærra Liða", "Þriliða", "Æfterra Liða", "Weodmōnaþ", "Hāliġmōnaþ", "Wintermōnaþ", "Blōtmōnaþ", "Ærra Ġēola"];

# Tamworth is used as the reference point for certain calculations like sunset time.. You should be able to get a more local calendar by changing these coordinates to your own. North and East is positive, whereas South and West is negative 
loc = ephem.Observer()
loc.lat = "52.634289"
loc.lon = "-1.690710"
	
def is_intercalary(year):
	M = (year -3) % 19
	if M in [0, 3, 6, 8, 11, 14, 17, 19]:
		return True
	else:
		return False
def nextNewMoon(date):
	nm = ephem.next_new_moon(date)
	nm = getSunset(nm+1)
	while getMoonIllum(nm) < 1:
		nm = getSunset(nm+1)
	nm -= 1
	return nm
	
def nextFullMoon(date):
	return ephem.next_full_moon(date)
def getWinterSolstice(year):
	date = datetime(year, 12, 1)
	return ephem.next_solstice(date)
def getSummerSolstice(year):
	date = datetime(year, 6, 1)
	return ephem.next_solstice(date)
def getM(year):
	M = (year -3) % 19
	if M==0: M=19
	return M
def convertToDatetime(date, bod = False):
	edate = ephem.Date(date)
	c = edate.tuple()
	if bod:
		dtdate = datetime(c[0], c[1], c[2], 0, 0, 0)
	else:
		dtdate = datetime(c[0], c[1], c[2], c[3], c[4], int(c[5]))
	return dtdate
def returnDateString(date):
	dtdate = convertToDatetime(date)
#	return dtdate.isoformat()
	return dtdate.strftime("%Y-%m-%d")
def getSunset(date):
	loc.date = convertToDatetime(date, True)
	sun = ephem.Sun(loc)
	return loc.next_setting(sun)
def getMoonIllum(date):
	loc.date = convertToDatetime(date, True)
	moon = ephem.Moon(loc)
	return moon.phase

class Year:
	def __init__(self, year, ss, ws, nm, fm):
		self.year = year
		self.summer_solstice = ss
		self.winter_solstice = ws
		self.new_moons = nm
		self.full_moons = fm

if (True): # This was originally a for loop that constructed a YAML file with calendar data from the years 1900 to 2099. I was too lazy to un-indent all the lines when I made it to just calculate a md file for a selected year.
	yr = int(input("Type a year to construct a calendar for: "))
	fullMoons = []
	newMoons = []
	date = getWinterSolstice(yr-1)
	summer = getSummerSolstice(yr)
	winter = getWinterSolstice(yr)
	if is_intercalary(yr):
		m = 13
		leap_string = "Leap year"
	else:
		m = 12
		leap_string = "Regular year"
		monthNames.remove("Þriliða")
	for j in range(m):
		date = nextNewMoon(date)
		newMoons.append(returnDateString(date))
		date = nextFullMoon(date)
		fullMoons.append(returnDateString(date))
	easter = fullMoons[4]
	if is_intercalary(yr):
		winterf = fullMoons[10]
	else:
		winterf = fullMoons[9]

md= f"""# Reconstructed Anglo-Saxon Calendar for {yr}
Metonic Year {getM(yr)}: {leap_string}

## Months

| Month Name | Begins[^1] | Full Moon |
|:---------------|:-------------:|:------------:|
"""
for x in range(len(newMoons)):
	md += f"| {monthNames[x]} | {newMoons[x]} | {fullMoons[x]} |\n"
md += f"""
## Holidays

| Holiday | Date |
|:----------|:------:|
| Eosturdæg | {easter} |
| Midsumor | {summer} |
| Winterfylleþ | {winterf} |
| Yule | {winter} |

For information on this calendar, see [my blog](https://www.minewyrtruman.com/anglosaxoncalendar)
[^1]: Keep in mind that in the Anglo-Saxon Calendar, all days start at sunset the day before.
"""
fname = "ascal-"+str(yr)+".md"
f = open(fname, "w")
f.write(md)
f.close()

print(f"File saved at `./{fname}`.")
