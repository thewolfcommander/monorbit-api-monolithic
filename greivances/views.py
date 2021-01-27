from django.http import Http404

from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from .models import *
from .serializers import *
from .permissions import *


class ListCreateFAQCategory(generics.ListCreateAPIView):
    """
    Creating FAQ category to help users.Only admin can create.
    List of FAQ category.
    """
    permission_classes = [IsAdmin]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all().order_by('-added')
    filterset_fields = [
        'is_active',
        'added_by'
    ]


class UpdateFAQCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Getting single FAQ category.
    Update(put ,patch, delete) Single FAQ category. Only admin can.
    """
    permission_classes = [IsAdmin]
    serializer_class = FAQCategorySerializer
    queryset = FAQCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateFAQ(generics.CreateAPIView):
    """
    Creating FAQ to help users.Only admin can create.
    """
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    serializer_class = FAQCreateSerializer
    queryset = FAQ.objects.all()


class ListFAQ(generics.ListAPIView):
    """
    List FAQ
    """
    permission_classes = [IsAdmin]
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
    """
    Getting single FAQ.
    Update(put ,patch, delete) Single FAQ . Only admin can.
    """
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    serializer_class = FAQShowSerializer
    queryset = FAQ.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    
class CreateFAQReaction(APIView):
    """
    Users Reaction on FAQ.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        # Get following data from request
        user = request.user
        faq = request.data.get('faq', None)
        like_it_or_not = request.data.get('like_it_or_not', False)

        if faq is None:
            raise ValidationError(detail="Invalid FAQ. Please try again later by correcting it.", code=400)

        try:
            # find FAQ object using requested "faq". And create reaction object
            faq_obj = FAQ.objects.get(id=faq)
            reaction = FAQReaction.objects.create(
                faq=faq_obj,
                user=user,
                like_it_or_not=like_it_or_not
            )
            # if user like the faq (True) then proceed.
            if reaction.like_it_or_not:
                reaction.faq.no_of_upvotes += 1
                # increase popularity score (so that we can sort according to this)
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
                # if user don't like faq (False)
                reaction.faq.no_of_downvotes += 1
                # decrease popularity score (so that we can sort according to this)
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
    """
    Deleting FAQ Reaction. Only admin can.
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = FAQReactionSerializer
    queryset = FAQReaction.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            # Get object by requested "id"
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
    """
    Create TicketCategory. Ticket is used in prolems identification.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()


class UpdateTicketCategory(generics.RetrieveUpdateDestroyAPIView):
    """
    Update Ticket category.
    """
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateTicket(generics.CreateAPIView):
    """
    Create Ticket (Problem)
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateTicketSerializer
    queryset = Ticket.objects.all()


class ListTicket(generics.ListAPIView):
    """
    List of Tickets (Problems)
    """
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
    """
    Update Ticket( Ticket owner will do) 
    """
    permission_classes = [IsOwner]
    serializer_class = ShowTicketSerializer
    queryset = Ticket.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateTicketComment(generics.ListCreateAPIView):
    """
    Comment on Ticket(problem). Anyone can do.
    """
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
    """
    Update Comment on ticket(problem). Comment Owner can do.
    """
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    serializer_class = TicketCommentSerializer
    queryset = TicketComment.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GiveTicketReaction(APIView):
    """
    Reaction on Ticket(problem). Anyone can comment on user ticket(problem)
    """
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
    """
    Anyone can comment on "comment of a ticket(problem)"
    """
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