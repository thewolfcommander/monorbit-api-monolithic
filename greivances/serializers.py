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
            'image_url',
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
        instance.image_url = validated_data.get('image_url', instance.image_url)
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

    
class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = [
            'id',
            'title',
            'description',
            'icon'
        ]


class TicketAttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = [
            'id',
            'attachment_type',
            'url'
        ]

    
class CreateTicketSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    attachments = TicketAttachmentCreateSerializer(many=True)
    class Meta:
        model = Ticket
        fields = [
            'id',
            'category',
            'monion_referral',
            'country_code',
            'mobile_number',
            'define_category',
            'title',
            'description',
            'ticket_status',
            'upvotes',
            'downvotes',
            'is_attachment',
            'is_active',
            'created_on',
            'updated_on',
            'user',
            'attachments'
        ]

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', None)

        try:
            user = self.context['request'].user
            country_code = user.country_code
            mobile_number = user.mobile_number
        except:
            user = None
            country_code = validated_data.get('country_code')
            mobile_number = validated_data.get('mobile_number')

        category = validated_data.get('category', None)
        if str(category.title).lower() == 'other':
            define_category = validated_data.get('define_category')
        else:
            define_category = None
        
        monion_referral = validated_data.get('monion_referral')
        title = validated_data.get('title')
        description = validated_data.get('description')

        instance = Ticket.objects.create(
            category=category,
            define_category=define_category,
            user=user,
            country_code=country_code,
            mobile_number=mobile_number,
            monion_referral=monion_referral,
            title=title,
            description=description,
            ticket_status='created'
        )
        if attachments is not None:
            instance.is_attachment = True
            for a in attachments:
                TicketAttachment.objects.create(**a, ticket=instance)
            instance.save()

        return instance

    
class ShowTicketSerializer(serializers.ModelSerializer):
    category = FAQCategorySerializer(read_only=True)
    user = UserMiniSerializer(read_only=True)
    attachments = TicketAttachmentCreateSerializer(many=True)
    class Meta:
        model = Ticket
        fields = [
            'id',
            'category',
            'monion_referral',
            'country_code',
            'mobile_number',
            'define_category',
            'title',
            'description',
            'ticket_status',
            'upvotes',
            'downvotes',
            'is_attachment',
            'is_active',
            'created_on',
            'updated_on',
            'user',
            'attachments'
        ]

    def update(self, instance, validated_data):
        attachments = validated_data.pop('attachments', None)

        attachments_data = (instance.attachments).all()
        attachments_data = list(attachments_data)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.ticket_status = validated_data.get('ticket_status', instance.ticket_status)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        if attachments is not None:
            for a in attachments:
                p = attachments_data.pop(0)
                p.attachment_type = a.get('attachment_type', p.attachment_type)
                p.url = a.get('url', p.url)
                p.save()
        instance.save()
        return instance

    
class TicketCommentSerializer(serializers.ModelSerializer):
    """
    TODO: Implement credit based feature for Commenting and helping tickets
    """
    user = UserMiniSerializer(read_only=True)
    class Meta:
        model = TicketComment
        fields = [
            'id',
            'ticket',
            'comment',
            'upvotes',
            'downvotes',
            'timestamp',
            'user'
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        instance = TicketComment.objects.create(
            **validated_data,
            user=user
        )
        return instance

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance