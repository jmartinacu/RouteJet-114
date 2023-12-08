from django.shortcuts import get_object_or_404, render

from store.forms import AddProductForm
from store.cart import Cart
from .models import Product, Review
from .forms import ReviewForm


def product_detail(request, product_id, slug):
    cart = Cart(request)
    product = get_object_or_404(
        Product,
        id=product_id,
        slug=slug,
        available=True
    )
    form = AddProductForm(cart=cart, product=product)

    return render(request, 'product/detail.html', {
        'product': product,
        'form': form,
        'cart': cart,
    })


def rate(request, product_id, slug):
    cart = Cart(request)
    product = get_object_or_404(
        Product,
        id=product_id,
        slug=slug,
        available=True
    )
    user = request.user
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form2 = ReviewForm(request.POST)
        print(user)
        if request.user.is_anonymous:
            form2 = ReviewForm()
            return render(
                request,
                'product/review.html',
                {
                    'product': product,
                    'reviews': reviews,
                    'form2': form2,
                    'cart': cart
                }
            )
        if form2.is_valid():
            valoration = form2.cleaned_data['valoration']
            description = form2.cleaned_data['description']
            product_review = Review(
                user=user, product=product, valoration=valoration, description=description)
            product_review.save()
            reviews = Review.objects.filter(product=product)
    else:
        form2 = ReviewForm()

    return render(
        request,
        'product/review.html',
        {
            'product': product,
            'reviews': reviews,
            'form2': form2,
            'cart': cart
        })
