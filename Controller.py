from GUI import ConcoleGUI 
from SQLiteAPI import CategoryDatabase
from SQLiteAPI import EmployeeDatabase

class Controls():
	
	def __init__(self):
		self.gui = ConcoleGUI()
		runDescription = '''Generates a plot that shows the total number of hours for\n\t\ta given category\\sub-category per 7 day period.'''
		self.commandDict = {
			'exit': [self.exitProgram, "Exits the program."],
			'help': [self.basicInstructions, "Lists each command."],
			'emp': [self.getEmployeeClockNumberString, "Lists each employee & clock number."],
			'cat': [self.viewCategories, "Lists all categories and it's numerical abbreviation."],
			'scat': [self.viewSubcategories, "Lists all the subategories of a given category."],
			'run': [self.runDataTrend, runDescription],
			'ck': [self.test, 'check the whole column lib']
			}
		self.runProgram = True
		dbpath = 'C:\\ProgramData\\TimeTrax\\'
		
		self.catDB = CategoryDatabase("%sSepSci_cat.db" % dbpath)
		self.catDB.createTableDictionary()
		self.empDB = EmployeeDatabase("%sSepSci_emp.db" % dbpath)
		self.empDB.createEmployeeDictionary()
		
	def exitProgram(self):
		self.runProgram = False
		self.giveUserFeedback('Exiting Program...\nGoodbye')
		self.catDB.closeDBConnection()
		self.empDB.closeDBConnection()
		
	def run(self):
		return self.runProgram
		
	def runUserCommand(self, prompt):
		self.exectuteCommand(self.gui.userInput(prompt))
		
	def getRawUserInput(self, prompt):
		return self.gui.userInput(prompt)
		
	def giveUserFeedback(self, text):
		self.gui.concoleOutput(text)
	
	def basicInstructions(self):
		text = self.getCommandsWithDescriptions()
		self.giveUserFeedback(text)
		
	def getCommandsWithDescriptions(self):
		keyList = self.commandDict.keys()
		keyList.sort()
		commandString = 'Command\t\tDescription'
		for key in keyList:
			commandString += '\n%s\t\t%s' % (key, self.commandDict[key][1])
		
		return commandString
		
	def getEmployeeClockNumberString(self):
		text = self.empDB.getEmployeeClockNumberString()
		self.giveUserFeedback(text)
		
	def viewCategories(self):
		text = self.catDB.getCategoryTables()
		self.giveUserFeedback(text)
		
	def viewSubcategories(self):
		text = "Input the category abbreviation whose subcategories you'd like to plot."
		tableAbbreviation = self.getRawUserInput(text)
		text = self.catDB.getTableColumns(tableAbbreviation)
		self.giveUserFeedback(text)
		
		return tableAbbreviation
		
	def runDataTrend(self):
		# Get the category, sub-category (optional), and population that will be used to generate the querry.
		
		# Lists categories for easy selection
		self.viewCategories()
		categoryAbbreviation = self.viewSubcategories()
		
		# If bad cateogry abbreviation is entered, it kicks the user out of the method
		category = self.catDB.TableDictionary.get(categoryAbbreviation, False)
		if category != False:
			text = "Enter the sub-category abbreviation you'd like to plot.\nOr enter 0 to plot the whole category rather then a sub-category."
			subcategoryAbbreviation = self.getRawUserInput(text)
			
			subcategory = self.catDB.ColumnDictionary.get(subcategoryAbbreviation, False)
			
			
			# If bad sub-cateogry abbreviation is entered, it kicks the user out of the method
			if subcategory != False:
			
				if subcategoryAbbreviation == '0':
					subcategoryLabel = "None"
				else:
					subcategoryLabel = subcategory
			
				self.getEmployeeClockNumberString()
				text = "Finally, enter the Clock Number corresponding to the\nindividual(s) you'd like to be included in the plot."
				populationClockNumber = self.getRawUserInput(text)
				
				population = self.empDB.employeeDictionary.get(populationClockNumber, False)
				
				# If bad clock number is entered, it kicks the user out of the method
				if population != False:
				
					print "\n\nYou've entered the following querry parameters,\ndo you wish to accept and preceede?\n"
					print "category:", category
					print "subcategory:", subcategoryLabel
					print "subcategory:", subcategory
					print "Employee:", population
					
					#Give the user an oppertunity to abort
					if self.getRawUserInput('Type "y" to accept query parameters.').lower() == 'y':
						
						#Evalute the query parameters to define which query method to run
						if subcategoryLabel == "None":
							
							if populationClockNumber == '0000':
								# Entire category with all employees
								self.catDB.queryEntireCategoryAllEmployees(subcategory)
								
							else:
								# Entire category with single employee
								self.catDB.queryEntireCategorySingleEmployee(subcategory, populationClockNumber)
						
						else:
							
							if populationClockNumber == '0000':
								# Specific sub-category with all employees
								self.catDB.querySubcategoryAllEmployees(category, subcategory)
								
							else:
								# Specific sub-category with single employee
								self.catDB.querySubcategorySingleEmployee(category, subcategory, populationClockNumber)
								
					else:
						self.giveUserFeedback('Trending Plot Aborted')
				else:
					self.giveUserFeedback('Invalid Clock Number')
	
			else:
				self.giveUserFeedback('Invalid Sub-category Abbreviation')
	
	def test(self):
		print self.catDB.ColumnDictionary
		
	def exectuteCommand(self, command):
	
		function = self.commandDict.get(command.lower(), 'Invalid Command')
		
		if function != 'Invalid Command':
			function[0]()
		else:
			self.giveUserFeedback('Invalid Command\nFor a list of the commands type "help"')
		
app = Controls()
app.giveUserFeedback('\n\n\n\n\n\nWelcome to Time Trax Trending\nBelow is the list of commands.')
app.basicInstructions()

while(app.run()):
	app.runUserCommand("Enter Command")

	
	
	
	
	