from django.urls import path
from .views import dashboard_view, logout_view, login_view, pdb_test_view, person_view, create_person_view, \
    edit_person_view, save_sidebar_view
from .viewsets import ListCountryView, ListDistrictView, ListLocalityView, ListRegionView, ListBookNumberView, \
    ListHostelView, ListPasportystView, ListTypeLocalityView

# app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name="main"),
    # session
    path('save_sidebar_view/', save_sidebar_view, name="save_sidebar_view"),
    # person
    path('person/create/', create_person_view, name="create_person"),
    path('person/<int:pk>/', person_view, name="show_person"),
    path('person/<int:pk>/edit/', edit_person_view, name="edit_person"),
    # auth
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    # api
    path('country/', ListCountryView.as_view(), name="country_api"),
    path('region/', ListRegionView.as_view(), name="region_api"),
    path('district/', ListDistrictView.as_view(), name="district_api"),
    path('locality/', ListLocalityView.as_view(), name="locality_api"),
    path('pasportyst/', ListPasportystView.as_view(), name="pasportyst_api"),
    path('hostel/', ListHostelView.as_view(), name="hostel_api"),
    path('book-number/', ListBookNumberView.as_view(), name="book_number_api"),
    path('type-locality/', ListTypeLocalityView.as_view(), name="type_locality_api"),
    # testing
    path('populate-db/', pdb_test_view, ),

]
