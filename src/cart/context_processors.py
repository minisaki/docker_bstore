from .cart import Cart


def cart_context_processors(request):
    cart = Cart(request)
    return {'cart': cart}
