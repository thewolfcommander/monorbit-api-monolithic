from rest_framework import serializers

from network.serializers import NetworkCategorySerializer, ShowNetworkSerializer
from accounts.serializers import UserMiniSerializer
from .models import *


class ProductDefaultCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDefaultCategory
        fields = [
            'id',
            'network_category',
            'name',
            'image'
        ]

    
class ProductDefaultCategoryShowSerializer(serializers.ModelSerializer):
    network_category = NetworkCategorySerializer(read_only=True)
    class Meta:
        model = ProductDefaultCategory
        fields = [
            'id',
            'network_category',
            'name',
            'image'
        ]


class ProductCustomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCustomCategory
        fields = [
            'id',
            'name',
            'image'
        ]


class ProductDefaultSubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDefaultSubCategory
        fields = [
            'id',
            'category',
            'name',
            'image'
        ]

    
class ProductDefaultSubCategoryShowSerializer(serializers.ModelSerializer):
    category = ProductDefaultCategoryShowSerializer(read_only=True)
    class Meta:
        model = ProductDefaultSubCategory
        fields = [
            'id',
            'category',
            'name',
            'image'
        ]


class ProductCustomSubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCustomSubCategory
        fields = [
            'id',
            'category',
            'name',
            'image'
        ]


class ProductCustomSubCategoryShowSerializer(serializers.ModelSerializer):
    category = ProductCustomCategorySerializer(read_only=True)
    class Meta:
        model = ProductCustomSubCategory
        fields = [
            'id',
            'category',
            'name',
            'image'
        ]


class ProductMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMeasurement
        fields = [
            'id',
            'full_form',
            'short_form',
            'active'
        ]

    
class ProductImageShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'label',
            'image'
        ]


class ProductVideoShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = [
            'label',
            'video'
        ]


class ProductDocumentShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDocument
        fields = [
            'label',
            'doc'
        ]


class ProductTagShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = [
            'name',
        ]


class ProductSizeShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = [
            'size',
            'change_side',
            'price_change'
        ]


class ProductSpecificationShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            'key',
            'value',
            'measured_in'
        ]


class ProductExtraShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExtra
        fields = [
            'key',
            'value',
            'change_side',
            'price_change'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    images = ProductImageShowSerializer(many=True, required=False)
    videos = ProductVideoShowSerializer(many=True, required=False)
    documents = ProductDocumentShowSerializer(many=True, required=False)
    tags = ProductTagShowSerializer(many=True, required=False)
    sizes = ProductSizeShowSerializer(many=True, required=False)
    specifications = ProductSpecificationShowSerializer(many=True, required=False)
    extras = ProductExtraShowSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'item_code',
            'slug',
            'brand_name',
            'barcode',
            'thumbnail_image',
            'mrp',
            'nsp',
            'discount_percent',
            'tax',
            'quantity_per_measurement',
            'short_description',
            'rating',
            'no_of_reviews',
            'available_in_stock',
            'network',
            'default_category',
            'custom_category',
            'default_subcategory',
            'custom_subcategory',
            'measurement',
            'is_active',
            'is_archived',
            'is_open_for_sharing',
            'is_digital',
            'images',
            'videos',
            'documents',
            'tags',
            'sizes',
            'specifications',
            'extras'
        ]

    def create(self, validated_data):
        images = validated_data.pop('images', None)
        videos = validated_data.pop('videos', None)
        documents = validated_data.pop('documents', None)
        tags = validated_data.pop('tags', None)
        sizes = validated_data.pop('sizes', None)
        specifications = validated_data.pop('specifications', None)
        extras = validated_data.pop('extras', None)

        product = Product.objects.create(**validated_data)

        if images is not None:
            for i in images:
                ProductImage.objects.create(**i, product=product)
            product.thumbnail_image = images[0]
            product.save()

        if videos is not None:
            for i in videos:
                ProductVideo.objects.create(**i, product=product)

        if documents is not None:
            for i in documents:
                ProductDocument.objects.create(**i, product=product)

        if tags is not None:
            for i in tags:
                ProductTag.objects.create(**i, product=product)

        if sizes is not None:
            for i in sizes:
                ProductSize.objects.create(**i, product=product)

        if specifications is not None:
            for i in specifications:
                ProductSpecification.objects.create(**i, product=product)

        if extras is not None:
            for i in extras:
                ProductExtra.objects.create(**i, product=product)

        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    images = ProductImageShowSerializer(many=True, required=False)
    videos = ProductVideoShowSerializer(many=True, required=False)
    documents = ProductDocumentShowSerializer(many=True, required=False)
    tags = ProductTagShowSerializer(many=True, required=False)
    sizes = ProductSizeShowSerializer(many=True, required=False)
    specifications = ProductSpecificationShowSerializer(many=True, required=False)
    extras = ProductExtraShowSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'item_code',
            'slug',
            'brand_name',
            'barcode',
            'thumbnail_image',
            'mrp',
            'nsp',
            'discount_percent',
            'tax',
            'quantity_per_measurement',
            'short_description',
            'rating',
            'no_of_reviews',
            'available_in_stock',
            'network',
            'default_category',
            'custom_category',
            'default_subcategory',
            'custom_subcategory',
            'measurement',
            'is_active',
            'is_archived',
            'is_open_for_sharing',
            'is_digital',
            'images',
            'videos',
            'documents',
            'tags',
            'sizes',
            'specifications',
            'extras'
        ]

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        videos = validated_data.pop('videos', None)
        documents = validated_data.pop('documents', None)
        tags = validated_data.pop('tags', None)
        sizes = validated_data.pop('sizes', None)
        specifications = validated_data.pop('specifications', None)
        extras = validated_data.pop('extras', None)

        images_data = (instance.images).all()
        images_data = list(images_data)
        videos_data = (instance.videos).all()
        videos_data = list(videos_data)
        documents_data = (instance.documents).all()
        documents_data = list(documents_data)
        tags_data = (instance.tags).all()
        tags_data = list(tags_data)
        sizes_data = (instance.sizes).all()
        sizes_data = list(sizes_data)
        specifications_data = (instance.specifications).all()
        specifications_data = list(specifications_data)
        extras_data = (instance.extras).all()
        extras_data = list(extras_data)

        instance.default_category = validated_data.get('default_category', instance.default_category)
        instance.custom_category = validated_data.get('custom_category', instance.custom_category)
        instance.default_subcategory = validated_data.get('default_subcategory', instance.default_subcategory)
        instance.custom_subcategory = validated_data.get('custom_subcategory', instance.custom_subcategory)
        instance.measurement = validated_data.get('measurement', instance.measurement)
        instance.name = validated_data.get('name', instance.name)
        instance.brand_name = validated_data.get('brand_name', instance.brand_name)
        instance.barcode = validated_data.get('barcode', instance.barcode)
        instance.thumbnail_image = validated_data.get('thumbnail_image', instance.thumbnail_image)
        instance.mrp = validated_data.get('mrp', instance.mrp)
        instance.nsp = validated_data.get('nsp', instance.nsp)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.quantity_per_measurement = validated_data.get('quantity_per_measurement', instance.quantity_per_measurement)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.available_in_stock = validated_data.get('available_in_stock', instance.available_in_stock)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        instance.is_open_for_sharing = validated_data.get('is_open_for_sharing', instance.is_open_for_sharing)
        instance.is_digital = validated_data.get('is_digital', instance.is_digital)
        instance.save()

        if images is not None:
            for i in images:
                j = images_data.pop(0)
                j.image = i.get('image', j.image)
                j.save()

        if videos is not None:
            for i in videos:
                j = videos_data.pop(0)
                j.video = i.get('video', j.video)
                j.save()

        if documents is not None:
            for i in documents:
                j = documents_data.pop(0)
                j.doc = i.get('doc', j.doc)
                j.save()

        if tags is not None:
            for i in tags:
                j = tags_data.pop(0)
                j.name = i.get('name', j.name)
                j.save()

        if sizes is not None:
            for i in sizes:
                j = sizes_data.pop(0)
                j.size = i.get('size', j.size)
                j.change_side = i.get('change_side', j.change_side)
                j.price_change = i.get('price_change', j.price_change)
                j.save()

        if specifications is not None:
            for i in specifications:
                j = specifications_data.pop(0)
                j.key = i.get('key', j.key)
                j.value = i.get('value', j.value)
                j.measured_in = i.get('measured_in', j.measured_in)
                j.save()

        if extras is not None:
            for i in extras:
                j = extras_data.pop(0)
                j.key = i.get('key', j.key)
                j.value = i.get('value', j.value)
                j.change_side = i.get('change_side', j.change_side)
                j.price_change = i.get('price_change', j.price_change)
                j.save()

        return instance


class ProductShowSerializer(serializers.ModelSerializer):
    network = ShowNetworkSerializer(read_only=True)
    default_category = ProductDefaultCategoryShowSerializer(read_only=True)
    custom_category = ProductCustomCategorySerializer(read_only=True)
    default_subcategory = ProductDefaultSubCategoryShowSerializer(read_only=True)
    custom_subcategory = ProductCustomSubCategoryShowSerializer(read_only=True)
    measurement = ProductMeasurementSerializer(read_only=True)
    images = ProductImageShowSerializer(many=True, required=True)
    videos = ProductVideoShowSerializer(many=True, required=True)
    documents = ProductDocumentShowSerializer(many=True, required=True)
    tags = ProductTagShowSerializer(many=True, required=True)
    sizes = ProductSizeShowSerializer(many=True, required=True)
    specifications = ProductSpecificationShowSerializer(many=True, required=True)
    extras = ProductExtraShowSerializer(many=True, required=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'item_code',
            'slug',
            'brand_name',
            'barcode',
            'thumbnail_image',
            'mrp',
            'nsp',
            'discount_percent',
            'tax',
            'quantity_per_measurement',
            'short_description',
            'rating',
            'no_of_reviews',
            'available_in_stock',
            'network',
            'default_category',
            'custom_category',
            'default_subcategory',
            'custom_subcategory',
            'measurement',
            'is_active',
            'is_archived',
            'is_open_for_sharing',
            'is_digital',
            'images',
            'videos',
            'documents',
            'tags',
            'sizes',
            'specifications',
            'extras'
        ]


  
class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'product',
            'image',
        ]


class ProductVideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = [
            'product',
            'video',
        ]


class ProductDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDocument
        fields = [
            'product',
            'doc',
        ]


class ProductTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = [
            'product',
            'name',
        ]


class ProductSizeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = [
            'product',
            'size',
            'change_side',
            'price_change'
        ]


class ProductSpecificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            'key',
            'product',
            'value',
            'measured_in'
        ]


class ProductExtraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExtra
        fields = [
            'key',
            'product',
            'value',
            'change_side',
            'price_change'
        ]


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = [
            'id',
            'network',
            'rating',
            'comment',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        review = ProductReview.objects.create(**validated_data, by=user)
        init = float(review.product.rating)*float(review.product.no_of_reviews)
        new_rate = (init+float(review.rating))/(review.product.no_of_reviews+1)
        review.product.rating = new_rate
        review.product.no_of_reviews += 1
        review.product.save()
        return review


class ProductReviewShowSerializer(serializers.ModelSerializer):
    by = UserMiniSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = [
            'id',
            'product',
            'by',
            'rating',
            'comment',
            'is_spam',
            'created',
            'is_active'
        ]