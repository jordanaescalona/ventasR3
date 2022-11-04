from django import forms
from .models import Entidad,Imagen,Vendedor

class EntidadForm(forms.ModelForm):
    
    
    imagen = forms.FileField(widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'multiple':True,
            'accept':'image/*'}),
            required = False
            )
    
    class Meta: 
        model = Entidad
        fields = '__all__'
        

        widgets ={
            'vendedor': forms.Select(attrs={
                'name':'vendedor',
                'id':'vendedor'
            })
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        
        #agregamos valor por default
        self.fields['vendedor'].empty_label = "---Seleccione Comisionista---"
        
        self.fields['descripcion'].label = "Descripción detallada:"
        self.fields['precio'].label = "Precio:"
        self.fields['imagen'].label = "Imágenes (Utilice ctrl + click para seleccionar las imagenes que desea agregar):"

class EstadoForm(forms.ModelForm):
    class Meta: 
        model = Entidad
        fields = ['estado',] 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class VendedorForm(forms.ModelForm):
    class Meta: 
        model = Vendedor
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })