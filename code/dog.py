class DOG:
    def __init__(self,name,age):
      self.name = name
      self.age  = age
    def give_treat(self,whattreat):
      self.treat = whattreat
      print('licks his chops, slop slop farapp')
            
koko = DOG('Kokochek',7)

#if hasattr(koko,'name'):
#    print(koko.name)
    
#koko.give_treat('cheese')
if hasattr(koko,'treat'):
    print('Dog has received a treat.')
    print('It is:',koko.treat)
