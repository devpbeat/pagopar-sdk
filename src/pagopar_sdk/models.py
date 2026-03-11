"""Typed models used by the Pagopar SDK."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Sequence

NumberLike = int | float | Decimal | str


@dataclass(slots=True)
class Buyer:
    """Buyer data for `iniciar-transaccion`."""

    nombre: str
    email: str
    documento: str
    telefono: str
    ruc: str | None = None
    ciudad: str | None = None
    direccion: str = ""
    coordenadas: str = ""
    razon_social: str | None = None
    tipo_documento: str = "CI"
    direccion_referencia: str | None = None

    def to_payload(self) -> dict[str, Any]:
        """Return a JSON-serializable payload for Pagopar."""

        return {
            "ruc": self.ruc,
            "email": self.email,
            "ciudad": self.ciudad,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "documento": self.documento,
            "coordenadas": self.coordenadas,
            "razon_social": self.razon_social or self.nombre,
            "tipo_documento": self.tipo_documento,
            "direccion_referencia": self.direccion_referencia,
        }


@dataclass(slots=True)
class PurchaseItem:
    """Item row for `compras_items` in `iniciar-transaccion`."""

    id_producto: int | str
    nombre: str
    descripcion: str
    cantidad: int
    precio_total: NumberLike
    categoria: str | int
    ciudad: str | int
    url_imagen: str
    public_key: str | None = None
    vendedor_telefono: str = ""
    vendedor_direccion: str = ""
    vendedor_direccion_referencia: str = ""
    vendedor_direccion_coordenadas: str = ""

    def to_payload(self, default_public_key: str) -> dict[str, Any]:
        """Return a JSON-serializable payload for Pagopar."""

        return {
            "ciudad": str(self.ciudad),
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "categoria": str(self.categoria),
            "public_key": self.public_key or default_public_key,
            "url_imagen": self.url_imagen,
            "descripcion": self.descripcion,
            "id_producto": self.id_producto,
            "precio_total": self.precio_total,
            "vendedor_telefono": self.vendedor_telefono,
            "vendedor_direccion": self.vendedor_direccion,
            "vendedor_direccion_referencia": self.vendedor_direccion_referencia,
            "vendedor_direccion_coordenadas": self.vendedor_direccion_coordenadas,
        }


@dataclass(slots=True)
class StartTransactionRequest:
    """Request model for `/api/comercios/2.0/iniciar-transaccion`."""

    id_pedido_comercio: str | int
    monto_total: NumberLike
    tipo_pedido: str
    forma_pago: int | str
    comprador: Buyer
    compras_items: Sequence[PurchaseItem]
    fecha_maxima_pago: str
    descripcion_resumen: str = ""

    def to_payload(self, public_key: str) -> dict[str, Any]:
        """Return a JSON-serializable payload for Pagopar."""

        return {
            "comprador": self.comprador.to_payload(),
            "public_key": public_key,
            "monto_total": self.monto_total,
            "tipo_pedido": self.tipo_pedido,
            "compras_items": [item.to_payload(default_public_key=public_key) for item in self.compras_items],
            "fecha_maxima_pago": self.fecha_maxima_pago,
            "id_pedido_comercio": str(self.id_pedido_comercio),
            "descripcion_resumen": self.descripcion_resumen,
            "forma_pago": self.forma_pago,
        }
