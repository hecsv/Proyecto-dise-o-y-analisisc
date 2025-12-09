from django import forms
from .models import Proveedor, CategoriaProducto, Producto, MovimientoInventario


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "telefono", "email", "direccion", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "categoria",
            "proveedor",
            "codigo",
            "descripcion",
            "stock",
            "stock_minimo",
            "precio_compra",
            "precio_venta",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "proveedor": forms.Select(attrs={"class": "form-select"}),
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "stock_minimo": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "precio_compra": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "precio_venta": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["producto", "tipo", "cantidad", "motivo"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "motivo": forms.TextInput(attrs={"class": "form-control"}),
        }
