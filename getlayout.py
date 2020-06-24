import sys




def getLayouts(filepath, airspace=0):
	gamelayouts = []
	thefile = open(filepath, 'r')
	contents = thefile.read()
	levels = contents.split("\n\n")  # Splits the contents of the file by double linebreaks (paragraphs).
	color = str(levels.pop(0))  # Gets the color from the top of the file.
	gamelevels = []
	for level in levels:
		empty = True
		layout = []
		for i in range(airspace):
			layout.append(' ')
		rows = level.split('\n')  # Splits each "paragraph" (level) into rows by linebreaks.
		for row in rows:
			levelrow = []
			for char in row:
				levelrow.append(char)
				if char != ' ' and empty:
					empty = False
			layout.append(levelrow)
		if not empty:
			gamelevels.append(layout) # Makes sure empty levels don't get added to gamelevels.
	if not gamelevels[-1][-1]:
		del gamelevels[-1][-1]  # Deletes extra space at the end of list.
	thefile.close()
	return gamelevels, color



#print(getLayouts('world1'))
