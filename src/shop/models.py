from django.db import models
from django.urls import reverse
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# from pyzbar.pyzbar import decode
# from PIL import Image

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    # def get_url(self):
    #     return reverse('shop:index', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='image/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_like', blank=True)
    quality = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.name

    def size_split(self):
        return self.size.split(',')

    def color_split(self):
        return self.color.split(',')

    def save(self, *args, **kwargs):
        qr = qrcode.make(f'{self.id}|{self.name}|{self.price}')
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr)
        fname = f'qr_code_{self.id}_{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        if self.qr_code == "":
            self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
        # self.qr_code.save(qr, save=False)


