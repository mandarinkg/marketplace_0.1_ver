from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from products.models import Product, Category
from shops.models import Shop
from .models import Favorite

User = get_user_model()


class FavoriteModelTest(TestCase):
    """Тесты для модели Favorite"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='client'
        )
        
        self.shop = Shop.objects.create(name='Test Shop')
        
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123',
            role='seller'
        )
        
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='Test Description',
            price=100.00,
            stock=10,
            seller=self.seller,
            shop=self.shop,
            category=self.category
        )
    
    def test_favorite_creation(self):
        """Тест создания избранного товара"""
        favorite = Favorite.objects.create(user=self.user, product=self.product)
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.product, self.product)
    
    def test_favorite_unique_constraint(self):
        """Тест уникальности пары user-product"""
        Favorite.objects.create(user=self.user, product=self.product)
        
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, product=self.product)


class FavoriteViewsTest(TestCase):
    """Тесты для views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='client'
        )
        
        self.shop = Shop.objects.create(name='Test Shop')
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            description='Test Description',
            price=100.00,
            stock=10,
            seller=self.seller,
            shop=self.shop,
            category=self.category
        )
    
    def test_toggle_favorite_requires_login(self):
        """Тест что toggle требует аутентификации"""
        response = self.client.get(f'/favorites/toggle/{self.product.id}/')
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_favorite_list_requires_login(self):
        """Тест что список требует аутентификации"""
        response = self.client.get('/favorites/list/')
        self.assertEqual(response.status_code, 302)
    
    def test_toggle_favorite_add(self):
        """Тест добавления товара в избранное"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/favorites/toggle/{self.product.id}/')
        
        self.assertTrue(Favorite.objects.filter(user=self.user, product=self.product).exists())
    
    def test_toggle_favorite_remove(self):
        """Тест удаления товара из избранного"""
        Favorite.objects.create(user=self.user, product=self.product)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(f'/favorites/toggle/{self.product.id}/')
        
        self.assertFalse(Favorite.objects.filter(user=self.user, product=self.product).exists())
    
    def test_favorite_list_view(self):
        """Тест отображения списка избранных товаров"""
        Favorite.objects.create(user=self.user, product=self.product)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/favorites/list/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
