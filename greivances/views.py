from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *


class ListCreateFAQCategory(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all().order_by('-added')
    filterset_fields = [
        'is_active',
        'added_by'
    ]


class UpdateFAQCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateFAQ(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FAQCreateSerializer
    queryset = FAQ.objects.all()


class ListFAQ(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
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
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        user = request.user
        faq = request.data.get('faq', None)
        like_it_or_not = request.data.get('like_it_or_not', False)

        if faq is None:
            raise ValidationError(detail="Invalid FAQ. Please try again later by correcting it.", code=400)

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
            raise ValidationError(detail="Invalid FAQ. Please try again later by correcting it.", code=404)

        
class DeleteFAQReaction(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
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

    
class ListCreateTicketCategory(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()


class UpdateTicketCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateTicket(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateTicketSerializer
    queryset = Ticket.objects.all()


class ListTicket(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowTicketSerializer
    queryset = Ticket.objects.all()
    filterset_fields = [
        'id',
        'category',
        'category__title',
        'monion_referral',
        'mobile_number',
        'define_category',
        'title',
        'ticket_status',
        'upvotes',
        'downvotes',
        'is_active',
        'user'
    ]


class UpdateTicket(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShowTicketSerializer
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateTicketComment(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TicketCommentSerializer
    queryset = TicketComment.objects.all()
    filterset_fields = [
        'id',
        'ticket',
        'upvotes',
        'downvotes',
        'user'
    ]


class UpdateTicketComment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketCommentSerializer
    queryset = TicketComment.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GiveTicketReaction(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        reaction = request.data.get('reaction', None)
        ticket = request.data.get('ticket', None)

        if reaction is None:
            raise ValidationError(detail="Invalid Reaction. Please give a proper reaction on the ticket.", code=400)
        
        if ticket is None:
            raise ValidationError(detail="Invalid Ticket ID. Please try again later by correcting it.", code=400)

        try:
            ticket_obj = Ticket.objects.get(id=ticket)
            if reaction == 'up':
                ticket_obj.upvotes += 1
                ticket_obj.save()
            elif reaction == 'down':
                ticket_obj.downvotes += 1
                ticket_obj.save()
            else:
                raise ValidationError(detail="Invalid Reaction.", code=400)
            return Response({
                'status': True,
                'message': "Hurray! You reacted"
            }, status=200)
        except Ticket.DoesNotExist:
            raise ValidationError(detail="Invalid Ticket ID.", code=404)

        

class GiveTicketCommentReaction(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        reaction = request.data.get('reaction', None)
        comment = request.data.get('comment', None)

        
        if reaction is None:
            raise ValidationError(detail="Invalid Reaction. Please give a proper reaction on the ticket.", code=400)
        
        if comment is None:
            raise ValidationError(detail="Please provide comment to give reaction", code=400)

        try:
            comment_obj = TicketComment.objects.get(id=comment)
            if reaction == 'up':
                comment_obj.upvotes += 1
                comment_obj.save()
            elif reaction == 'down':
                comment_obj.downvotes += 1
                comment_obj.save()
            else:
                raise ValidationError(detail="Invalid Reaction.", code=400)
            return Response({
                'status': True,
                'message': "Hurray! You reacted"
            }, status=200)
        except TicketComment.DoesNotExist:
            raise ValidationError(detail="Invalid Comment ID.", code=404)