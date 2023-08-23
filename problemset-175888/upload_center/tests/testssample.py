from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from account.models import *


class Tests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pro_max = Account.objects.create(title='Pro Max', storage=2621440, max_file_transfer=2097152)
        User.objects.create_user(account=pro_max, username="kian", password="ak18")

    def test_upload_empty_file(self):
        c = APIClient()
        res_login = c.post('/fm/login/', {'username': 'kian', 'password': 'ak18'})
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
        c.credentials(HTTP_AUTHORIZATION='Token ' + res_login.json()['token'])

        with open('empty_file', 'wb'):
            pass

        with open('empty_file', 'rb') as fp:
            res_upload = c.put('/fm/upload/', {'file_field': fp})
            self.assertEqual(res_upload.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_download(self):
        c = APIClient()
        response = c.get('/fm/download/kian/quera.png')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response.json(), {"detail": "quera.png hasn't existed!"}
        )
