from django.shortcuts import render

class Carro:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
            self.carro = self.session["carro"]
        else:
            self.carro = carro

    def agregar(self, producto): 
        id = str(producto.idProducto)

        if id not in self.carro.keys():
            self.carro[id] = {
                "idProducto": producto.idProducto,
                "nombreProducto": producto.nombreProducto,
                "precio": int(producto.precio),
                "cantidad": 1,
                "imagen": producto.foto.url
            }
        else:
            for key, value in self.carro.items():
                if key == producto.idProducto:
                    value["cantidad"] = int(value["cantidad"])+1
                    value["precio"] = int(value["precio"])+producto.precio
                    break
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        producto.idProducto = str(producto.idProducto)
        if producto.idProducto in self.carro:
            del self.carro[producto.idProducto]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key, value in self.carro.items():
            if key == str(producto.idProducto):
                value["cantidad"] = int(value["cantidad"])-1
                value["precio"] = int(value["precio"])-producto.precio
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def vaciar_carro(self):
        carro = self.session["carro"] = {}
        self.session.modified = True

