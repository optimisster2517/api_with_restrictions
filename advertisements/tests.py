"""
Тесты для приложения advertisements.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementAPITestCase(TestCase):
    """Тесты для API объявлений."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаём пользователей
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Создаём токены
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # Создаём клиента API
        self.client = APIClient()
        
        # Создаём тестовое объявление
        self.advertisement = Advertisement.objects.create(
            title='Test Ad',
            description='Test Description',
            creator=self.user1,
            status=AdvertisementStatusChoices.OPEN
        )
    
    def test_list_advertisements_anonymous(self):
        """Тест просмотра списка объявлений неавторизованным пользователем."""
        response = self.client.get('/api/advertisements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_advertisement_anonymous(self):
        """Тест просмотра одного объявления неавторизованным пользователем."""
        response = self.client.get(f'/api/advertisements/{self.advertisement.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_advertisement_authenticated(self):
        """Тест создания объявления авторизованным пользователем."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {
            'title': 'New Ad',
            'description': 'New Description',
            'status': AdvertisementStatusChoices.OPEN
        }
        response = self.client.post('/api/advertisements/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['creator']['id'], self.user1.id)
    
    def test_create_advertisement_anonymous(self):
        """Тест попытки создания объявления неавторизованным пользователем."""
        data = {
            'title': 'New Ad',
            'description': 'New Description'
        }
        response = self.client.post('/api/advertisements/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_own_advertisement(self):
        """Тест обновления своего объявления."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        response = self.client.patch(
            f'/api/advertisements/{self.advertisement.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_update_other_user_advertisement(self):
        """Тест попытки обновления чужого объявления."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        data = {'title': 'Hacked Title'}
        response = self.client.patch(
            f'/api/advertisements/{self.advertisement.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_own_advertisement(self):
        """Тест удаления своего объявления."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(
            f'/api/advertisements/{self.advertisement.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_other_user_advertisement(self):
        """Тест попытки удаления чужого объявления."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.delete(
            f'/api/advertisements/{self.advertisement.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_max_open_advertisements_validation(self):
        """Тест валидации максимального количества открытых объявлений."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Создаём 9 дополнительных открытых объявлений (уже есть 1)
        for i in range(9):
            Advertisement.objects.create(
                title=f'Ad {i}',
                description=f'Description {i}',
                creator=self.user1,
                status=AdvertisementStatusChoices.OPEN
            )
        
        # Попытка создать 11-е объявление должна провалиться
        data = {
            'title': 'Too Many Ads',
            'description': 'This should fail',
            'status': AdvertisementStatusChoices.OPEN
        }
        response = self.client.post('/api/advertisements/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_by_status(self):
        """Тест фильтрации по статусу."""
        # Создаём закрытое объявление
        Advertisement.objects.create(
            title='Closed Ad',
            description='Closed',
            creator=self.user1,
            status=AdvertisementStatusChoices.CLOSED
        )
        
        # Фильтруем только открытые
        response = self.client.get(
            '/api/advertisements/',
            {'status': AdvertisementStatusChoices.OPEN}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for ad in response.data['results']:
            self.assertEqual(ad['status'], AdvertisementStatusChoices.OPEN)
