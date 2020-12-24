from django.contrib import admin
from .models import Employee,Department,Branch,DummyModel
from django.urls import path
from django.utils.html import conditional_escape, format_html
from django.urls import reverse
from django.utils.http import urlencode
from .views import my_custom_view
from django.contrib import messages


# Register your models here.

class MyFilter(admin.SimpleListFilter):
    
    title = "Hourly Price"
    parameter_name = 'hourlyprice'
    def lookups(self, request, model_admin):
        return (
            ('lte_5',  '<=5'   ),
            ('lte_10', ' <= 10'),
            ('lte_15', ' <= 15'),
            ('lte_20', ' <= 20'),
            ('gte_25', ' > 20'),
        )

    def queryset(self, request, queryset):
        
        if self.value() == 'lte_5':
            return queryset.filter(pph__lte=5)
        elif  self.value() == 'lte_10':
            return queryset.filter(pph__lte=10)
        elif  self.value() == 'lte_15':
            return queryset.filter(pph__lte=15)
        elif  self.value() == 'lte_20':    
            return queryset.filter(pph__lte=20)
        elif  self.value() == 'gte_25':    
            return queryset.filter(pph__gte=25)
        
        return queryset


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    save_as = True
    #save_as_continue = False
    save_on_top = True

    # organizing fields in admin add/modify
    fieldsets=(
        ('Personal Data',{
            'fields':('first_name','last_name')
            
        }),
        ('Employment Data',{
            'fields':('branch','department','sort','pph','pont')
        }),
        
        ('Status',{
            'classes': ('wide', 'extrapretty'),
            'fields':('joining','active')
        }),
    )


    #radio_fields = {"branch": admin.HORIZONTAL}    
    autocomplete_fields = ['branch','department']
    
    # ordering list results
    ordering = ('branch','department','sort',)

    #filter
    list_filter = ('branch','department','pph',MyFilter)

    #display List
    list_display = ['display_full_name','display_branch_link','display_department_link','sort','pph','pont']
    
    list_editable = ('sort','pont','pph')

    search_fields = ('first_name','last_name','department__title')

    def display_full_name(self,obj):
        return "%s %s"%(obj.first_name,obj.last_name)
    display_full_name.short_description = 'Full Name'

    def display_branch_link(self,obj):
        #count = obj.branch.employee_set.count()
        url = (
            reverse("admin:app_employee_changelist")
            + "?"
            + urlencode({"branch__id__exact": f"{obj.branch.id}"})
        )
        return format_html('<a href="{}">{}</a>', url,obj.branch)
    display_branch_link.short_description = 'Branch'

    
    
    def display_department_link(self,obj):
        #count = obj.branch.employee_set.count()
        url = (
            reverse("admin:app_employee_changelist")
            + "?"
            + urlencode({"department__id__exact": f"{obj.department.id}"})
        )
        return format_html('<a href="{}">{}</a>', url,obj.department)
    display_department_link.short_description = 'Department'

    def save_model(self, request, obj, form, change):
        

        emp = Employee.objects.get(id=obj.id)
        print ('emp pph',emp.pph)
        print ('emp pont',emp.pont)
        print ('obj pph',obj.pph)
        print ('obj pont',obj.pont)


        # Secure Fields
        if change:

            if not request.user.has_perm('app.change_pph_employee') and obj.pph != emp.pph:
                obj.pph = emp.pph
                messages.add_message(request, messages.ERROR, 'لا يمكنك تعديل ساعة الموظف')
                
            if not request.user.has_perm('app.change_pont_employee') and obj.pont != emp.pont:
                obj.pont = emp.pont
                messages.add_message(request, messages.ERROR, 'لا يمكنك تعديل التبس')


        
        obj.user = request.user
        print('change pph', not request.user.has_perm('app.change_pph_employee'))
        print('change pont', not request.user.has_perm('app.change_pont_employee'))
        print ('obj',obj)

        super().save_model(request, obj, form, change)

        
    

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title','sort',)
    search_fields = ['title',]
    ordering=['sort',]
    

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('show_code','sort',)
    list_display_links = ('show_code',)
    search_fields = ['title',]
    ordering=['sort',]

    def show_code(self,obj):
        return "[%s] %s"%(obj.id,obj.title)
    show_code.short_description= "branch"



class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]
admin.site.register(DummyModel, DummyModelAdmin)