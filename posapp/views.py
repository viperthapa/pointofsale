from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import *
from .forms import *
from django.shortcuts import redirect,reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse, reverse_lazy
import json
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import HttpResponse

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

     
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



#customer add
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


#product create
class ProductCreateView(CreateView):
    template_name = 'product/productadd.html'
    form_class = ProductForm
    success_url = reverse_lazy('posapp:productslist')


#product update
class ProductUpdateView(UpdateView):
    template_name = 'product/productupdate.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("posapp:productslist")


class ProductdeleteView(DeleteView):
    template_name = 'product/productdelete.html'
    model = Product
    success_url = reverse_lazy("posapp:productslist")



class SalesListView(TemplateView):
    template_name = 'sales/salescreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = Sales.objects.all()
        context['order'] = OrderItem.objects.order_by('-timestamp')

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
    

#create invoice 
def CreateInvoiceView(request):
    if request.method == 'GET':
        customerform = CustomerForms
        salesform = SalesCreateForm
        customer = Customer.objects.all()
        # print(customerform,"88888")
        return render(request, 'sales/customerform.html',{'customerform':customerform , 'salesform':salesform,'customer':customer})
    else:
        cid = request.POST.get('dropdown',None)
        print(cid,'|||||||||||||')
        customer = Customer.objects.get(customer=cid)
        products = list(Product.objects.all())
        if customer is not None:
            return render(request, 'sales/test.html', {'customer': customer, 'products': products})
        else:
            return messages.error(request, "Error!")




#order bill
def orderBill(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        if data is None:
            raise AttributeError
        print(data)
        customer = Customer.objects.get(pk=data['customer_id'])
        print(customer.email,'************')
        # print('********',customer.id)
        order = Sales.objects.create(customer=customer,
                                    total_price=data['total_price'],
                                    )
        for product_id in data['product_ids']:
            OrderItem(product=Product.objects.get(pk=product_id), order=order).save()
        if data['total_price']:
            customer.save()
        order.save()
        print(order.id)
        cus = customer.email
        subject, from_email, to = 'Greetings Messages', 'settings.EMAIL_HOST_USER', cus
        html_content = render_to_string('bill/emailmessage.html', {'customer':customer}) 
            # render with dynamic value
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_file('/home/ramthapa/Documents/djangoprojects/jobproject/static/email/logo.png')
        msg.attach_alternative(html_content, "text/html")
        # msg.mixed_subtype = 'related'
        # for f in ['logo.png']:
        #     fp = open(os.path.join(os.path.dirname("/home/ramthapa/Documents/djangoprojects/jobproject/static/email/logo.png"), f), 'rb')
        #     msg_img = MIMEImage(fp.read())
        #     fp.close()
        #     msg_img.add_header('Content-ID', '<{}>'.format(f))
        #     msg.attach(msg_img)

        msg.send()
        print('email succesfully send')

        return render(request, 'sales/orderbill.html', context={'id':order.id})


#bill generate
def BillGeneration(request, pk):
    """Generate pdf."""
    
    print(pk)
    sales = Sales.objects.get(id=pk)
    print(sales)
    order = OrderItem.objects.filter(order=sales)
    product = Product.objects.all()

    # Rendered
    html_string = render_to_string('bill/report.html', {'sales' : sales,'order' : order })
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=report.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

#chart 

class ChartView(TemplateView):
    template_name = 'reports/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = OrderItem.objects.all()
        context['sales'] = Sales.objects.all()

        return context
