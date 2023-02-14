from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #check if its a supply or sale, if its sale but the quantity is> than the product existing quantity do nothing
            #when done add to actions at last
            Productid=int(splittedline[0])
            quantity=int(splittedline[1])
            #check if its supply or sale
            if(quantity!=0):
                product=repo.products.find(id=Productid) #list of product parameters
                prod=product[0]
                OGquantity=prod.return_quantity()
                if(quantity<0):#then its a sale and i need to get the product quantity 
                    if(OGquantity+quantity>=0):#update the quantity and add actionzyy
                        data = {'quantity': OGquantity+quantity}
                        repo.products.update( Productid, data)
                        #adding action to actions
                        actionToAdd=Activitie(*splittedline)
                        repo.activities.insert(actionToAdd)

                if(quantity>0): #increase quantity and add action
                        data = {'quantity': OGquantity+quantity}
                        repo.products.update( Productid, data)
                        #adding action to actions
                        actionToAdd=Activitie(*splittedline)
                        repo.activities.insert(actionToAdd)
            
            

if __name__ == '__main__':
    main(sys.argv)