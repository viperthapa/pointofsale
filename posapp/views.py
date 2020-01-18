from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import *
from .forms import *
from django.shortcuts import redirect,reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse, reverse_lazy
import json

# Create your views here.


#login form
class LoginView(FormView):
    template_name = 'login/login.html'
    form_class = LoginForm
    success_url = '/home/'
    

    def form_valid(self, form):

        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        print(uname,'88')


        user = authenticate(username=uname, password=pword)
        print(user,'3333333333')
        self.thisuser = user
        if user is not None and user.is_superuser:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {
                'error': 'Username you enter doesnot exist',
                'form': form
            })
        return super().form_valid(form)

  
#home view
class HomeView(TemplateView):
    template_name = 'admintemplates/adminhome.html'


#logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


#supplier list
class SupplierListView(TemplateView):
    template_name = 'supplier/supplierlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        return context

#supplier add
class SupplierCreateView(CreateView):
    template_name = 'supplier/supplieradd.html'
    form_class = SupplierForm
    success_url = reverse_lazy('posapp:supplierlist')


#supplier update
class SupplierUpdateView(UpdateView):
    template_name = 'supplier/supplierupdate.html'
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("posapp:supplierlist")

#supplier delete
class SupplierdeleteView(DeleteView):
    template_name = 'supplier/supplierdelete.html'
    model = Supplier
    success_url = reverse_lazy("posapp:supplierlist")



#customer list
class CustomerListView(TemplateView):
    template_name = 'customer/customerlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        return context



#sucustomer add
class CustomerCreateView(CreateView):
    template_name = 'customer/customeradd.html'
    form_class = CustomerForm
    success_url = reverse_lazy('posapp:customerlist')



#customer update
class CustomerUpdateView(UpdateView):
    template_name = 'customer/customerupdate.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy("posapp:customerlist")

#supplier delete
class CustomerdeleteView(DeleteView):
    template_name = 'customer/customerdelete.html'
    model = Customer
    success_url = reverse_lazy("posapp:customerlist")



#customer list
class ProductListView(TemplateView):
    template_name = 'product/productlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context




#sales create 
class SalesCreateView(FormView):
    template_name = 'sales/test.html'
    form_class = SalesCreateForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = SalesHistory.objects.all()  
        context['products'] = Product.objects.all()   

         
        # context['customers'] = Customer.objects.all()    
        return context
    


def CreateInvoiceView(request):
    if request.method == 'GET':
        return render(request, 'sales/customerform.html')
    else:
        cid = request.POST.get('name',None)
        customer = Customer.objects.get(customer=cid)
        products = list(Product.objects.all())
        

        # context = { 'cust' : customer.identity,
        #             'name' : customer.name,
        #             'balance' : customer.balance,
        #             'products': products, }
        return render(request, 'sales/test.html', {'customer': customer, 'products': products})



def orderBill(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        if data is None:
            raise AttributeError
        print(data)
        customer = Customer.objects.get(pk=data['customer_id'])
        # print('********',customer.id)
        order = Sales.objects.create(customer=customer,
                                    total_price=data['total_price'],
                                    )
        for product_id in data['product_ids']:
            OrderItem(product=Product.objects.get(pk=product_id), order=order).save()
        if data['total_price']:
            customer.save()
        order.save()
        return render(request, 'sales/orderbill.html')
