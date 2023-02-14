from persistence import *

def main():
    #FIRST REQUIREMENT
    #print activities this by dates
    print('Activities')
    for activity in repo.activities.find_all_date():
     print(activity)
        
    #print branches all bellow and this by primary key ascending order
    print('Branches')
    for branche in repo.branches.find_all_Primary():
     print(branche)
    #print employees
    print('Employees')
    for employee in repo.employees.find_all_Primary():
     print(employee)
    #print products
    print('Products')
    for product in repo.products.find_all_Primary():
     print(product)
    #print suppliers
    print('Suppliers')
    for supplier in repo.suppliers.find_all_Primary():
     print(supplier)
    #SECOND REQUIREMENT
    repo.find_employees_report()
    #THIRD REQUIREMENT
    repo.find_activity_report()
    
    

if __name__ == '__main__':
    main()