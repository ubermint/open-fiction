from django.test import TestCase
from .models import Store, Book
from django.urls import reverse

class StoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Store.objects.create(
            city="New York", country="USA", open_date="Mon-Wed",
            address="st. Street", contact="example@example.com")

    def test_city_label(self):
        store = Store.objects.get(id=1)
        field_label = store._meta.get_field('city').verbose_name
        max_length = store._meta.get_field('city').max_length
        self.assertEquals(field_label, 'city')
        self.assertEquals(max_length, 30)

    def test_get_url(self):
        store = Store.objects.get(id=1)
        self.assertEquals(store.get_url(),'/store/1/')

class CatalogViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        books_num = 40
        s = Book.subjects()

        for i in range(books_num):
            Book.objects.create(
                uid=i, title=f"Title{i}", author = f"Author{i}", subject = [s[i%len(s)]],
                year=i, word_count=i, description="Description")

    def test_view_url_exists_at_desired_location(self):
        catalog = self.client.get('/')
        self.assertEqual(catalog.status_code, 200)

    def test_view_uses_correct_template(self):
        catalog = self.client.get(reverse('catalog'))
        self.assertEqual(catalog.status_code, 200)
        self.assertTemplateUsed(catalog, 'catalog.html')

    def test_pagination(self):
        catalog = self.client.get(reverse('catalog'))
        self.assertEqual(catalog.status_code, 200)
        self.assertTrue('is_paginated' in catalog.context)
        self.assertTrue(catalog.context['is_paginated'] == True)
        self.assertTrue(len(catalog.context['books']) == 20)