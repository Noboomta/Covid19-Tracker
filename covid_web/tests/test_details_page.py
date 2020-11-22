"""Unittests for Django polls application."""
import covid_web.views
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from covid_web.covid_data import CountryCovidData, WorldCovidData
from covid_web.views import get_user_country_form_ip

def my_reverse(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url

class IndexPageTest(TestCase):
    def setUp(self):
        """set up method for set everythings that use in test"""
        User.objects.create_user(username='bhatara007', password='ddddd007')
        self.client.login(username='bhatara007', password='ddddd007')

    def test_blank_detail_page(self):
        """
        test 'Let's find your Interesting area' text show
        when user not select their area
        """
        url = reverse('details')
        response = self.client.get(url)
        self.assertContains(response, "Let's find your Interested area")

    def test_details_page_display_correctly(self):
        """
        test Covid data show correctly 
        when user selected Thailand country.
        """
        test_country = 'Thailand'
        cd = CountryCovidData()
        url = my_reverse('details', kwargs=None, query_kwargs={'country': 
            test_country})
        response = self.client.get(url)
        self.assertContains(response, "{:,}".format(cd.get_result("cases", "Thailand")))
        self.assertContains(response, "{:,}".format(cd.get_result("todayCases", "Thailand")))
        self.assertContains(response, "{:,}".format(cd.get_result("deaths", "Thailand")))
        self.assertContains(response, "{:,}".format(cd.get_result("todayDeaths", "Thailand")))

    def test_user_location_form_ip(self):
        """
        Test for get_user_country_form_ip method if we put our ip 
        This method will return our current country "Thailand"
        """
        my_current_ip = '49.229.136.171'
        my_current_country = "Thailand"
        self.assertEqual(my_current_country, get_user_country_form_ip(my_current_ip))

    def test_prevent_page(self):
        url = reverse('prevent')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
    

