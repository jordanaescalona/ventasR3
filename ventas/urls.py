from django.urls import path
from .views import EntidadListView,EntidadView,EntidadDeleteView, eliminar_entidad,entidad_update, VendedorCreate2
from .views import VendedorListView,VendedorCreateView,VendedorDeleteView,VendedorUpdateView,eliminar_vendedor
from .views import borrar_imagen_entidad,editar_estado
from .views import crear_pdf

app_name = "ventas"

urlpatterns = [
    path('',EntidadListView.as_view(),name="listado"),
    path('entidad/',EntidadView.as_view(),name="nueva_entidad"),
    path('entidad/<int:pk>',entidad_update,name='modificar_entidad'),
    path('entidad/delete/<int:pk>',eliminar_entidad,name="eliminar_entidad"),
    path('entidad/nuevo_vendedor', VendedorCreate2.as_view(),name="nuevo_vendedor_entidad"), 
    path('entidad/editar_estado/<int:pk>',editar_estado,name="editar_estado"),

    path('nuevo_vendedor/',VendedorCreateView.as_view(),name="nuevo_vendedor"),   
    path('vendedores/',VendedorListView.as_view(),name="vendedores"),
    path('vendedores/delete/<int:pk>',eliminar_vendedor,name="eliminar_vendedor"),
    path('vendedor/edit/<int:pk>/',VendedorUpdateView.as_view(),name="editar_vendedor"),

    path('entidad/delete/imagen/<int:pk>',borrar_imagen_entidad,name="borrar_imagen_entidad"),
    path('pdf/<int:pk>',crear_pdf,name="pdf"),

]