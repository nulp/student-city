from rest_framework.generics import ListAPIView
from .serializers import CountrySerializer, RegionSerializer, DistrictSerializer, LocalitySerializer, \
    TypeLocalitySerializer, HostelSerializer, BookNumberSerializer, PasportystSerializer
from .models import Country, Region, District, Locality, TypeLocality, Hostel, Pasportyst, Book


class ListCountryView(ListAPIView):
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer


class ListRegionView(ListAPIView):
    def get_queryset(self):
        queryset = Region.objects.all()
        country_id = self.request.query_params.get('country_id', None)
        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        return queryset.order_by('name')

    serializer_class = RegionSerializer


class ListDistrictView(ListAPIView):
    def get_queryset(self):
        queryset = District.objects.all()
        region_id = self.request.query_params.get('region_id', None)
        if region_id is not None:
            queryset = queryset.filter(region_id=region_id)
        return queryset.order_by('name')

    serializer_class = DistrictSerializer


class ListLocalityView(ListAPIView):
    def get_queryset(self):
        queryset = Locality.objects.all()
        region_id = self.request.query_params.get('region_id', None)
        district_id = self.request.query_params.get('district_id', None)
        type_locality_id = self.request.query_params.get('type_locality_id', None)

        if region_id is not None:
            queryset = queryset.filter(region_id=region_id)
        if district_id is not None:
            if district_id == '-1':
                queryset = queryset.filter(region_id=region_id, district_id=None)
            else:
                queryset = queryset.filter(district_id=district_id)
        if type_locality_id is not None:
            queryset = queryset.filter(type_locality_id=type_locality_id)

        return queryset.order_by('name')

    serializer_class = LocalitySerializer


class ListTypeLocalityView(ListAPIView):
    queryset = TypeLocality.objects.all()

    serializer_class = TypeLocalitySerializer


class ListHostelView(ListAPIView):
    queryset = Hostel.objects.all()

    serializer_class = HostelSerializer


class ListBookNumberView(ListAPIView):

    def get_queryset(self):
        queryset = Book.objects.all()
        hostel_id = self.request.query_params.get('hostel_id', None)
        if hostel_id is not None:
            queryset = queryset.filter(hostel_id=hostel_id)
        return queryset

    serializer_class = BookNumberSerializer


class ListPasportystView(ListAPIView):
    queryset = Pasportyst.objects.all().order_by('name')

    serializer_class = PasportystSerializer
