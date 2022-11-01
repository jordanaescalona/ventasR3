from multiprocessing import context
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EntidadForm,VendedorForm,EstadoForm
from .models import Entidad, Imagen, Vendedor
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders
#marca de agua 
from PIL import Image,ImageDraw,ImageFont
FONT_PATH = "static/fonts/FiraMono-Bold.ttf"
FONT_SIZE = 25

# Create your views here.

#---------------ENTIDAD--------------------
class EntidadListView(ListView):
    template_name = "index.html"
    model = Entidad
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CONTENIDO GENERAL'
        
        return context

class EntidadView(View):

    def get(self,request,*args,**kgargs):
        form = EntidadForm
        entidades = Entidad.objects.all()
        context = {
            'form':form,
            'entidades':entidades
        }
        return render(request,'entidad.html',context)

    def post(self,request,*args,**kwargs):
        
        entidades = Entidad.objects.all()

        form = EntidadForm(request.POST,request.FILES)
        imagenes = request.FILES.getlist('imagen')

        if form.is_valid():
            nueva_entidad = form.save(commit=False)
            nueva_entidad.save()

            for i in imagenes:
                img = Imagen(imagen=i)
                
                img.save()
                nueva_entidad.imagen.add(img)
            
            nueva_entidad.save()

            messages.success(request,"Registro guardado exitosamente!")
            return redirect('ventas:listado')
        context ={
            'form':form
        }
        return render(request,'entidad.html',context)


class EntidadUpdateView(SuccessMessageMixin,UpdateView):
    model = Entidad
    """ fields = '__all__' """
    template_name = "entidad_edit.html"
    form_class = EntidadForm 
    success_url = reverse_lazy("ventas:nueva_entidad")
    success_message = "Registro modificado exitosamente!"

    def get_context_data(self,**kwargs):
        context = super(EntidadUpdateView,self).get_context_data(**kwargs)
        entidad = Entidad.objects.get(pk=self.kwargs.get('pk'))
        
        context['lista_imagenes'] = entidad.imagen.all()
        context['title'] = 'Editar registro'
        context['boton'] = 'Editar'
        
        return context


def entidad_update(request,pk):
    
    entidad = get_object_or_404(Entidad,pk=pk)
    
    form = EntidadForm(request.POST or None, request.FILES or None, instance=entidad)

    
    lista_imagenes = entidad.imagen.all()
    
    if request.method == "POST":
        
        if form.is_valid():
            
            entidad_new = form.save(commit=False)
            entidad_new.save()
            for i in request.FILES.getlist("imagen"):
                img = Imagen(imagen=i)
                img.save()
                entidad_new.imagen.add(img)
            entidad_new.save()
            messages.success(request,"Registro modificado exitosamente!")
            return redirect('ventas:listado')
        
    return render(request, 'entidad_edit.html', {
        'form': form,
        'lista_imagenes':lista_imagenes
        })

#Reemplazamos la vista basada en clase por la vista basada en funcion
class EntidadDeleteView(SuccessMessageMixin,DeleteView):
    model = Entidad
    template_name = "delete.html"
    success_url = success_url = reverse_lazy("ventas:listado")
    success_message = "Registro eliminado exitosamente"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar registro"
        
        return context

def eliminar_entidad(request,pk):
    template_name ="delete.html"
    entidad = get_object_or_404(Entidad,pk=pk)
    imagenes = entidad.imagen.all()
    
    if request.method == 'GET':
        context = {"entidad":entidad}
            
    if request.method == 'POST':
        print("imagenes:"+str(imagenes))
        for i in imagenes:
            i.imagen.delete()
            
            
        entidad.delete()
        messages.success(request,"Registro eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)

#----------PDF---------------------------
def images_url(uri,rel):
   
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

            # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

def crear_pdf(request,pk):
    template_path = 'pdf.html'

    entidad = Entidad.objects.get(pk=pk)
    context = {
        'entidad':entidad    
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="archivo.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,link_callback=images_url)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#--------------VENDEDORES-------------------------------------------------
class VendedorListView(ListView):
    template_name = "vendedores.html"
    model = Vendedor
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'LISTADO DE COMISIONISTAS'
        
        return context

class VendedorCreateView(SuccessMessageMixin,CreateView):
    model = Vendedor
    template_name = "vendedor.html"
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:vendedores")
    success_message = "Registro cargado exitosamente"
    error_message = "El comisionista que intenta agregar ya existe!"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NUEVO COMISIONISTA'
        context['boton'] = "GUARDAR"
        
        return context

class VendedorCreate2(SuccessMessageMixin,CreateView):
    model = Vendedor
    template_name = "vendedor_nuevo.html"
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:nueva_entidad")
    success_message = "Registro cargado exitosamente"
    error_message = "El comisionista que intenta agregar ya existe!"


class VendedorDeleteView(SuccessMessageMixin,DeleteView):
    model = Vendedor
    template_name = "delete_vendedor.html"
    success_url = success_url = reverse_lazy("ventas:vendedores")
    success_message = "Registro eliminado exitosamente!"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar Comisionista"
        
        return context

def eliminar_vendedor(request,pk):
    template_name ="delete_vendedor.html"
    vendedor = get_object_or_404(Vendedor,pk=pk)

    if request.method == 'GET':
        context = {"vendedor":vendedor}
    if request.method == 'POST':
        vendedor.delete()
        messages.success(request,"Comisionista eliminado exitosamente!")
        return HttpResponse("ok")
    return render(request,template_name,context)

class VendedorUpdateView(SuccessMessageMixin,UpdateView):
    model = Vendedor
    template_name = "vendedor.html"
    form_class = VendedorForm 
    success_url = reverse_lazy("ventas:vendedores")
    success_message = "Registro modificado exitosamente!"

    def get_context_data(self,**kwargs):
        context = super(VendedorUpdateView,self).get_context_data(**kwargs)
        
        context['title'] = 'EDITAR DATOS DE COMISIONISTA'
        context['boton'] = 'GUARDAR CAMBIOS'
        
        return context

#----------EXTRAS---------------
def borrar_imagen_entidad(request,pk):

    template_name = 'eliminar_imagen.html'
    img = get_object_or_404(Imagen,pk=pk)
    
    if request.method == 'GET':
        context = {"img":img}
    if request.method == 'POST':
        img.delete()
        return HttpResponse("ok")
        
    return render(request,template_name,context)


def editar_estado(request,pk):
    template_name = 'estado.html'
    entidad = get_object_or_404(Entidad,pk=pk)
    
    if request.method == 'GET':
        
        form = EstadoForm(instance=entidad)
        
        context = {"entidad":entidad,"form":form}
        
    if request.method == "POST":
        entidad.estado = request.POST.get('estado')
        
        form = EstadoForm(request.POST or None,request.FILES or None,instance=entidad)
        
        if form.is_valid():
            
            print("El formulario es valido")
            form.save()
            messages.success(request,"Estado modificado exitosamente!")
        else:
            print("El formulario no es valido")
        return HttpResponse("ok")
    
        
    return render(request,template_name,context)


