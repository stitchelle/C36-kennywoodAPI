"""View module for handling requests about intineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer

class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for intineraries

    Arguments:
        serializers
    """

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction',)
        depth = 2

class ItineraryItems(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Itinerary instance
        """
        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer_id = request.auth.user.customer.id
        new_itinerary_item.attraction_id = request.data["attraction_id"]

        new_itinerary_item.save()

        serializer = ItinerarySerializer(new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a itinerary

        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary_item = Itinerary.objects.get(pk=pk)
        itinerary_item.starttime = request.data["starttime"]
        itinerary_item.attraction_id = request.data["attraction_id"]
        itinerary_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = Itinerary.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to itinerary resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        itinerary_item = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            itinerary_item, many=True, context={'request': request})
        return Response(serializer.data)