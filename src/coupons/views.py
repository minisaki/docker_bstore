from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Coupon
from django.views import View

# Create your views here.


class CouponApply(View):
    def post(self, request):
        now = timezone.now()
        code_coupon = request.POST['coupon']
        if code_coupon:
            try:
                coupon = Coupon.objects.get(code__iexact=code_coupon,
                                            valid_from__lte=now,
                                            valid_to__gte=now, active=True)
                request.session['coupon_id'] = coupon.id
            except coupon.DoesNotExit:
                request.session['coupon_id'] = None

        return redirect('cart:cart_detail')