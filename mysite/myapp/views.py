from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum
# Create your views here.
def index(request):
    if(request.method=="POST"):
        expense_form=ExpenseForm(request.POST)
        if(expense_form.is_valid()):
            expense_form.save()
    
    expense_form=ExpenseForm()
    expenses=Expense.objects.all()
    total_expense=expenses.aggregate(Sum('amount'))
    print(total_expense)
    #yearly expenses
    last_year=datetime.date.today()-datetime.timedelta(days=365)
    data=Expense.objects.filter(date__gt=last_year)
    yearly_expense=data.aggregate(Sum('amount'))
    #monthly expenses
    last_month=datetime.date.today()-datetime.timedelta(days=30)
    data_month=Expense.objects.filter(date__gt=last_month)
    monthly_expense=data_month.aggregate(Sum('amount'))
    #weekly expenses
    last_week=datetime.date.today()-datetime.timedelta(days=7)
    data_week=Expense.objects.filter(date__gt=last_week)
    weekly_expense=data_week.aggregate(Sum('amount'))


    daily_sums=Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    category_sums=Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expense':total_expense,
                                              'monthly_expense':monthly_expense,'weekly_expense':weekly_expense,'yearly_expense':yearly_expense,
                                              'daily_sums':daily_sums,'category_sums':category_sums})

def edit(request,id):
    expense=Expense.objects.get(id=id)
    
    if(request.method=='POST'):
        expense_form=ExpenseForm(request.POST,instance=expense)
        expense_form.save()
        return redirect('index')
    expense_form=ExpenseForm(instance=expense)

    return render(request,'myapp/edit.html',{'expense_form':expense_form})

def delete(request,id):
    if(request.method=='POST' and 'delete' in request.POST):
        expense=Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')