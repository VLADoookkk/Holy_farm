from rest_framework import generics
from rest_framework.response import Response
import codecs
import chardet
from django.http import HttpResponse
from celery import shared_task

from .models import Category, Product
from .serializers import CategorySerializer, ProductCreateSerializer, ProductListSerializer, AddingAccountsSerializer, \
    AccountPurchaseSerializer


# изменение и выдача готового файла после покупки данные на вход "number_accounts": 10
@shared_task
def process_purchase(product_id, number_accounts):
    # Получаем объект Product
    product = Product.objects.get(id=product_id)

    # Получаем путь к файлу
    file_path = product.account_file.path

    # Определяем кодировку файла
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    file_encoding = result['encoding']

    # Открываем файл с определенной кодировкой
    with open(file_path, 'r', encoding=file_encoding) as file:
        file_content = file.read()

    # Получаем первые number_accounts строк
    lines = file_content.split('\n')
    selected_lines = lines[:number_accounts]

    # Создаем текстовое содержимое файла
    file_text = '\n'.join(selected_lines)

    # Удаляем выбранные строки из исходного файла
    with open(file_path, 'w', encoding=file_encoding) as file:
        file.write('\n'.join(lines[number_accounts:]))

    # Подсчет количества строк в обновленном файле
    line_count = sum(1 for _ in lines[number_accounts:])
    product.quantity = line_count

    # Сохраняем изменения в модели Product
    product.save()

    # Возвращаем файл в ответе
    response = HttpResponse(file_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{line_count}_{product.name}.txt"'
    return response


class ChangingProductAfterPurchase(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = AccountPurchaseSerializer

    def post(self, request, *args, **kwargs):
        number_accounts = request.data.get('number_accounts')
        product = self.get_object()

        if number_accounts is not None:
            # Выполняем задачу сразу в представлении
            response = process_purchase(product.id, number_accounts)
            return response

        return Response({'message': 'Invalid request'})


# добавление аккаунтов в сужествующий продукт. в урлах по айдишнику
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
    serializer_class = ProductCreateSerializer


# создание категории
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# получение категорий
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
