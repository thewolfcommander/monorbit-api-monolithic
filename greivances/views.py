from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *


class ListCreateFAQCategory(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all()
    filterset_fields = [
        'is_active',
        'added_by'
    ]


class UpdateFAQCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateFAQ(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQCreateSerializer
    queryset = FAQ.objects.all()


class ListFAQ(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQShowSerializer
    queryset = FAQ.objects.all().order_by('popularity_score')
    filterset_fields = [
        'category',
        'popularity_score',
        'no_of_upvotes',
        'no_of_downvotes',
        'is_active'
    ]


class UpdateFAQ(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQShowSerializer
    queryset = FAQ.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateFAQReaction(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        faq = request.data.get('faq', None)
        like_it_or_not = request.data.get('like_it_or_not', False)

        if faq is None:
            return Response({
                'status': False,
                'message': 'Invalid FAQ. Please try again by correcting it.'
            })

        try:
            faq_obj = FAQ.objects.get(id=faq)
            reaction = FAQReaction.objects.create(
                faq=faq_obj,
                user=user,
                like_it_or_not=like_it_or_not
            )
            if reaction.like_it_or_not:
                reaction.faq.no_of_upvotes += 1
                reaction.faq.popularity_score = float(reaction.faq.popularity_score) + 0.01
                reaction.faq.save()
                return Response({
                    'status': True,
                    'message': 'You have successfully liked it.',
                    'id': reaction.id,
                    'faq': {
                        'popularity_score': reaction.faq.popularity_score,
                        'no_of_upvotes': reaction.faq.no_of_upvotes,
                        'no_of_downvotes': reaction.faq.no_of_downvotes,
                    }
                })
            else:
                reaction.faq.no_of_downvotes += 1
                reaction.faq.popularity_score = float(reaction.faq.popularity_score) - 0.01
                reaction.faq.save()
                return Response({
                    'status': True,
                    'message': 'You have successfully disliked it.',
                    'id': reaction.id,
                    'faq': {
                        'popularity_score': reaction.faq.popularity_score,
                        'no_of_upvotes': reaction.faq.no_of_upvotes,
                        'no_of_downvotes': reaction.faq.no_of_downvotes,
                    }
                })
        except FAQ.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Invalid FAQ. Please try again by correcting it.'
            })

        
class DeleteFAQReaction(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQReactionSerializer
    queryset = FAQReaction.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.like_it_or_not:
                instance.faq.no_of_upvotes -= 1
                instance.faq.popularity_score = float(instance.faq.popularity_score) - 0.01
                instance.faq.save()
            else:
                instance.faq.no_of_downvotes -= 1
                instance.faq.popularity_score = float(instanec.faq.popularity_score) + 0.01
                instance.faq.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=204)