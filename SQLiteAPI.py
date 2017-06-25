import sqlite3

class Database():
	def __init__(self, filepath):
		self.filepath = filepath
		self.conn = sqlite3.connect(self.filepath)
		self.cur = self.conn.cursor()
		
	def getTables(self):
		#returns a tuple list with all the table names from a given db connection
		self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		return self.cur.fetchall()
		
	def getColumns(self, table):
		#returns a tuple list with all the column names from a given db connection
		column_query = self.conn.execute('SELECT * from %s' % table)
		return [description[0] for description in column_query.description]
		
	def closeDBConnection(self):
		self.conn.close()
		
class EmployeeDatabase(Database):

	def createEmployeeDictionary(self):
		self.employeeDictionary = {'0000': 'All'}
		cursor = self.conn.execute("SELECT clk_no, employee_name FROM employee ORDER BY employee_name ASC")
		for row in cursor:
			key = str("%s" % row[0])
			value = str("%s" % row[1])
			self.employeeDictionary[key] = value
			
	def getEmployeeClockNumberString(self):
		keys = self.employeeDictionary.keys()
		keys.sort()
		employees = "Clk #\tEmployee"
		for key in keys:
			employees += '\n%s\t%s' % (key, self.employeeDictionary[key])
			
		return employees
		
		
class CategoryDatabase(Database):

	def getCategoryTables(self):
		continueIteration = True
		index = 0
		categoriesStr = "Abb\tCategories"
		while(continueIteration):
			index += 1
			table = self.TableDictionary.get(str(index),'no more keys')
			if table == 'no more keys':
				continueIteration = False
			else:
				categoriesStr += "\n%s\t%s" % (str(index), table)
		return categoriesStr
		
	def getTableColumns(self, tableAbbreviation):
		table = self.TableDictionary.get(tableAbbreviation, 'no table exists')
		
		if table != 'no table exists':
			columnTuple = self.getColumns(table)
			self.createColumnDictionary(columnTuple)
			continueIteration = True
			index = 0
			subcategoriesStr = "Category: %s\nSubcategories...\n\nAbb\tSubcategories" % table
			
			while(continueIteration):
				index += 1
				column = self.ColumnDictionary.get(str(index),'no more columns')
				if column == 'no more columns':
					continueIteration = False
				else:
					subcategoriesStr += "\n%s\t%s" % (str(index), column)
		else:
			subcategoriesStr = 'Invalid Category Abbreviation...\nType "help" for a list of commands or type "cat" to see the list of categories and their abbreviations.'
			
		return subcategoriesStr
		
	def createTableDictionary(self):
		self.TableDictionary = {}
		tablelist = ["SS_Installations", "SS_PM_Site_Visits", "SS_Rpr_Maint_Site_Visits", "SS_Rmt_Hrdwr_Spt", 
			"SS_Rmt_Sftwr_Spt", "SS_Rpr_Mant_RFB_in_House", "Miscellaneous", "SS_Doc_Gen", "SS_Inter_Dep_Spt", 
			"SS_Online_Training", "SS_Onsite_Training", "SS_In_House_Training", "Validation_Duties"]
		for index, table in enumerate(tablelist):
			self.TableDictionary[str(index + 1)] = str("%s" % table)
			
	def createColumnDictionary(self, columnTuple):
		self.ColumnDictionary = {}
		for index, column in enumerate(columnTuple[2:]):
			self.ColumnDictionary[str(index)] = str("%s" % column)
			
	def transformTableIntoTrendingTable(self, table, column, employeeClockNumber):
		pass
		
		
	def queryEntireCategoryAllEmployees(self, column):
		
		table_column = 'Name_Data_AllDaySums.%s' % column
		
		cursor = self.conn.execute("SELECT \
				SUBSTR(data_date,1,7), \
				SUM(%s) \
			FROM ( \
				SELECT \
					SS_Installations.data_date AS 'data_date', \
					SS_Installations.Installations_day_sum, \
					SS_PM_Site_Visits.PM_Site_Visits_day_sum, \
					SS_Rpr_Maint_Site_Visits.Inst_Repair_or_Maintenance_on_Site_day_sum, \
					SS_Rmt_Hrdwr_Spt.Rmt_Hardware_Support_day_sum, \
					SS_Rmt_Sftwr_Spt.Rmt_Software_Support_day_sum, \
					SS_Rpr_Mant_RFB_in_House.Inst_Repair_Maint_Rfb_In_House_day_sum, \
					Miscellaneous.Miscellaneous_day_sum, \
					SS_Doc_Gen.Document_Generation_day_sum, \
					SS_Inter_Dep_Spt.Inter_Dep_Spt_day_sum, \
					SS_Online_Training.Online_Training_day_sum, \
					SS_Onsite_Training.Onsite_Training_day_sum, \
					SS_In_House_Training.In_House_Training_day_sum, \
					Validation_Duties.Validation_Duties_day_sum \
				FROM \
					SS_Installations \
				INNER JOIN SS_PM_Site_Visits ON \
					SS_Installations.employee_clk_no = SS_PM_Site_Visits.employee_clk_no AND \
					SS_Installations.data_date = SS_PM_Site_Visits.data_date \
				INNER JOIN SS_Rpr_Maint_Site_Visits ON \
					SS_Installations.employee_clk_no = SS_Rpr_Maint_Site_Visits.employee_clk_no AND \
					SS_PM_Site_Visits.data_date = SS_Rpr_Maint_Site_Visits.data_date \
				INNER JOIN SS_Rmt_Hrdwr_Spt ON \
					SS_Installations.employee_clk_no = SS_Rmt_Hrdwr_Spt.employee_clk_no AND \
					SS_Rpr_Maint_Site_Visits.data_date = SS_Rmt_Hrdwr_Spt.data_date \
				INNER JOIN SS_Rmt_Sftwr_Spt ON \
					SS_Installations.employee_clk_no = SS_Rmt_Sftwr_Spt.employee_clk_no AND \
					SS_Rmt_Hrdwr_Spt.data_date = SS_Rmt_Sftwr_Spt.data_date \
				INNER JOIN SS_Rpr_Mant_RFB_in_House ON \
					SS_Installations.employee_clk_no = SS_Rpr_Mant_RFB_in_House.employee_clk_no AND \
					SS_Rmt_Sftwr_Spt.data_date = SS_Rpr_Mant_RFB_in_House.data_date \
				INNER JOIN Miscellaneous ON \
					SS_Installations.employee_clk_no = Miscellaneous.employee_clk_no AND \
					SS_Rpr_Mant_RFB_in_House.data_date = Miscellaneous.data_date \
				INNER JOIN SS_Doc_Gen ON \
					SS_Installations.employee_clk_no = SS_Doc_Gen.employee_clk_no AND \
					Miscellaneous.data_date = SS_Doc_Gen.data_date \
				INNER JOIN SS_Inter_Dep_Spt ON \
					SS_Installations.employee_clk_no = SS_Inter_Dep_Spt.employee_clk_no AND \
					SS_Doc_Gen.data_date = SS_Inter_Dep_Spt.data_date \
				INNER JOIN SS_Online_Training ON \
					SS_Installations.employee_clk_no = SS_Online_Training.employee_clk_no AND \
					SS_Inter_Dep_Spt.data_date = SS_Online_Training.data_date \
				INNER JOIN SS_Onsite_Training ON \
					SS_Installations.employee_clk_no = SS_Onsite_Training.employee_clk_no AND \
					SS_Online_Training.data_date = SS_Onsite_Training.data_date \
				INNER JOIN SS_In_House_Training ON \
					SS_Installations.employee_clk_no = SS_In_House_Training.employee_clk_no AND \
					SS_Onsite_Training.data_date = SS_In_House_Training.data_date \
				INNER JOIN Validation_Duties ON \
					SS_Installations.employee_clk_no = Validation_Duties.employee_clk_no AND \
					SS_In_House_Training.data_date = Validation_Duties.data_date \
				WHERE \
					(SS_Installations.Installations_day_sum != 0 OR \
					SS_PM_Site_Visits.PM_Site_Visits_day_sum !=0 OR \
					SS_Rpr_Maint_Site_Visits.Inst_Repair_or_Maintenance_on_Site_day_sum != 0 OR \
					SS_Rmt_Hrdwr_Spt.Rmt_Hardware_Support_day_sum != 0 OR \
					SS_Rmt_Sftwr_Spt.Rmt_Software_Support_day_sum != 0 OR \
					SS_Rpr_Mant_RFB_in_House.Inst_Repair_Maint_Rfb_In_House_day_sum != 0 OR \
					Miscellaneous.Miscellaneous_day_sum != 0 OR \
					SS_Doc_Gen.Document_Generation_day_sum != 0 OR \
					SS_Inter_Dep_Spt.Inter_Dep_Spt_day_sum != 0 OR \
					SS_Online_Training.Online_Training_day_sum != 0 OR \
					SS_Onsite_Training.Onsite_Training_day_sum != 0 OR \
					SS_In_House_Training.In_House_Training_day_sum != 0 OR \
					Validation_Duties.Validation_Duties_day_sum != 0)) Name_Data_AllDaySums \
			GROUP BY SUBSTR(data_date,1,7) \
			ORDER BY SUBSTR(data_date,1,7) ASC" % table_column)
			
		dataList = cursor.fetchall()
		for data in dataList:
			print data
			
	def queryEntireCategorySingleEmployee(self, column, employeeClockNumber):
		
		table_column = 'Name_Data_AllDaySums.%s' % column
		
		cursor = self.conn.execute("SELECT \
				SUBSTR(data_date,1,7), \
				SUM(%s) \
			FROM ( \
				SELECT \
					SS_Installations.data_date AS 'data_date', \
					SS_Installations.Installations_day_sum, \
					SS_PM_Site_Visits.PM_Site_Visits_day_sum, \
					SS_Rpr_Maint_Site_Visits.Inst_Repair_or_Maintenance_on_Site_day_sum, \
					SS_Rmt_Hrdwr_Spt.Rmt_Hardware_Support_day_sum, \
					SS_Rmt_Sftwr_Spt.Rmt_Software_Support_day_sum, \
					SS_Rpr_Mant_RFB_in_House.Inst_Repair_Maint_Rfb_In_House_day_sum, \
					Miscellaneous.Miscellaneous_day_sum, \
					SS_Doc_Gen.Document_Generation_day_sum, \
					SS_Inter_Dep_Spt.Inter_Dep_Spt_day_sum, \
					SS_Online_Training.Online_Training_day_sum, \
					SS_Onsite_Training.Onsite_Training_day_sum, \
					SS_In_House_Training.In_House_Training_day_sum, \
					Validation_Duties.Validation_Duties_day_sum \
				FROM \
					SS_Installations \
				INNER JOIN SS_PM_Site_Visits ON \
					SS_Installations.employee_clk_no = SS_PM_Site_Visits.employee_clk_no AND \
					SS_Installations.data_date = SS_PM_Site_Visits.data_date \
				INNER JOIN SS_Rpr_Maint_Site_Visits ON \
					SS_Installations.employee_clk_no = SS_Rpr_Maint_Site_Visits.employee_clk_no AND \
					SS_PM_Site_Visits.data_date = SS_Rpr_Maint_Site_Visits.data_date \
				INNER JOIN SS_Rmt_Hrdwr_Spt ON \
					SS_Installations.employee_clk_no = SS_Rmt_Hrdwr_Spt.employee_clk_no AND \
					SS_Rpr_Maint_Site_Visits.data_date = SS_Rmt_Hrdwr_Spt.data_date \
				INNER JOIN SS_Rmt_Sftwr_Spt ON \
					SS_Installations.employee_clk_no = SS_Rmt_Sftwr_Spt.employee_clk_no AND \
					SS_Rmt_Hrdwr_Spt.data_date = SS_Rmt_Sftwr_Spt.data_date \
				INNER JOIN SS_Rpr_Mant_RFB_in_House ON \
					SS_Installations.employee_clk_no = SS_Rpr_Mant_RFB_in_House.employee_clk_no AND \
					SS_Rmt_Sftwr_Spt.data_date = SS_Rpr_Mant_RFB_in_House.data_date \
				INNER JOIN Miscellaneous ON \
					SS_Installations.employee_clk_no = Miscellaneous.employee_clk_no AND \
					SS_Rpr_Mant_RFB_in_House.data_date = Miscellaneous.data_date \
				INNER JOIN SS_Doc_Gen ON \
					SS_Installations.employee_clk_no = SS_Doc_Gen.employee_clk_no AND \
					Miscellaneous.data_date = SS_Doc_Gen.data_date \
				INNER JOIN SS_Inter_Dep_Spt ON \
					SS_Installations.employee_clk_no = SS_Inter_Dep_Spt.employee_clk_no AND \
					SS_Doc_Gen.data_date = SS_Inter_Dep_Spt.data_date \
				INNER JOIN SS_Online_Training ON \
					SS_Installations.employee_clk_no = SS_Online_Training.employee_clk_no AND \
					SS_Inter_Dep_Spt.data_date = SS_Online_Training.data_date \
				INNER JOIN SS_Onsite_Training ON \
					SS_Installations.employee_clk_no = SS_Onsite_Training.employee_clk_no AND \
					SS_Online_Training.data_date = SS_Onsite_Training.data_date \
				INNER JOIN SS_In_House_Training ON \
					SS_Installations.employee_clk_no = SS_In_House_Training.employee_clk_no AND \
					SS_Onsite_Training.data_date = SS_In_House_Training.data_date \
				INNER JOIN Validation_Duties ON \
					SS_Installations.employee_clk_no = Validation_Duties.employee_clk_no AND \
					SS_In_House_Training.data_date = Validation_Duties.data_date \
				WHERE \
					(SS_Installations.Installations_day_sum != 0 OR \
					SS_PM_Site_Visits.PM_Site_Visits_day_sum !=0 OR \
					SS_Rpr_Maint_Site_Visits.Inst_Repair_or_Maintenance_on_Site_day_sum != 0 OR \
					SS_Rmt_Hrdwr_Spt.Rmt_Hardware_Support_day_sum != 0 OR \
					SS_Rmt_Sftwr_Spt.Rmt_Software_Support_day_sum != 0 OR \
					SS_Rpr_Mant_RFB_in_House.Inst_Repair_Maint_Rfb_In_House_day_sum != 0 OR \
					Miscellaneous.Miscellaneous_day_sum != 0 OR \
					SS_Doc_Gen.Document_Generation_day_sum != 0 OR \
					SS_Inter_Dep_Spt.Inter_Dep_Spt_day_sum != 0 OR \
					SS_Online_Training.Online_Training_day_sum != 0 OR \
					SS_Onsite_Training.Onsite_Training_day_sum != 0 OR \
					SS_In_House_Training.In_House_Training_day_sum != 0 OR \
					Validation_Duties.Validation_Duties_day_sum != 0) AND \
					SS_Installations.employee_clk_no = '%s') Name_Data_AllDaySums \
			GROUP BY SUBSTR(data_date,1,7) \
			ORDER BY SUBSTR(data_date,1,7) ASC" % (table_column, employeeClockNumber))
			
		dataList = cursor.fetchall()
		for data in dataList:
			print data
			
	def querySubcategoryAllEmployees(self, table, column):
		table_column = "%s.%s" % (table, column)
		cursor = self.conn.execute("SELECT \
				SUBSTR(%s.data_date,1,7) AS 'dateMonth', \
				SUM(%s) \
			FROM \
				%s \
			GROUP BY \
				dateMonth \
			ORDER BY \
				dateMonth ASC" % (table, table_column, table))
				
		dataList = cursor.fetchall()
		for data in dataList:
			print data
	
	def querySubcategorySingleEmployee(self, table, column, employeeClockNumber):
		table_column = "%s.%s" % (table, column)
		cursor = self.conn.execute("SELECT \
				SUBSTR(%s.data_date,1,7) AS 'dateMonth', \
				SUM(%s) \
			FROM \
				%s \
			WHERE \
				%s.employee_clk_no = '%s'\
			GROUP BY \
				dateMonth \
			ORDER BY \
				dateMonth ASC" % (table, table_column, table, table, employeeClockNumber))
				
		dataList = cursor.fetchall()
		for data in dataList:
			print data