from rest_framework import serializers
from .models import *
from users.models import User
from django.db.models import Q


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['user']

    def create(self, validated_data, user):
        category = Category(**validated_data)
        category.user = user
        category.save()
        return category


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data, user=None):
        data = validated_data.copy()
        category_data = data.pop('category')
        product = Product(**data)
        category = Category.objects.get(pk=category_data)
        product.category = category
        if user:
            product.user = user
        product.save()
        return product


class BillSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Bill
        fields = '__all__'


class BillFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        exclude = ['code', 'creator']

    def create(self, validated_data, creator):
        admin_info = self.context['request'].user
        validated_data = validated_data.copy()
        products_data = None
        if 'products' in validated_data:
            products_data = validated_data['products']
            validated_data.pop('products')
        user = User.objects.get(pk=validated_data['user'])
        validated_data.pop('user')

        bill = Bill(**validated_data)
        bill.user = user
        # for idx in validated_data:
        #     if idx == 'user':
        #         bill.user = User.objects.get(pk=validated_data['user'])
        #     elif idx == 'creator':
        #         bill.creator = User.objects.get(pk=validated_data['creator'])
        #     elif idx == 'products':
        #         pass
        #     else:
        #         setattr(bill, idx, validated_data[idx])
        # print(idx, validated_data[idx])
        bill.creator = creator
        bill.save()
        if products_data:
            products_id = list(map(
                lambda x: int(x['product']), products_data))
            numbers = list(map(lambda x: int(x['number']),
                               products_data))
            sellers_id = list(map(lambda x: int(
                x['seller']), products_data))
            sellers = User.objects.filter(
                id__in=sellers_id, admin=bill.creator)
            products = Product.objects.filter(id__in=products_id)
            c_products = products.count()
            c_sellers = sellers.count()
            c_numbers = len(numbers)
            # check products and sellers belongs to admin
            access_products = Product.objects.filter(Q(category__user=admin_info)
                                                     | Q(category__parent__user=admin_info)
                                                     | Q(category__parent__parent__user=admin_info)
                                                     | Q(user=admin_info)
                                                     ).values('id')
            set_access_products = set(map(lambda x: x['id'], access_products))
            access_sellers = User.objects.filter(
                admin=admin_info, groups__name='employee_user').values('id')
            set_access_sellers = set(map(lambda x: x['id'], access_sellers))
            if (c_numbers == c_products == c_sellers) and (len(set(products_id)-set_access_products) == 0) and (len(set(sellers_id)-set_access_sellers) == 0):
                for i in range(c_numbers):
                    bill.products.add(products[i], through_defaults={
                        'number': numbers[i], 'seller': sellers[i]})

        return bill

    def validate_user(self, value):
        if self.context['request'].user != value.admin and self.context['request'].user.admin != value.admin:
            raise serializers.ValidationError('user is not available')
        return value
