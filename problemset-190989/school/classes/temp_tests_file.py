from _decimal import Decimal
from django.test import TestCase
from rest_framework import serializers
from .models import Classroom
from .serializers import ClassroomSerializer


class SerializerTest(TestCase):
    def serialization_assert_true(self, data):
        serializer = ClassroomSerializer(data=data)
        serializer.is_valid()
        data = serializer.data
        deserialized = ClassroomSerializer(data=data)
        self.assertTrue(deserialized.is_valid())

    def serializer_is_valid_assert_false(self, data):
        serializer = ClassroomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def deserialization(self, data):
        serializer = ClassroomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        classroom = serializer.save()
        self.assertEqual(classroom.name, data["name"])
        self.assertEqual(classroom.capacity, data["capacity"])
        self.assertEqual(classroom.department, data["department"])
        self.assertEqual(classroom.area, data["area"])

    def retrieval(self, data):
        classroom = Classroom.objects.get(name=data['name'])
        serializer = ClassroomSerializer(classroom)
        retrieved_data = serializer.data
        self.assertEqual(retrieved_data["name"], data['name'])
        self.assertEqual(retrieved_data["capacity"], data['capacity'])
        self.assertEqual(retrieved_data["department"], data['department'])
        self.assertEqual(retrieved_data["area"], data['area'])

    # def serializer_is_valid_assert_true(self, data):
    #     serializer = ClassroomSerializer(data=data)
    #     self.assertTrue(serializer.is_valid())

    # def serialize(self, data, serialized_data_with_id):
    #     classroom = Classroom.objects.create(**data)
    #     serializer = ClassroomSerializer(classroom)
    #     self.assertEquals(serializer.data, serialized_data_with_id)

    # def deserialize(self, serialized_data):
    #     serializer = ClassroomSerializer(data=serialized_data)
    #     self.assertTrue(serializer.is_valid())
    #     deserialized_object = serializer.save()
    #     expected_object = Classroom(**serialized_data)
    #     self.assertEquals(deserialized_object.capacity, expected_object.capacity)
    #     self.assertEquals(deserialized_object.name, expected_object.name)
    #     self.assertEquals(deserialized_object.department, expected_object.department)
    #     self.assertEquals(deserialized_object.area, expected_object.area)

    def test_valid_capacity_and_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_capacity_less_than_five(self):
        data = {'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        serialized_data_with_id = {'id': 1, 'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serializer_is_valid_assert_false(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)

    def test_area_less_than_zero(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': -1}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '-1.00'}

        self.serializer_is_valid_assert_false(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)

    def test_capacity_less_than_five_area_less_than_zero(self):
        data = {'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': -1}
        serialized_data_with_id = {'id': 1, 'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': '-1.00'}

        self.serializer_is_valid_assert_false(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)

    def test_valid_capacity_maximum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 999.99}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('999.99')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main',
                                   'area': '999.99'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_valid_capacity_minimum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 0}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.00')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.00'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_maximum_capacity_valid_area(self):
        data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        serialized_data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data_with_id = {'id': 1, 'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main',
                                   'area': '0.01'}
        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_minimum_capacity_valid_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 0}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.00')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.00'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_maximum_capacity_maximum_area(self):
        data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main', 'area': 999.99}
        serialized_data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main',
                           'area': Decimal('999.99')}
        serialized_data_with_id = {'id': 1, 'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main',
                                   'area': '999.99'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_minimum_capacity_minimum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_invalid_capacity_valid_area(self):
        data = {'capacity': 'capacity', 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        self.serializer_is_valid_assert_false(data=data)

    def test_valid_capacity_invalid_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 'area'}
        self.serializer_is_valid_assert_false(data=data)

    def test_empty_name(self):
        data = {'capacity': 5, 'department': 'main', 'area': 5}
        self.serializer_is_valid_assert_false(data=data)

    def test_string_int_capacity(self):
        data = {'capacity': '5', 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_string_decimal_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}
        serialized_data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': Decimal('0.01')}
        serialized_data_with_id = {'id': 1, 'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serializer_is_valid_assert_true(data=data)
        self.serialize(data=data, serialized_data_with_id=serialized_data_with_id)
        self.deserialize(serialized_data=serialized_data)

    def test_none_capacity_valid_area(self):
        data = {'capacity': None, 'name': 'Classroom 1', 'department': 'main', 'area': 5}
        self.serializer_is_valid_assert_false(data=data)

    def test_without_capacity_valid_area(self):
        data = {'name': 'Classroom 1', 'department': 'main', 'area': 5}
        self.serializer_is_valid_assert_false(data=data)

    def test_valid_capacity_none_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main', 'area': None}
        self.serializer_is_valid_assert_false(data=data)

    def test_valid_capacity_without_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main'}
        self.serializer_is_valid_assert_false(data=data)

    def test_valid_capacity_exceeding_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main', 'area': 9999.99}
        self.serializer_is_valid_assert_false(data=data)

    def test_decimal_capacity_valid_area(self):
        data = {'capacity': 5.5, 'name': 'Classroom 1', 'department': 'main', 'area': 10}
        self.serializer_is_valid_assert_false(data=data)

    def test_validate_capacity_method_five(self):
        self.assertEquals(ClassroomSerializer.validate_capacity(5), 5)

    def test_validate_capacity_method_less_than_five(self):
        with self.assertRaises(serializers.ValidationError):
            ClassroomSerializer.validate_capacity(3)

    def test_validate_capacity_method_more_than_five(self):
        self.assertEquals(ClassroomSerializer.validate_capacity(100), 100)

    def test_validate_area_method_zero(self):
        self.assertEquals(ClassroomSerializer.validate_area(0), 0)

    def test_validate_area_method_positive(self):
        self.assertEquals(ClassroomSerializer.validate_area(10), 10)

    def test_validate_area_method_negative(self):
        with self.assertRaises(serializers.ValidationError):
            self.assertEquals(ClassroomSerializer.validate_area(-10), -10)
