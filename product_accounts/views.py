from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import generics, status
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
import codecs

from .models import Category, Product
from .serializers import CategorySerializer, ProductCreatSerializer, ProductListSerializer, AddingAccountsSerializer


# добавление аккаунтов в сужествующий продукт. в урлах во айдишнику
# class ChangingProductAfterPurchase(generics.RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def perform_update(self, serializer):
#         account_file = self.request.data.get('account_file')
#
#         if account_file:
#             # Получаем содержимое загруженного текстового файла
#             new_text = account_file.read().decode('utf-8')
#
#             # Открываем существующий текстовый файл и добавляем новое содержимое
#             with codecs.open(serializer.instance.account_file.path, 'a+', encoding='utf-8') as file:
#                 file.write(new_text.replace('\r\n', '\r'))
#
#             # Подсчет количества строк в новом файле
#             with codecs.open(serializer.instance.account_file.path, 'rb', encoding='utf-8') as file:
#                 line_count = sum(1 for _ in file)
#
#             serializer.instance.quantity = line_count
#         serializer.save()


# добавление аккаунтов в сужествующий продукт. в урлах во айдишнику
class AddingAccounts(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = AddingAccountsSerializer

    def perform_update(self, serializer):
        account_file = self.request.data.get('account_file')

        if account_file:
            # Получаем содержимое загруженного текстового файла
            new_text = account_file.read().decode('utf-8')

            # Открываем существующий текстовый файл и добавляем новое содержимое
            with codecs.open(serializer.instance.account_file.path, 'a+', encoding='utf-8') as file:
                file.write(new_text.replace('\r\n', '\r'))

            # Подсчет количества строк в новом файле
            with codecs.open(serializer.instance.account_file.path, 'rb', encoding='utf-8') as file:
                line_count = sum(1 for _ in file)

            serializer.instance.quantity = line_count
        serializer.save()


# получение продукта
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


# создание продукта
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreatSerializer


# создание категории
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# получение категорий
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
