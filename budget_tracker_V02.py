# IMPORTS
import datetime

# DATABASE
import sqlite3
db = sqlite3.connect('data/tracker_db')
db.execute("PRAGMA foreign_keys = 1") # Turns ON foreign key constraints
cursor = db.cursor()

# Creates table for categories
cursor.execute('''
               CREATE TABLE IF NOT EXISTS categories
               (id INTEGER PRIMARY KEY, 
               cat_name VARCHAR(100),
               budget DOUBLE(10, 2))
               ''')
db.commit()

# Creates table for expense transactions
cursor.execute('''
               CREATE TABLE IF NOT EXISTS expense
               (id INTEGER PRIMARY KEY, 
               Category VARCHAR(100),
               Description VARCHAR(100),
               Date DATE,
               Value DOUBLE(10, 2))
               ''')
db.commit()

# Creates table for income transactions
cursor.execute('''
               CREATE TABLE IF NOT EXISTS income
               (id INTEGER PRIMARY KEY, 
               Category VARCHAR(100), 
               Description VARCHAR(100),
               Date DATE,
               value DOUBLE(10, 2))
               ''')
db.commit()

# LISTS
cat_lst = [(8000,'BILLS'),
           (8001,'GROCERIES'),
           (8002,'TRANSPORT'),
           (8003,'EATING OUT'),
           (8004,'PERSONAL CARE'),
           (8005,'HOLIDAY'),
           (8006,'SALARY'),
           (8007,'TAX BENEFIT'),
           (8008,'OTHER INCOME'),
           (8009,'OTHER EPXENSE'),
           (8010,'SAVINGS')]

inc_list = [(5001,'SALARY','Pay Check',"2023-10-01",3650.10),
            (5002,'TAX BENEFIT','Child Tax',"2023-10-04",153.87)]

exp_lst = [(1001,'BILLS','Mortage',"2023-10-01",1250.36),
           (1002,'GROCERIES','Food Shop',"2023-10-06",110.58),
           (1003,'EATING OUT','Dinner Date',"2023-10-08",57.80),
           (1004,'SAVINGS','Monthly Saving',"2023-10-09",150.00)]

# Inserts list into relevant table
cursor.executemany('''INSERT INTO categories(id, cat_name)
                   VALUES(?,?)
                   ON CONFLICT (id) DO NOTHING''', cat_lst)

cursor.executemany('''INSERT INTO income(id, Category, Description, Date, value)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT (id) DO NOTHING''', inc_list)

cursor.executemany('''INSERT INTO expense(id, Category, Description, Date, Value)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT (id) DO NOTHING''', exp_lst)

# CLASSES
class Transaction:
    """
    Class for generation of transactions (Income and Expense)
    """
    def __init__(self):
        cat = cat_id_search()
        self.cat = cat[1]
        self.type = trans_type()
        self.description = input('Enter transaction description:  ')
        self.date = trans_date()
        self.value = trans_value()
   
    def __str__(self):
        return f'{self.cat}, {self.type}, {self.description}, {self.date}, {self.value}'
    
    def disp_transaction(self):
        print(f'''\nTransaction details entered:
Category:     {self.cat}
Type:         {self.type}
Description:  {self.description}
Date:         {self.date.strftime("%d-%m-%y")}
Value:        {self.value}
''')

# DICTIONARIES
homepage_dict = {1: 'Transactions (Income & Expense)',
                 2: 'Categories',
                 3: 'Budget & Financial Goals',
                 4: 'Reports',
                 0: 'Exit'}

sub_menu_dict = {1: 'Manage Transactions',
                 2: 'Manage Categories',
                 3: 'Reports',
                 0: 'Exit'}

action_menu_dict = {1: 'Add',
                    2: 'Amend',
                    3: 'Delete',
                    4: 'Search',
                    0: 'Exit'}

type_dict = {1: 'income',
             2: 'expense'}

# FUNCTIONS | GENERAL
def repeat_action():
    """
    User input to allow for previous action to be repeated.
    """
    repeat = input(f'{action_menu_dict[action_menu]} another record (Y/N)?  ').upper()
    while repeat not in ['Y', 'N']:
        print('Invalid entry.  Please enter "Y" or "N".')
        repeat = input(f'{action_menu_dict[action_menu]} another record (Y/N)?  ').upper()
    return(repeat)

def trans_date():
    """
    Valdiation of transaction dates and ensure user entry is standardised.
    """
    while True:
            while True:
                try:
                    select_date = int(input(f'''Select transaction date:
1.  Today's date ({datetime.date.today().strftime("%d-%m-%y")})
2.  Enter alternative date.

Select opiton:  '''))
                    break
                except ValueError:
                    print('Invalid entry.  Please retry...')
            if select_date == 1:
                return datetime.date.today()
            
            elif select_date == 2:
                while True:
                    try:
                        day = int(input('day DD: '))
                        month = int(input('month MM: '))
                        year = int(input('year YYYY: '))
                        
                        date = datetime.date(year=year, month=month, day=day)

                        print(date.strftime("%d-%m-%y"))
                        return date

                    except ValueError:
                        print('Invalid date entered, please retry...')

            else:
                print('Invalid Entry.  Please retry...')

def trans_value():
    """
    Ensure user input of transaction is always in float format.
    """
    while True:
        try:
            value = float(input('Enter transaction value:  '))
            return(value)
        except ValueError:
             print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...
                  ''')

def trans_type_opt():
    """
    Allows user to select the transaction type (income or expense).
    """
    while True:
        try:
            trans_type = int(input('''Confirm transaction type:
1. Income
2. Expense
                                   
Enter seletion:  '''))
            return(trans_type)
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...
                  ''')
                
def trans_type():
    """
    Ensures user entry is validated and provides standardised returns.
    """
    type = trans_type_opt()
    while type not in [1, 2]:
        print(f'\nInvalid Entry. Please try again...\n')
        type = trans_type_opt()

    if type == 1:
        return('income')
    
    elif type == 2:
        return('expense')
    
    else:
        print(f'\nInvalid Entry. Please try again...\n')
    
    return(type)

def conf_proceed(x):
    """
    Requires user to confirm they wish to proceed.  TO be used in conjunction
    with other functions or code.

    Args:
        x (str): transaction type.
    """
    proceed = input(f'''
Would you like to {(action_menu_dict[action_menu]).lower()} this {x} record (Y/N)?  ''').upper()
    
    while proceed not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            proceed = input(f' {(action_menu_dict[action_menu])} {x}  (Y/N)?  ').upper()
    return(proceed)

def convert_to_list(tuple_list, result=None):
    """Converts list of tuple into list.

    Args:
        tuple_list (str and int): Includes id, title, author and qty.
        result (extend, optional): Checks tuple length. Defaults to None.

    Returns:
        list: list of record details.
    """
    if result is None:
        result = []
    if len(tuple_list) == 0:
        return result
    else:
        result.extend(tuple_list[0])
        return convert_to_list(tuple_list[1:], result)


# FUNCTIONS | MENUES
def menu_return():
    """
    User input required to confrim that they are ready to return to menu
    option page.

    Returns:
        input: "Y" - confirmation to return to option menu.
    """
    ready = input('''\nPress "Y" to return to the option menu:  ''').upper()
    
    while ready not in ['Y']:
        print('''
** Invalid entry **
Please enter "Y" to return to the  menu.''')
        
        ready = input('''
Ready to return to the option menu?
(Press "Y" to continue):  ''').upper()
    else:
        return

def homepage_opt():
    """
    Homepage menu options
    """
    while True:
        try:
            homepage = int(input('''
-----------------------------
Budget Tracker App | Homepage
-----------------------------
Menu Options:
1.  Transactions | Income & Expense
2.  Categories
3.  Budget & Financial Goals
4.  Reports
0.  Exit
                     
Enter Option Number:  '''))
            return homepage
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...''')

def action_menu_opt(x):
    """
    Action menu options.  

    Args:
        x (str): to call previously selected menu option.
    """
    while True:
        try:
            action_menu = int(input(f'''
-----------------------------
{x} | Option Menu
-----------------------------
Menu Options:
1.  Add
2.  Amend
3.  Delete
0.  Exit
                     
Enter Option Number:  '''))
            return(action_menu)
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...''')

def report_menu_opt(x):
    """ Report menu options

    Args:
        x (str): to call previpus menu option selection.
    """
    while True:
        try:
            report_menu = int(input(f'''
-----------------------------
{x} | Option Menu
-----------------------------
Menu Options:
1.  View All Transactions
2.  Filter by Date Range
3.  Filter by Category
0.  Exit
                     
Enter Option Number:  '''))
            return report_menu
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...''')

def amend_menu_opt(x):
    """amend transaction menu options

    Args:
        x (str): to call previpus menu option selection.
    """
    while True:
        try:
            amend_opt = int(input(f'''
-----------------------------
{x} | Option Menu
-----------------------------
Menu Options:
1.  Amend Record (id required)
2.  Search & Amend
0.  Exit
                     
Enter Option Number:  '''))
            return amend_opt
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...''')

def budget_goals(x):
    """Budget & Goales menu options

    Args:
        x (str): to call previpus menu option selection.
    """
    while True:
        try:
            action_menu = int(input(f'''
-----------------------------
{x} | Option Menu
-----------------------------
Menu Options:
1.  Add Category Budget
2.  View Category Budget
3.  Add Financial Goal
4.  View Financial Goal
0.  Exit
                     
Enter Option Number:  '''))
            return(action_menu)
        
        except ValueError:
            print('''
** INVALID ENTRY **
Only numbers can be entered.  Please retry...''')
    pass

# FUNCTIONS | ADD TRANSACTIONS
def add_trans():
    """
    Checks previously entered user data and checks for potential duplicate
    transactions (income and expense)
    User input required to confirm new transaction.
    Functions ensures record is allocated to the correct table (income or 
    expense) based on user selection.
    """
    proceed = 'N'
    while True:
        new_trans = Transaction()
        new_trans.disp_transaction()
        tran_type = new_trans.type
        
        if tran_type == 'income':
            cursor.execute('''SELECT * FROM expense WHERE Category=? AND Date=? AND Value=?''', 
                        (new_trans.cat,
                        new_trans.date,
                        new_trans.value))
            
        elif tran_type == 'expense':
            cursor.execute('''SELECT * FROM expense WHERE Category=? AND Date=? AND Value=?''', 
                        (new_trans.cat,
                        new_trans.date,
                        new_trans.value))
            
        data = cursor.fetchall()
        data_list = [list(ele) for i,ele in enumerate(data)]
        if data:
            for record in data_list:
                print(f'''
The following record with similar data already exists:
Cat ID:       {record[0]}
Description:  {record[1]}
Date:         {record[2]} 
Value:        {record[3]}''')
        proceed = conf_proceed(tran_type)
        if proceed == 'Y': 
            if tran_type == 'income':
                cursor.execute('''INSERT INTO income(Category, Description, Date, Value)
                            VALUES(?,?,?,?)''',
                            (new_trans.cat, 
                            new_trans.description, 
                            new_trans.date, 
                            new_trans.value))
                db.commit()
            elif tran_type == 'expense':
                cursor.execute('''INSERT INTO expense(Category, Description, Date, Value)
                            VALUES(?,?,?,?)''',
                            (new_trans.cat, 
                            new_trans.description, 
                            new_trans.date, 
                            new_trans.value))
                db.commit()
            print('''
** New Transaction Added **
          ''')
            return(1)
        else:
            return(0)

def loop_add_trans():
    """
    While loop to allow user to add multiple transactions without returning to 
    menu options.
    """
    record_count = add_trans()
    repeat = repeat_action()

    while repeat != 'N':
        record_count += add_trans()
        repeat = repeat_action()
            
    print(f'''\n ** Upload Complete **
Records Processed:  {record_count}
''')


# FUNCTIONS | ADD TRANSACTIONS
def amend_cat(x_tran, x_type, id):
    """
    Specific function to amend transaction category for exisitng records.

    Args:
        x_tran (list): transaction details
        x_type (str): transaction type pre-selected by user.
        id (str): record ID
    """
    amend = input('Amend category (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend category (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current category: {x_tran[1]}')
            new = cat_id_search()
            new = (new[1])
            print(new)
            confirm = conf_proceed(x_type)

        if x_type == 'income':
            cursor.execute('''UPDATE income SET Category=? WHERE id=?''', (new, id))
            db.commit()

        elif x_type == 'expense':
            cursor.execute('''UPDATE expense SET Category=? WHERE id=?''', (new, id))
            db.commit()

        print('''
-----------------------------
Category Update Successful
-----------------------------
              ''')

    else:
        print('''
------------------------------
No changes made to Category
------------------------------
              ''')

def amend_desc(x_tran, x_type, id):
    """
    Specific function to amend transaction description for exisitng records.

    Args:
        x_tran (list): transaction details
        x_type (str): transaction type pre-selected by user.
        id (str): record ID
    """
    amend = input('Amend description (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend description (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current description: {x_tran[2]}')
            new = input('Enter new description:  ')
            confirm = conf_proceed(x_type)

        if x_type == 'income':
            cursor.execute('''UPDATE income SET Description=? WHERE id=?''', (new, id))
            db.commit()        
        elif x_type == 'expense':
            cursor.execute('''UPDATE expense SET Description=? WHERE id=?''', (new, id))   
            db.commit()

        print('''
-----------------------------
Description Update Successful
-----------------------------
              ''')

    else:
        print('''
------------------------------
No changes made to Description
------------------------------
              ''')

def amend_date(x_tran, x_type, id):
    """
    Specific function to update of transaction descriptons on exisitng records.
    """
    amend = input('Amend date (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend date (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'\nCurrent date: {x_tran[3].strftime("%d-%m-%y")}\n')
            new = trans_date()
            confirm = conf_proceed(x_type)

        if x_type == 'income':
            cursor.execute('''UPDATE income SET Date=? WHERE id=?''', (new, id))
            db.commit()        
        elif x_type == 'expense':
            cursor.execute('''UPDATE expense SET Date=? WHERE id=?''', (new, id))
            db.commit()

        print('''
-----------------------------
Date Update Successful
-----------------------------
              ''')

    else:
        print('''
------------------------------
No changes made to date
------------------------------
              ''')

def amend_value(x_tran, x_type, id):
    """
    Specific function to amend transaction value for exisitng records.

    Args:
        x_tran (list): transaction details
        x_type (str): transaction type pre-selected by user.
        id (str): record ID
    """
    amend = input('Amend transaction value (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend transaction value (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current value: {x_tran[4]}')
            new = trans_value()
            confirm = conf_proceed(x_type)

        if x_type == 'income':
            cursor.execute('''UPDATE income SET Value=? WHERE id=?''', (new, id))
            db.commit()
        
        elif x_type == 'expense':
            cursor.execute('''UPDATE expense SET Value=? WHERE id=?''', (new, id))
            db.commit()

        print('''
-----------------------------------
Transaction Value Update Successful
-----------------------------------
              ''')

    else:
        print('''
------------------------------------
No changes made to transaction value
------------------------------------
              ''')

def amend_trans(x_type):
    """
    Function to iterate through and each record field separately.

    Args:
        x_type (str): transaction type
    """
    select_conf = 'N'
                
    while select_conf != 'Y':
        inc_tran = id_search(x_type)
        id_selected = (inc_tran[0])
        select_conf = conf_proceed(x_type)

    # Functions called to allow user to update each record field.
    amend_cat(inc_tran, x_type, id_selected)    
    amend_desc(inc_tran, x_type, id_selected)
    amend_date(inc_tran, x_type, id_selected)
    amend_value(inc_tran, x_type, id_selected)

def amend_proceed(x_type):
    """User input to confirm they with to proceed with amendments.

    Args:
        x_type (str): transaction type
    """
    proceed = input(f'''
Would you like to proceed with amending a record (Y/N)?  ''').upper()
    
    while proceed not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            proceed = input(f'Proceed with amending a record (Y/N)?  ').upper()
    if proceed == 'Y':
        amend_trans(x_type)
    else:
        return()

def search_amend(x_type):
    """
    Menu options to allow user search and amend transactions.

    Args:
        x_type (str): transaction type
    """
    while True:
        try:
            search_menu = int(input('''
--------------------------------
Transaction Search | Option Menu
--------------------------------

Select from the following:
1.  View All
2.  Select Search Criteria
0.  Exit
                                                                                
Enter Option Number:  '''))
            if search_menu == 1:
                if x_type == 'income':
                    inc_print_all()
                    amend_proceed(x_type)

                elif x_type == 'expense':
                    exp_print_all()
                    amend_proceed(x_type)
    
            elif search_menu == 2:
                search_crit(x_type)
                amend_proceed(x_type)
            
            elif search_menu == 0:
                break

            else:
                print(f'\n** Invalid Entry. Please try again... **\n')
        
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')


# FUNCTIONS | DELETE TRANSACTIONS
def del_opt_menu():
    """
    User Input - select option from menu to determine method to identify and
    delete records from selected table.
    """
    while True:
        try:
            delete_opt = int(input('''\n 
-------------------------------------------------------------------------------
Delete Transactions | Menu Options
-------------------------------------------------------------------------------
1.  Delete Transaction (id required)
2.  Search and Delete
3.  Delete All Transactions
0.  Return to Menu
                       
Enter option number:  '''))
            return(delete_opt)
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

def id_del_trans():
    """ 
    Specific function to identify record by ID and delete associated record.

    """
    select_conf = 'N'
    while select_conf != 'Y':
        type = trans_type()
        proceed = del_proceed()

        if proceed == 'Y':
            del_tran = id_search(type)
            id_selected = int(del_tran[0])
            select_conf = input('''Is this the correct transaction for deleting?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()
            
            if type == 'income':
                cursor.execute('''DELETE FROM income WHERE id=?''', (id_selected,))
                db.commit()

            elif type == 'expense':
                cursor.execute('''DELETE FROM expense WHERE id=?''', (id_selected,))
                db.commit()
            print(f'''
----------------------------------------
{type} transaction successfully deleted
----------------------------------------
''')
        else:
            print(f'''
-------------------------------
No {type} transactions deleted
-------------------------------
''')
            break
        
def search_del_trans():
    """
    Allow user to search for and select a specific record for deletion.
    """
    select_conf = 'N'
    while select_conf != 'Y':
        type = trans_type()
        search_options(type)
        proceed = del_proceed()

        if proceed == 'Y':
            del_tran = id_search(type)
            id_selected = int(del_tran[0])
            select_conf = input('''Is this the correct transaction for deleting?
"Y" to continue
"N" to re-enter detials
Enter selection:  ''').upper()
            
            if type == 'income':
                cursor.execute('''DELETE FROM income WHERE id=?''', (id_selected,))
                db.commit()

            elif type == 'expense':
                cursor.execute('''DELETE FROM expense WHERE id=?''', (id_selected,))
                db.commit()
            print(f'''
----------------------------------------
{type} transaction successfully deleted
----------------------------------------
''')
        else:
            print(f'''
-------------------------------
No {type} transactions deleted
-------------------------------
''')
            break

def delete_all():
    """
    Deletes all records within selected table, but the table remains in existence.
    """
    delete_all = input('''
---------------
*** WARNING ***
---------------
You are about to delete all transactions from the selected data table.
Enter "Y" to continue.
Enter "N' to cancel and return to the main menu.
Are you sure you want to continue (Y/N):  ''').upper()
    while delete_all not in ['Y', 'N']:
        print('Invalid entry.  Please enter "Y" or "N".')
        delete_all = input('Are you sure you want to delete ALL records:  ').upper()

    if delete_all == 'Y':
        type = trans_type()

        if type == 'income':
            cursor.execute('''DELETE FROM income''')
            db.commit()

        elif type == 'expense':
            cursor.execute('''DELETE FROM expense''')
            db.commit()
        print(f'''
---------------------------------------
All {type} records successfully deleted
---------------------------------------
                      ''')
    else:
        menu_return()

def del_proceed():
    """
    User input to confirm that they wish to proceed with action.
    """
    proceed = input(f'''
Would you like to proceed with deleting a record (Y/N)?  ''').upper()
    
    while proceed not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            proceed = input(f'Proceed with deleting a record (Y/N)?  ').upper()

    return(proceed)

# FUNCTIONS | ADD CATEGORIES
def add_cat():
    """
    Allows user to add new category to relevant table.
    """
    proceed = 'N'
    while True:
        new_cat_name = input('Enter New Category Name:  ').upper()
        cursor.execute('''SELECT * FROM categories WHERE cat_name=?''', 
                        (new_cat_name,))
            
        data = cursor.fetchall()
        data_list = [list(ele) for i,ele in enumerate(data)]
        if data:
            for record in data_list:
                print(f'''
The following category with the same name already exists:
ID:        {record[0]}
Cat Name:  {record[1]}''')
        proceed = conf_proceed('category')
        if proceed == 'Y': 
            cursor.execute('''INSERT INTO categories(cat_name)
                            VALUES(?)''',
                            (new_cat_name,))
            db.commit()
            print('''
** New Category Added **
          ''')
            return(1)
        else:
            return(0)

def loop_add_cat():
    """
    Allow user to add multiple new categories without returning to menu options.
    """
    record_count = add_cat()
    repeat = repeat_action()

    while repeat != 'N':
        record_count += add_cat()
        repeat = repeat_action()
            
    print(f'''\n ** Upload Complete **
Records Processed:  {record_count}
''')

# FUNCTIONS | AMEND CATEGORIES
def amend_cat():
    """
    Allows user to amend pre-existing category name
    """
    cat = cat_id_search()

    amend = input('Amend category name (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Amend category (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            print(f'Current category: {cat[1]}')
            new = input("Enter new category name:  ").upper()
            confirm = conf_proceed('category')

        cursor.execute('''UPDATE categories SET cat_name=? WHERE id=?''', (new, cat[0]))
        db.commit()

        print('''
--------------------------------
Category Name  Update Successful
--------------------------------
              ''')

    else:
        print('''
--------------------------------
No changes made to Category Name
--------------------------------
              ''')

# FUNCTIONS | DELETE CATEGORIES
def del_cat():
    """
    Allows user to delete category from relevant table.
    A search will also be completed on income and expense tables to identify
    transactions assigned to the category selected for deletion.
    If transactions are assigned the user will not be able to delete 
    category.
    Only once all transactions are re-assigned will the user be able to delete
    the category.
    """
    cat = cat_id_search()

    del_cat = input('Delete category (Y/N):  ').upper()
    while del_cat not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        del_cat = input('Delete category (Y/N):  ').upper()

    if del_cat == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            cursor.execute('''SELECT * FROM income WHERE Category=?''', (cat[1],))
            inc_data = cursor.fetchall()
            data_list = [list(ele) for i,ele in enumerate(inc_data)]

            if inc_data:
                print(f'''
Expense transcations assigned to {cat[1]} category:''')
                
                for info in data_list:
                    print(f'''
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
---------------------------------------------''')
            else:
                print(f'''
** No Income transcations assigned to {cat[1]} **
''')
            
            cursor.execute('''SELECT * FROM expense WHERE Category=?''', (cat[1],))
            exp_data = cursor.fetchall()
            data_list = convert_to_list(exp_data)
            data_list = [list(ele) for i,ele in enumerate(exp_data)]

            if exp_data:
                print(f'''
Expense transcations assigned to {cat[1]} category:''')
                
                for info in data_list:
                    print(f'''
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
---------------------------------------------''')
            else:
                print(f'''
** No Expense transcations assigned to {cat[1]} **
''')  
            if exp_data or exp_data:
                print(f'''
*** ACTION REQUIRED ***
These records will need to be assigned new categories BEFORE {cat[1]} can be deleted.''')
                menu_return()
                print('''
---------------------------
Category Deletion Cancelled
---------------------------
              ''')
                break
            else:
                confirm = conf_proceed('category')

                cursor.execute('''DELETE FROM categories WHERE id=?''', (cat[0],))
                db.commit()

                print('''
----------------------------
Category Deletion Successful
----------------------------
              ''')

    else:
        print('''
---------------------------
Category Deletion Cancelled
---------------------------
              ''')

# FUNCTIONS | BUDGETS & GOALS
def cat_budget():
    """
    Allows user to assign a new budget to a specific category.
    """
    cat = cat_id_search()
    
    amend = input('Set category budget (Y/N):  ').upper()
    while amend not in ['Y', 'N']:
        print('\nInvalid entry. Please retry...\n')
        amend = input('Set category budget (Y/N):  ').upper()

    if amend == 'Y':
        confirm = 'N'
        while confirm != 'Y':
            set_budget = float(input('Enter budget value:  '))
            confirm = budget_proceed()

        cursor.execute('''UPDATE categories SET budget=? WHERE id=?''', (set_budget, cat[0]))
        db.commit()

        print('''
--------------------------------
Category Budget Set Successful
--------------------------------
              ''')

    else:
        print('''
----------------------
No Category Budget Set
----------------------
              ''')

def budget_proceed():
    """
    User input to confirm that they wish to proceed with action.
    """
    proceed = input(f'''
Would you like to proceed with setting a category budget (Y/N)?  ''').upper()
    
    while proceed not in ['Y','N']:
            print('Invalid entry.  Please enter "Y" or "N".')
            proceed = input(f'Proceed (Y/N)?  ').upper()

    return(proceed)

def view_budget():
    """
    Allows user to search for category and view specifc budget.  
    Function will return any associated income or expense transactions assigned
    to the category.
    User will be provided with net-performance vs. budget.
    """
    cat = cat_id_search()

    cursor.execute('''SELECT budget FROM categories WHERE id=?''', (cat[0],))
    data = cursor.fetchall()
    cat_budget = convert_to_list(data)
    cat_budget = float(cat_budget[0])

    print(cat_budget)

    cursor.execute('''SELECT value FROM income WHERE Category=?''', (cat[1],))
    data = cursor.fetchall()

    if not data:
        inc_value = 0

    else:
        cursor.execute('''SELECT SUM(value) FROM expense WHERE Category=?''', (cat[1],))
        data = cursor.fetchall()
        inc_value = convert_to_list(data)
        inc_value = float(inc_value[0])
    
    print(inc_value)

    cursor.execute('''SELECT value FROM expense WHERE Category=?''', (cat[1],))
    data = cursor.fetchall()

    if not data:
        exp_value = 0

    else:
        cursor.execute('''SELECT SUM(value) FROM expense WHERE Category=?''', (cat[1],))
        data = cursor.fetchall()
        exp_value = convert_to_list(data)
        exp_value = float(exp_value[0])    

    print(exp_value)

    performance = (cat_budget + inc_value - exp_value)

    print(f'''Budget Performance
Budget Target: {cat_budget}
Income:        {inc_value}
Expenditure:   {exp_value}
Net Total:     {performance}''')


# FUNCTIONS | REPORTS
def cat_print_all():
    """
    Printout of all categories table records terminal friendly format
    """
    cursor.execute('''SELECT * FROM categories''')
    data = cursor.fetchall()
    data_list = [list(ele) for i,ele in enumerate(data)]
    print('''ID   | Category Name''')
    for cat_info in data_list:
        print(f'''{cat_info[0]} | {cat_info[1]}''')

def cat_id_search():
    """
    user input - specific id.  
    Will check for ValueError 
    Will check if id exists in categories table.
    If id exists - prints specific record for categories table based on id.
    """
    while True:
        try:
            id = int(input(f'''
If category ID number known enter below.
Alternatively key "0" to see category list.

Enter Category ID:  '''))
            break
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

    cursor.execute('''SELECT * FROM categories
                    WHERE id=?''', (id,))

    data = cursor.fetchall()

    while not data:
        print(f'\n** No record found, please retry **\n')
        print(input('Press any key to view Cateogry list and make selection:  '))
        while True:
            try:
                print(f'Select ID from list below:\n')
                cat_print_all()
                id = int(input(f'\nEnter ID:  '))
                break
            except ValueError:
                print('Invalid entry.  Please re-enter a number.')
        
        cursor.execute('''SELECT * FROM categories
                        WHERE id=?''', (id,))
        data = cursor.fetchall()

    data_list = convert_to_list(data)
    print(f'''\nSelected Category Details:
Category ID:  {data_list[0]} | Name: {data_list[1]}
''')

    return(data_list)

def inc_print_all():
    """
    Printout of all income table records terminal friendly format
    """
    cursor.execute('''SELECT * FROM income''')
    data = cursor.fetchall()
    data_list = [list(ele) for i,ele in enumerate(data)]
    for info in data_list:
        print(f'''
ID:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-----------------------------------''')
        
def exp_print_all():
    """
    Printout of all expense table records terminal friendly format
    """
    cursor.execute('''SELECT * FROM expense''')
    data = cursor.fetchall()
    data_list = [list(ele) for i,ele in enumerate(data)]
    for info in data_list:
        print(f'''
ID:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-----------------------------------''')

# FUNCTIONS | SEARCHES
def id_search(x_type):
    """
    Allows user to carry out search based on transaction ID.
    When an invlade ID is provided, the user will be required to provide and 
    alternative.

    Args:
        x_type (str): transaction type
    """
    while True:
        try:
            id = int(input(f'\nEnter id:  '))
            break
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

    if x_type == 'income':
        cursor.execute('''SELECT * FROM income
                    WHERE id=?''', (id,))
        data = cursor.fetchall()
    
    elif x_type == 'expense':
        cursor.execute('''SELECT * FROM expense
                    WHERE id=?''', (id,))
        data = cursor.fetchall()
    
    while not data:
        print(f'\n** No record found, please retry **\n')
        while True:
            try:
                id = int(input(f'\nEnter id:  '))
                break
            except ValueError:
                print('Invalid entry.  Please re-enter a number.')

        if x_type == 'income':
            cursor.execute('''SELECT * FROM income
                        WHERE id=?''', (id,))
            data = cursor.fetchall()
    
        elif x_type == 'expense':
            cursor.execute('''SELECT * FROM expense
                        WHERE id=?''', (id,))
            data = cursor.fetchall()
    
    data_list = convert_to_list(data)
    print(f'''\nSelected record details:
id:          {data_list[0]}
Category:    {data_list[1]}
Description: {data_list[2]}
Date:        {data_list[3]}
Value:       {data_list[4]}
''')
    return(data_list)

def search_options(x_type):
    """
    Search options menu.
    Allows user to print all table records as well as search for specific
    records by certain criteria.  
    Income and Expense tables searchable.

    Args:
        x_type (str): transaction type
    """
    while True:
        try:
            search_menu = int(input(f'''
--------------------------------
{x_type} Search | Option Menu
--------------------------------

Select from the following:
1.  View All
2.  Select Search Criteria
0.  Exit Search
                                                                                
Enter Option Number:  '''))
            if search_menu == 1:
                if x_type == 'income':
                    inc_print_all()


                elif x_type == 'expense':
                    exp_print_all()

    
            elif search_menu == 2:
                search_crit(x_type)

            
            elif search_menu == 0:
                break

            else:
                print(f'\n** Invalid Entry. Please try again... **\n')
        
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

def search_crit(x_type):
    """Search criteria menu with relevant functions being called to carry 
    out search based on user input.

    Args:
        x_type (str): transaction type
    """
    while True:
        try:
            criteria = int(input(f'''
-----------------------------
{x_type} Search | Criteria
-----------------------------

Select search criteria:
1.  id
2.  Category
3.  Description
4.  Date
5.  Value
0.  Return Option Menu
                                                    
Enter option number:  '''))
            if criteria == 1: # id search
                id_search(x_type)

            elif criteria == 2: # Category search
                cat_search(x_type)

            elif criteria == 3: # Description search
                desc_search(x_type)

            elif criteria == 4: # Date search
                date_search(x_type)

            elif criteria == 5: # Value search
                value_search(x_type)

            elif criteria == 0: # Menu exit
                break
        
            else: # Input error handling
                print(f'\n** Invalid Entry. Please try again... **\n')
        
        except ValueError:
            print('Invalid entry.  Please re-enter a number.')

def cat_search(x_type):
    """
    Search function for income and expense tables based on user specified
    category.

    Args:
        x_type (str): transaction type.
    """
    cat = cat_id_search()

    if x_type == 'income':
        cursor.execute('''SELECT * FROM income
                    WHERE Category=?''', (cat[1],))
        data = cursor.fetchall()

        
    elif x_type == 'expense':
        cursor.execute('''SELECT * FROM expense
                    WHERE Category=?''', (cat[1],))
        data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found for {cat[1]}.\n')
        retry = input('Would you like to enter a different category (Y/N)?  ').upper()
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Enter a different category (Y/N)?  ')
        
        if retry == 'Y':
            cat = cat_id_search()

            if x_type == 'income':
                cursor.execute('''SELECT * FROM income
                            WHERE Category=?''', (cat[1],))
                data = cursor.fetchall()
        
            elif x_type == 'expense':
                cursor.execute('''SELECT * FROM expense
                    WHERE Category=?''', (cat[1],))
                data = cursor.fetchall()

        else:
            break

    data_list = [list(ele) for i,ele in enumerate(data)]

    # Loop to printout all rcords with specific title.
    for info in data_list: 
        print(f'''\nSelected transaction details:
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-------------------------------------------------''')
    menu_return()
    return(data_list)

def desc_search(x_type):
    """
    Search function for income and expense tables based on user specified
    description.

    Args:
        x_type (str): transaction type.
    """
    desc = input(f'\nEnter transaction description:  ')

    if x_type == 'income':
        cursor.execute('''SELECT * FROM income
                    WHERE Description=?''', (desc,))
        data = cursor.fetchall()
        
    elif x_type == 'expense':
        cursor.execute('''SELECT * FROM expense
                    WHERE Description=?''', (desc,)) 
        data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found for {desc}.\n')
        retry = input('Would you like to enter a different description (Y/N)?  ').upper()
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Enter a different description (Y/N)?  ')
        
        if retry == 'Y':
            desc = input(f'\nEnter transaction description:  ')

            if x_type == 'income':
                cursor.execute('''SELECT * FROM income
                            WHERE Description=?''', (desc,))
                data = cursor.fetchall()
        
            elif x_type == 'expense':
                cursor.execute('''SELECT * FROM expense
                            WHERE Description=?''', (desc,))
                data = cursor.fetchall()

        else:
            break

    data_list = [list(ele) for i,ele in enumerate(data)]

    # Loop to printout all rcords with specific title.
    for info in data_list: 
        print(f'''\nSelected transaction details:
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-------------------------------------------------''')
    menu_return()
    return(data_list)

def date_search(x_type):
    """
    Search function for income and expense tables based on user specified
    date range.

    Args:
        x_type (str): transaction type.
    """
    print('''You will be able to search over a date range.
To view a specific date enter in both "From Date" and "To Date".''')
    print(f'''
From Date
---------''')
    date_from = trans_date()
    print(f'''
To Date
---------''')
    date_to = trans_date()

    if x_type == 'income':
        cursor.execute('''SELECT * FROM income
                    WHERE Date BETWEEN ? AND ?''', (date_from, date_to,))
        data = cursor.fetchall()
        
    elif x_type == 'expense':
        cursor.execute('''SELECT * FROM expense
                    WHERE Date BETWEEN ? AND ?''', (date_from, date_to,))
        data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found between {date_from.strftime("%d-%m-%y")} and {date_to.strftime("%d-%m-%y")}.\n')
        retry = input('Would you like to enter different dates (Y/N)?  ').upper()
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Enter a different dates (Y/N)?  ')
        
        if retry == 'Y':
            print(f'''
From Date
---------''')
            date_from = trans_date()
            print(f'''
To Date
---------''')
            date_to = trans_date()

            if x_type == 'income':
                cursor.execute('''SELECT * FROM income
                            WHERE Date BETWEEN ? AND ?''', (date_from, date_to,))
                data = cursor.fetchall()
        
            elif x_type == 'expense':
                cursor.execute('''SELECT * FROM expense
                            WHERE Date BETWEEN ? AND ?''', (date_from, date_to,))
                data = cursor.fetchall()

        else:
            break

    data_list = [list(ele) for i,ele in enumerate(data)]

    # Loop to printout all rcords with specific title.
    for info in data_list: 
        print(f'''\nSelected transaction details:
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-------------------------------------------------''')
    menu_return()
    return(data_list)

def value_search(x_type):
    """
    SeaRch function for income and expense tables based on user specified
    transaction value range.

    Args:
        x_type (str): transaction type.
    """
    print('''You will be able to search over a value range.
          To view a specific value enter in both "From Value" and "To Value".''')
    
    print(f'''
From Value
---------''')
    value_from = trans_value()
    
    print(f'''
To Value
---------''')
    value_to = trans_value()

    if x_type == 'income':
        cursor.execute('''SELECT * FROM income
                    WHERE Value BETWEEN ? AND ?''', (value_from, value_to,))
        data = cursor.fetchall()
        
    elif x_type == 'expense':
        cursor.execute('''SELECT * FROM expense
                    WHERE Value BETWEEN ? AND ?''', (value_from, value_to,))   
        data = cursor.fetchall()
    
    while not data:
        print(f'\nNo record found between {value_from} and {value_to}.\n')
        retry = input('Would you like to enter different dates (Y/N)?  ').upper()
        
        while retry not in ['Y', 'N']:
            print('\nInvalid entry. Please retry...\n')
            retry = input('Enter a different dates (Y/N)?  ')
        
        if retry == 'Y':
            print(f'''
From Value
---------''')
            value_from = trans_value()
            print(f'''
To Value
---------''')
            value_to = trans_value()

            if x_type == 'income':
                cursor.execute('''SELECT * FROM income
                            WHERE Value BETWEEN ? AND ?''', (value_from, value_to,))
                data = cursor.fetchall()
        
            elif x_type == 'expense':
                cursor.execute('''SELECT * FROM expense
                            WHERE Value BETWEEN ? AND ?''', (value_from, value_to,))
                data = cursor.fetchall()

        else:
            break

    data_list = [list(ele) for i,ele in enumerate(data)]

    # Loop to printout all rcords with specific title.
    for info in data_list: 
        print(f'''\nSelected transaction details:
id:          {info[0]}
Category:    {info[1]}
Description: {info[2]}
Date:        {info[3]}
Value:       {info[4]}
-------------------------------------------------''')
    menu_return()
    return(data_list)

# PROGRAM
while True:
    homepage = homepage_opt()
    
    if homepage == 1: # Transactions
        action_menu = action_menu_opt(homepage_dict[homepage])
                        
        if action_menu == 1: # Add
            loop_add_trans()                
        
        elif action_menu == 2: # Amend
            amend_opt = amend_menu_opt(homepage_dict[homepage])
            
            if amend_opt == 1: # Amend with ID
                type = trans_type()
                amend_trans(type)

            elif amend_opt == 2: # Search & Amend
                type = trans_type()
                search_amend(type)
            
            elif amend_opt == 0: # Exit
                break

            else: # Input error
                print(f'\nInvalid Entry. Please try again...')

        elif action_menu == 3: # Delete
            del_opt = del_opt_menu()

            if del_opt == 1: # Delete transaction by ID
                id_del_trans()
            
            elif del_opt == 2: # Search & delete transaction
                search_del_trans()
            
            elif del_opt == 3: # Delete all record by table
                delete_all()

        elif action_menu == 0: # Exit
            break

        else: # Error
            print(f'\nInvalid Entry. Please try again...')

    elif homepage == 2: # Categories
        action_menu = action_menu_opt(homepage_dict[homepage])
                        
        if action_menu == 1: # Add
            loop_add_cat()
        
        elif action_menu == 2: # Amend
            amend_cat()

        elif action_menu == 3: # Delete
            del_cat()

        elif action_menu == 0: # Exit
            continue

        else:
            print(f'\nInvalid Entry. Please try again...')
     
    elif homepage == 3: # Budget & Financial Goals
        opt = budget_goals(homepage_dict[homepage])

        if opt == 1:  # Add Category Budget
            cat_budget()

        elif opt == 2: # View Category Budget
            view_budget()
            pass

        elif opt == 3: # Add Financial Goal
            pass

        elif opt == 4: # View Financial Goal
            pass

        elif opt == 0: # Exit
            pass

        else: # Error handling
            print(f'\nInvalid Entry. Please try again...')

    elif homepage == 4: # Reports
        type = trans_type()
        search_options(type)

    elif homepage == 0: # Exit Program
        #CLOSE 'budget' DB
        db.commit()
        db.close()
        print(f'''
-----------------------------
Connection to database closed
-----------------------------
              ''')
        exit()
     
    else:
        print(f'\nInvalid Entry. Please try again...')
        