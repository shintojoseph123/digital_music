# REST imports
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
# file imports
from dsrs import views
from dsrs import models
from dsrs import serializers

class TestDSR(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = '/dsrs/'

    def test_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create(self):
        params = {
        	'path': 'path.csv',
        	'period_end': '2020-01-01',
        	'period_start': '2020-01-01',
            'currency': {
                'name':'Dollar',
                'code':'USD',
                'symbol':'246',
                },
            'territory': {
                'name':'Spain',
                'code_2':'ES',
                'code_3':'EUS',
                },
        }
        response = self.client.post(self.uri, params, format='json')
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_read(self):
        curr_obj = models.Currency.objects.create(
                        name='Dollar',
                        code="USD",
                        symbol='246',
                        )
        terr_obj = models.Territory.objects.create(
                        name='Spain',
                        code_2="ES",
                        code_3='EUS',
                        local_currency=curr_obj,
                        )
        dsr_obj = models.DSR.objects.create(
                        path='path.csv',
                        period_end='2020-01-01',
                        period_start='2020-01-01',
                        currency=curr_obj,
                        territory=terr_obj,
                        )
        url = '/dsrs/%s/' % dsr_obj.id
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))


class TestResource(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = '/resources/'

    def test_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))


    def test_create(self):
        curr_obj = models.Currency.objects.create(
                        name='Dollar',
                        code="USD",
                        symbol='246',
                        )
        terr_obj = models.Territory.objects.create(
                        name='Spain',
                        code_2="ES",
                        code_3='EUS',
                        local_currency=curr_obj,
                        )
        dsr_obj = models.DSR.objects.create(
                        path='path.csv',
                        period_end='2020-01-01',
                        period_start='2020-01-01',
                        currency=curr_obj,
                        territory=terr_obj,
                        )
        resource_obj = models.Resource.objects.create(
                            dsp_id = 'dsp_id',
                            usages = 10,
                            revenue = 10,
                            isrc = 'isrc',
                            title = 'title',
                            artists = 'artists',
                            )
        resource_obj.dsr.set([dsr_obj.pk])

        url = '/resources/%s/' % resource_obj.id
        response = self.client.get(url)
        serialized = serializers.ResourceSerializer(resource_obj)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_percentile(self):
         url = '/resources/percentile/%s/' % 10
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200,
                          'Expected Response Code 200, received {0} instead.'
                          .format(response.status_code))
