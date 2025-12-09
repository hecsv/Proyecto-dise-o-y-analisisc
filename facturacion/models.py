from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum, Case, When, F, DecimalField

from pacientes.models import Paciente
from citas.models import Cita

User = get_user_model()


class CuentaPaciente(models.Model):
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='cuenta'
    )
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cuenta de {self.paciente}"

    @property
    def saldo(self):
        agg = self.movimientos.aggregate(
            total=Sum(
                Case(
                    When(tipo=MovimientoCuenta.Tipo.CARGO, then=-F('monto')),
                    When(tipo=MovimientoCuenta.Tipo.ABONO, then=F('monto')),
                    default=Decimal('0.00'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
        )
        return agg['total'] or Decimal('0.00')


class MovimientoCuenta(models.Model):

    class Tipo(models.TextChoices):
        CARGO = "cargo", "Cargo (Deuda)"
        ABONO = "abono", "Abono (Pago/Favor)"

    cuenta = models.ForeignKey(
        CuentaPaciente,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=5, choices=Tipo.choices)
    fecha = models.DateTimeField(auto_now_add=True)
    concepto = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    cita = models.ForeignKey(
        Cita,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimientos_cuenta'
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimientos_creados'
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        signo = "-" if self.tipo == self.Tipo.CARGO else "+"
        return f"{self.concepto} ({signo}{self.monto})"


class Pago(models.Model):

    class Metodo(models.TextChoices):
        EFECTIVO = "efectivo", "Efectivo"
        TARJETA = "tarjeta", "Tarjeta"
        TRANSFERENCIA = "transferencia", "Transferencia"
        OTRO = "otro", "Otro"

    cita = models.ForeignKey(
        Cita,
        on_delete=models.PROTECT,
        related_name='pagos',
        null=True,
        blank=True
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='pagos'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=Metodo.choices)
    referencia = models.CharField(
        max_length=100,
        blank=True,
        help_text="Folio, referencia bancaria, etc."
    )
    notas = models.TextField(blank=True)

    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pagos_registrados'
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Pago {self.id} - {self.paciente} - ${self.monto}"


class Factura(models.Model):

    class Estatus(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        TIMBRADA = "timbrada", "Timbrada"
        CANCELADA = "cancelada", "Cancelada"

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='facturas'
    )
    pago = models.OneToOneField(
        Pago,
        on_delete=models.PROTECT,
        related_name='factura'
    )

    fecha_emision = models.DateTimeField(auto_now_add=True)
    serie = models.CharField(max_length=10, blank=True)
    folio = models.CharField(max_length=20, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    estatus = models.CharField(
        max_length=20,
        choices=Estatus.choices,
        default=Estatus.BORRADOR
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='facturas_creadas'
    )

    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.serie or self.folio:
            return f"Factura {self.serie}{self.folio} - {self.paciente}"
        return f"Factura {self.id} - {self.paciente}"
