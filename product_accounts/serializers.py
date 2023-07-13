from rest_framework import serializers

from .models import Category, Product


# изменение и выдача готового файла после покупки
class AccountPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('account_file',)  # Делаем поле account_file только для чтения


# добавление аккаунтов в сужествующий продукт. в урлах по айдишнику
class AddingAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('account_file',)  # Делаем поле account_file только для чтения


# получение продукта
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('account_file',)


# получение категорий
# создание категории
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# создание продукта
class ProductCreateSerializer(serializers.ModelSerializer):
    account_file = serializers.FileField(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        account_file = validated_data.pop('account_file', None)
        validated_data['quantity'] = self.calculate_quantity(account_file)
        product = super().create(validated_data)

        if account_file:
            product.account_file.save(account_file.name, account_file)

        return product

    def calculate_quantity(self, account_file):
        if account_file:
            line_count = self.count_lines(account_file)
            return line_count
        return 0

    def count_lines(self, file):
        line_count = 0
        for _ in file:
            line_count += 1
        file.seek(0)  # Reset file pointer to the beginning
        return line_count
