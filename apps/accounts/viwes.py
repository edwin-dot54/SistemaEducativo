from django.shortcuts import render


# Nota: este archivo fue creado para evitar que falte un módulo llamado `viwes`.
# A futuro, si se desea, se pueden agregar vistas reales y luego enlazarlas en urls.py.


def home(request):
    """Vista de ejemplo para la app accounts."""
    return render(request, "base.html")

