from rest_framework.generics import ListAPIView
from .serializers import CountrySerializer, RegionSerializer, DistrictSerializer, LocalitySerializer, \
    TypeLocalitySerializer, HostelSerializer, BookNumberSerializer, PasportystSerializer
from .models import Country, Region, District, Locality, TypeLocality, BookNumber, Hostel, Pasportyst


class ListCountryView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ListRegionView(ListAPIView):
    def get_queryset(self):
        queryset = Region.objects.all()
        country_id = self.request.query_params.get('country_id', None)
        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        return queryset

    serializer_class = RegionSerializer


class ListDistrictView(ListAPIView):
    def get_queryset(self):
        queryset = District.objects.all()
        region_id = self.request.query_params.get('region_id', None)
        if region_id is not None:
            queryset = queryset.filter(region_id=region_id)
        return queryset

    serializer_class = DistrictSerializer


class ListLocalityView(ListAPIView):
    def get_queryset(self):
        queryset = Locality.objects.all()
        region_id = self.request.query_params.get('region_id', None)
        district_id = self.request.query_params.get('district_id', None)
        if district_id is not None:
            if region_id is not None and district_id == '-1':
                queryset = queryset.filter(region_id=region_id, district_id=None)
            else:
                queryset = queryset.filter(district_id=district_id)
        elif region_id is not None:
            queryset = queryset.filter(region_id=region_id)
        return queryset

    serializer_class = LocalitySerializer


class ListTypeLocalityView(ListAPIView):
    queryset = TypeLocality.objects.all()

    serializer_class = TypeLocalitySerializer


class ListHostelView(ListAPIView):
    queryset = Hostel.objects.all()

    serializer_class = HostelSerializer


class ListBookNumberView(ListAPIView):
    queryset = BookNumber.objects.all().order_by('-pk')

    serializer_class = BookNumberSerializer


class ListPasportystView(ListAPIView):
    queryset = Pasportyst.objects.all()

    serializer_class = PasportystSerializer
