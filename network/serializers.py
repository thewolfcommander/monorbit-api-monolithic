from rest_framework import serializers

from accounts.serializers import UserMiniSerializer
from .models import *


class NetworkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkCategory
        fields = [
            'id',
            'name',
            'priority',
            'image',
            'created'
        ]


class NetworkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkType
        fields = [
            'id',
            'name',
            'image',
            'created'
        ]

    
class NetworkImageShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkImage
        fields = [
            'image',
        ]


class NetworkVideoShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkVideo
        fields = [
            'video',
        ]


class NetworkDocumentShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDocument
        fields = [
            'doc',
        ]

    
class NetworkOperationTimingShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOperationTiming
        fields = [
            'day',
            'opening',
            'closing',
            'status'
        ]

    
class NetworkOperationLocationShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOperationLocation
        fields = [
            'pincode'
        ]

    
class CreateNetworkSerializer(serializers.ModelSerializer):
    images = NetworkImageShowSerializer(many=True, required=False)
    videos = NetworkVideoShowSerializer(many=True, required=False)
    documents = NetworkDocumentShowSerializer(many=True, required=False)
    timings = NetworkOperationTimingShowSerializer(many=True, required=False)
    locations = NetworkOperationLocationShowSerializer(many=True, required=False)
    class Meta:
        model = Network
        fields = [
            'id',
            'user',
            'category',
            'network_type',
            'name',
            'address',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'alt_phone',
            'alt_email',
            'images',
            'videos',
            'is_premium',
            'documents',
            'locations',
            'timings'
        ]

    def create(self, validated_data):
        images = validated_data.pop('images', None)
        videos = validated_data.pop('videos', None)
        documents = validated_data.pop('documents', None)
        timings = validated_data.pop('timings', None)
        locations = validated_data.pop('locations', None)

        alt_email = validated_data.get('alt_email', None)
        alt_phone = validated_data.get('alt_phone', None)
        request = self.context['request']
        user = request.user

        network = Network.objects.create(
            **validated_data, 
            user=user
        )

        user.network_created += 1
        user.is_creator = True
        if not user.city:
            user.city = validated_data.get('city')
        
        if not user.pincode:
            user.pincode = validated_data.get('pincode')
        user.save()

        if images is not None:
            for i in images:
                NetworkImage.objects.create(**i, network=network)
            network.thumbnail_image = NetworkImage.objects.filter(network=network).first().image
            network.save()

        if videos is not None:
            for i in videos:
                NetworkVideo.objects.create(**i, network=network)
            network.is_video = True
            network.save()

        if documents is not None:
            for i in documents:
                NetworkDocument.objects.create(**i, network=network)
            network.is_document = True
            network.save()

        if timings is not None:
            for i in timings:
                NetworkOperationTiming.objects.create(**i, network=network)

        if locations is not None:
            for i in locations:
                NetworkOperationLocation.objects.create(**i, network=network)

        return network

    
class ShowNetworkSerializer(serializers.ModelSerializer):
    timings = NetworkOperationTimingShowSerializer(many=True, required=False)
    category = NetworkCategorySerializer(read_only=True)
    network_type = NetworkTypeSerializer(read_only=True)
    class Meta:
        model = Network
        fields = [
            'id',
            'user',
            'category',
            'thumbnail_image',
            'network_type',
            'name',
            'address',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'timings',
            'rating',
            'no_of_reviews',
            'registered_stores',
            'is_verified',
            'is_active',
            'is_premium',
            'is_spam',
            'is_video',
            'is_document',
        ]


class NetworkDetailSerializer(serializers.ModelSerializer):
    images = NetworkImageShowSerializer(many=True, required=False)
    videos = NetworkVideoShowSerializer(many=True, required=False)
    documents = NetworkDocumentShowSerializer(many=True, required=False)
    timings = NetworkOperationTimingShowSerializer(many=True, required=False)
    locations = NetworkOperationLocationShowSerializer(many=True, required=False)
    category = NetworkCategorySerializer(read_only=True)
    network_type = NetworkTypeSerializer(read_only=True)
    class Meta:
        model = Network
        fields = [
            'id',
            'user',
            'category',
            'thumbnail_image',
            'network_type',
            'name',
            'address',
            'landmark',
            'city',
            'state',
            'country',
            'pincode',
            'alt_phone',
            'alt_email',
            'gst',
            'adhaar',
            'pan',
            'timings',
            'images',
            'videos',
            'documents',
            'locations',
            'rating',
            'no_of_reviews',
            'registered_stores',
            'is_verified',
            'is_archived',
            'is_active',
            'is_premium',
            'is_spam',
            'is_video',
            'is_document',
        ]

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        videos = validated_data.pop('videos', None)
        documents = validated_data.pop('documents', None)
        timings = validated_data.pop('timings', None)
        locations = validated_data.pop('locations', None)

        images_data = (instance.images).all()
        images_data = list(images_data)
        videos_data = (instance.videos).all()
        videos_data = list(videos_data)
        documents_data = (instance.documents).all()
        documents_data = list(documents_data)
        timings_data = (instance.timings).all()
        timings_data = list(timings_data)
        locations_data = (instance.locations).all()
        locations_data = list(locations_data)

        request = self.context['request']
        user = request.user
        
        instance.name = validated_data.get('name', instance.name)
        instance.thumbnail_image = validated_data.get('thumbnail_image', instance.thumbnail_image)
        instance.address = validated_data.get('address', instance.address)
        instance.landmark = validated_data.get('landmark', instance.landmark)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.alt_phone = validated_data.get('alt_phone', instance.alt_phone)
        instance.alt_email = validated_data.get('alt_email', instance.alt_email)
        instance.gst = validated_data.get('gst', instance.gst)
        instance.adhaar = validated_data.get('adhaar', instance.adhaar)
        instance.pan = validated_data.get('pan', instance.pan)
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

        if timings is not None:
            for i in timings:
                j = timings_data.pop(0)
                j.day = i.get('day', j.day)
                j.opeing = i.get('opening', j.opening)
                j.closing = i.get('closing', j.closing)
                j.status = i.get('status', j.status)
                j.save()

        if locations is not None:
            for i in locations:
                j = locations_data.pop(0)
                j.pincode = i.get('pincode', j.pincode)
                j.save()

        return instance

    
class DeleteNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = [
            'is_archived',
            'is_active'
        ]

    def update(self, instance, validated_data):
        instance.is_archived = True
        instance.is_active = False
        instance.save()

        return {
            "status": "SUCCESS",
            "message": "Network Deleted Successfully"
        }

    
class NetworkImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkImage
        fields = [
            'network',
            'image',
        ]


class NetworkVideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkVideo
        fields = [
            'network',
            'video',
        ]


class NetworkDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDocument
        fields = [
            'network',
            'doc',
        ]

    
class NetworkOperationTimingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOperationTiming
        fields = [
            'network',
            'day',
            'opening',
            'closing'
        ]

    
class NetworkOperationLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOperationLocation
        fields = [
            'network',
            'pincode'
        ]

    
class NetworkReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkReview
        fields = [
            'id',
            'network',
            'rating',
            'comment',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        review = NetworkReview.objects.create(**validated_data, by=user)
        init = float(review.network.rating)*float(review.network.no_of_reviews)
        new_rate = (init+float(review.rating))/(review.network.no_of_reviews+1)
        review.network.rating = new_rate
        review.network.no_of_reviews += 1
        review.network.save()
        return review


    
class NetworkReviewShowSerializer(serializers.ModelSerializer):
    by = UserMiniSerializer(read_only=True)
    class Meta:
        model = NetworkReview
        fields = [
            'id',
            'network',
            'by',
            'rating',
            'comment',
            'is_spam',
            'created',
            'is_active'
        ]