from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from accounts.serializers import UserMiniSerializer


class FAQCategorySerializer(serializers.ModelSerializer):
    added_by = UserMiniSerializer(read_only=True)
    class Meta:
        model = FAQCategory
        fields = [
            'id',
            'title',
            'description',
            'is_active',
            'added_by',
            'added'
        ]
    
    def create(self, validated_data):
        try:
            user = self.context['request'].user
            instance = FAQCategory.objects.create(**validated_data, added_by=user)
            return instance
        except:
            raise ValidationError("Cannot complete request. Please try again later")
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    
class FAQCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id',
            'category',
            'question',
            'answer',
            'popularity_score',
            'no_of_upvotes',
            'no_of_downvotes',
            'added_by',
            'is_active',
            'added',
            'updated'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        instance = FAQ.objects.create(**validated_data, added_by=user)
        return instance


class FAQShowSerializer(serializers.ModelSerializer):
    added_by = UserMiniSerializer(read_only=True)
    category = FAQCategorySerializer(read_only=True)
    class Meta:
        model = FAQ
        fields = [
            'id',
            'category',
            'question',
            'answer',
            'popularity_score',
            'no_of_upvotes',
            'no_of_downvotes',
            'added_by',
            'is_active',
            'added',
            'updated'
        ]

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class FAQReactionSerializer(serializers.ModelSerializer):
    faq = FAQShowSerializer()
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = FAQReaction
        fields = [
            'id',
            'faq',
            'user',
            'like_it_or_not',
            'added'
        ]