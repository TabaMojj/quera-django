from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from books.models import Book
from authors.models import Author
from discounts.models import AuthorDiscount, CountryDiscount

User = get_user_model()


class SampleTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.farhad = User.objects.create(username='farhad', password='123456', country='IR')
        tolstoy = User.objects.create(username='tolstoy', password='123456')

        author = Author.objects.create(user=tolstoy)

        self.book = Book.objects.create(
            isbn='978-4-7741-8411-1',
            title='Biography of Farhad',
            content='Once upon a time, farhad was born on a cold winter day...',
            price=Decimal('100.0'),
        )
        self.book.authors.add(author)

        AuthorDiscount.objects.create(percent=Decimal('25'), author=author)
        CountryDiscount.objects.create(percent=Decimal('50'), country='IR')

    def test_get_discount(self):
        self.assertEqual(self.book.get_discount(), Decimal('75.00'))
        self.assertEqual(self.book.get_discount(user=self.farhad), Decimal('50.00'))

    def test_serializer(self):
        response = self.client.get('/books/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['price'], '100.00')
        self.assertEqual(response.data['price_after_discount'], 75)
        self.assertListEqual(response.data['authors'], [1])
        self.assertListEqual(response.data['categories'], [])
        self.assertIsNotNone(response.data['title'])
        self.assertIsNotNone(response.data['content'])

        self.client.force_authenticate(user=User.objects.get(username='farhad'))
        response = self.client.get('/books/1/')
        self.assertEqual(response.data['price_after_discount'], 50)

        response = self.client.post('/books/',
                                    {
                                        "isbn": "978-1-69698-378-7",
                                        "title": "python",
                                        "content": "hello world from python",
                                        "price": 1000,
                                        "authors": [1],
                                    })

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Book.objects.filter(isbn='978-1-69698-378-7').exists())
        book = Book.objects.get(isbn='978-1-69698-378-7')
        self.assertEqual(book.title, 'python')
        self.assertEqual(book.price, 1000)
        self.assertEqual(book.content, 'hello world from python')
        self.assertListEqual(list(book.authors.values_list('id', flat=True)), [1])
