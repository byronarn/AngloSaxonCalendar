# This script will generate an Anglo-Saxon Calendar
# for the specified year. By default, it goes by UTC time
# but this can be changed by typing 'config' at the first
# command prompt.
#
# It follows Bede's 'On the Reckoning of Time' as closely
# as possible, but a couple assumptions had to be made
# because Bede didn't give us *quite* enough information.
# You can type 'help' at the first command prompt for more
# information.

# Imports
import datetime

#month names
months = ['Æfterra Gēola', 'Solmōnaþ', 'Hreþmonaþ','Ēastremōnaþ', 'Þrimilcemōnaþ', 'Ærra Liða', 'Þriliða', 'Æfterra Liða', 'Weodmōnaþ', 'Hāligmōnaþ', 'Wintermōnaþ', 'Blōtmōnaþ', 'Ærra Gēola']
#initialize moon arrays and holidays
newmoons = []
fullmoons = []
newyear = ''
easter = ''
midsummer = ''
winterfylleth = ''
yule = ''

#Other variables used
thrilitha = 1
tz = '0'
ascii = '0'

# try opening settings file of it exists, otherwise set default values
try:
	settingsf = open('settings.cfg', 'r')
	settings = settingsf.readlines()
	for i in settings:
		ilist = i.split()
		if ilist[0] == 'tz':
			tz = ilist[1]
		elif ilist[0] == 'ascii':
			ascii = ilist[1]
except FileNotFoundError:
	tz = '0'
	ascii = '0'

date_format = '%A %B %d, %Y'

year = input('Please input year, or type "help" for information, or \n"config" to change settings.\n> ')
if year.lower() == 'help':
	help = '\nThis program will create a reconstructed Anglo-Saxon\
	\ncalendar for the specified year. It follows Bede\'s \
	\n"Reckoning of Time" as closely as possible.\
	\n\
	\nEverything we know about the Anglo-Saxon calendar\
	\ncomes from Bede. He tells us it was lunisolar, meaning\
	\nthat it consisted of twelve lunar months with a leap month\
	\nadded every few years to keep it in line with the solar\
	\nyear.\
	\n\
	\nSince the majority of ancient cultures that followed a luni-\
	\nsolar calendar began their month with the first night that\
	\nthe young moon was visible, I estimate the beginning of the\
	\nmonth by adding 36 hours to the new moon data that was\
	\ncalculated. To determine whether or not to add\
	\nthe leap month to the year, I add it when there is thirteen\
	\nnew moons between the winter solstice of the previous\
	\nyear and the winter solstice of the current year. (For an\
	\nexample, check out the calendar for 2020.)\
	\n\
	\nMidsummer and Yule is placed on the summer and winter\
	\nsolstices, respectively. Ēastur and Winterfylleþ is placed\
	\non the full moon of the months of Ēasturmōnaþ and\
	\nWintermōnaþ, respectively.\
	\n\
	\nAll astronomical data (solstices, full and new moons) is\
	\ncalculated using algorithms from "Astronomical Algorithms".\
	\nBy default, all dates are applicable to UTC. You can change\
	\nthis by typing "config".\
	\n'
	if ascii == '1':
		help = help.replace('þ','th')
		help = help.replace('Ē', 'E')
		help = help.replace('ō', 'o')
	print(help)
	year = input('\nTo get your calendar, please input year.\n> ')

if year == 'config':
	print('\nTo reset to default, leave blank.')
	tz = input(f'Enter time zone as offset of UTC (i.e., EST=-5).\n[{tz}]> ')
	try:
		if int(tz) < -12 and int(tz) > 12:
			tz = '0'
	except:
		tz='0'
	ans = 'no'
	if ascii == '1':
		ans = 'yes'
	ascii = input(f'Do you want to display ascii characters instead of unicode? (yes/no)\n(Say yes if "þ" is not displaying correctly).\n[{ans}]> ')
	if ascii == 'yes' or ascii == 'y':
		ascii = '1'
	else:
		ascii = '0'
	settings = open('settings.cfg', 'w+')
	settings.write('tz '+tz+'\n')
	settings.write('ascii '+ascii)
	settings.close()
	year = input('\nPlease input year.\n> ')

# if year is out of range, use current year.	
if year.isdigit() and int(year) > 1000 and int(year) < 3000:
	print('')
else:
	print('The year must be a whole number between 1000 and 3000. Using current year instead.')
	year = datetime.datetime.now()
	year = year.strftime('%Y')
	
if ascii == '1':
	months = ['Efterra Geola', 'Solmonath', 'Hrethmonath','Eastremonath', 'Thrimilcemonath', 'Erra Litha', 'Thrilitha', 'Efterra Litha', 'Weodmonath', 'Haligmonath', 'Wintermonath', 'Blotmonath', 'Erra Geola']

# Get the dates for the solstices from the data files
# Data files are used so that the user need not deal
# with pip to install 'pymeeus''
decsolsf = open('decsols.dat', 'r')
junesolsf = open('junesols.dat', 'r')
tz = int(tz)

ds = decsolsf.readlines()
for i in ds:
	temp = datetime.datetime.strptime(i, '%b %d, %Y %H:%M ')
	if temp.strftime('%Y') == str(int(year)-1):
		newyear = temp + datetime.timedelta(hours=tz)
	if temp.strftime('%Y') == year:
		yule = temp + datetime.timedelta(hours=tz)
		break
js = junesolsf.readlines()
for i in js:
	temp = datetime.datetime.strptime(i, '%b %d, %Y %H:%M ')
	if temp.strftime('%Y') == str(year):
		midsummer = temp + datetime.timedelta(hours=tz)
		break

decsolsf.close()
junesolsf.close()

#Get the moons, again from data files
newmoonsf = open('newmoons.dat', 'r')
fullmoonsf = open('fullmoons.dat', 'r')
nm = newmoonsf.readlines()
fm = fullmoonsf.readlines()
index = 0

for i in nm:
	temp = datetime.datetime.strptime(i, '%b %d, %Y %H:%M ')
	if temp > newyear:
		index = nm.index(i)
		break

for i in range(0,13):
	temp = datetime.datetime.strptime(nm[index+i], '%b %d, %Y %H:%M ')
	newmoons.append(temp + datetime.timedelta(hours=tz+30))
	temp = datetime.datetime.strptime(fm[index+i], '%b %d, %Y %H:%M ')
	fullmoons.append(temp + datetime.timedelta(hours=tz))
	
newmoonsf.close()
fullmoonsf.close()

# if the thirteenth new moon is after Yule, it's not a leap year, so remove the leap month.
if newmoons[-1] >yule:
	newmoons.pop()
	fullmoons.pop()
	months.pop(6)
	thrilitha = 0

# Display the calendar on screen
easter = fullmoons[3]
winterfylleth = fullmoons[9+thrilitha]
print('\n')
print('==============================')
print(f'ANGLO-SAXON CALENDAR FOR {year}')
print('==============================')
print('')
if thrilitha == 1:
	print('(This year has thirteen new moons between the previous \
	\nDecember solstice and this year\'s December solstice.\
	\nTherefore, the leap month is added between the sixth and \
	\nseventh months.)\n')
print('====MONTHS====')
for i in months:
	n = months.index(i)
	print(f'{i} begins on {newmoons[n].strftime(date_format)}.')
print('')
print('====HOLY TIDES====')
if ascii == '1':
		print(f'Eastre is on {easter.strftime(date_format)}.')
else:
	print(f'Ēastre is on {easter.strftime(date_format)}.')
print(f'Midsumor is on {midsummer.strftime(date_format)}.')
if ascii == '1':
	print(f'Winterfylleth is on {winterfylleth.strftime(date_format)}.')
else:
	print(f'Winterfylleþ is on {winterfylleth.strftime(date_format)}.')
print(f'Modraniht (Yule) is on {yule.strftime(date_format)}.')

# Ask user if they wish to save the calendar, and do so if the answer is yes.
ans = input('\nDo you want to save this information to a file?(yes/no)\n> ')
if ans.lower() != 'yes':
	quit()
	
file = f'AngloSaxonCal{year}.txt'
f = open(file, 'w+')
f.write(f'==============================\n')
f.write(f'ANGLO-SAXON CALENDAR FOR {year}\n')
f.write(f'==============================\n')
f.write(f'')
if thrilitha == 1:
	f.write(f'(This year has thirteen new moons between the previous \
	December solstice and this year\'s December solstice. Therefore, \
	the leap month is added between the sixth and \
	seventh months.)\n')
f.write(f'\n====MONTHS====\n')
for i in months:
	n = months.index(i)
	f.write(f'{i} begins on {newmoons[n].strftime(date_format)}.\n')
f.write(f'\n====HOLY TIDES====\n')
if ascii == '1':
		f.write(f'Eastre is on {easter.strftime(date_format)}.\n')
else:
	f.write(f'Ēastre is on {easter.strftime(date_format)}.\n')
f.write(f'Midsumor is on {midsummer.strftime(date_format)}.\n')
if ascii == '1':
	f.write(f'Winterfylleth is on {winterfylleth.strftime(date_format)}.\n')
else:
	f.write(f'Winterfylleþ is on  {winterfylleth.strftime(date_format)}.\n')
f.write(f'Modraniht (Yule) is on {yule.strftime(date_format)}.\n')
f.close()
print(f'File has been saved as "{file}"!')
quit()