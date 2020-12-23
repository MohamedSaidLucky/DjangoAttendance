from django.contrib import admin
from .models import Employee,Department,Branch

# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    # organizing fields in admin add/modify
    fieldsets=(
        ('Personal Data',{
            'fields':('first_name','last_name')
        }),
        ('Employment Data',{
            'fields':('branch','department','sort','pph','pont')
        }),
        ('Status',{
            'fields':('joining','active')
        }),
    )

    # ordering list results
    ordering = ['department','sort',]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    ordering=['sort',]

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('show_code','sort',)
    list_display_links = ('show_code',)
    ordering=['sort',]

    def show_code(self,obj):
        return "[%s] %s"%(obj.id,obj.title)
    show_code.short_description= "branch"
    
    
