from django.db import models

# Create your models here.
class Employee(models.Model):  

    #some comment here sss
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    department = models.ForeignKey( "Department" , on_delete = models.CASCADE , null=True, blank=True)
    branch = models.ForeignKey( "Branch" , on_delete = models.CASCADE , null=True, blank=True,)
    sort = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    joining = models.DateField( null=True)
    pph = models.FloatField(null=True,blank=True,default=0)
    pont = models.FloatField(null=True,blank=True,default=0)

    def get_full_name(self):
        return '%s %s'%(self.first_name,self.last_name)

    def __str__(self):
        return '%s %s'%(self.first_name,self.last_name)

class Branch(models.Model):
    id = models.CharField(primary_key=True,max_length=10,verbose_name="code")
    title = models.CharField(max_length=50,null=True)
    sort = models.IntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return self.title

class Department(models.Model):
    
    title = models.CharField(max_length=50,null=True)
    sort = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title



