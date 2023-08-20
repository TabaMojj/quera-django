import io
from _decimal import Decimal
from rest_framework.test import APIClient

from django.http import JsonResponse
from django.test import TestCase
from rest_framework import serializers
from rest_framework.parsers import JSONParser

from .models import Classroom
from .serializers import ClassroomSerializer

CAPACITY_MESSAGE = 'Capacity should be equal or more than 5'
AREA_MESSAGE = 'Area should be positive'
BLANK_MESSAGE = 'This field may not be blank.'
MAX_LENGTH_MESSAGE = 'Ensure this field has no more than 50 characters.'
VALID_INTEGER_MESSAGE = 'A valid integer is required.'
NULL_MESSAGE = 'This field may not be null.'
VALID_NUMBER_MESSAGE = 'A valid number is required.'
REQUIRED_FIELD_MESSAGE = 'This field is required.'
DECIMAL_DIGITS_MESSAGE = 'Ensure that there are no more than 5 digits in total.'
MAXIMUM_CAPACITY_MESSAGE = 'Capacity should be equal or less than 2147483647'


class SerializerTest(TestCase):
    def serialization_assert_true(self, data):
        serializer = ClassroomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        data = serializer.data
        deserialized = ClassroomSerializer(data=data)
        self.assertTrue(deserialized.is_valid())

    def serializer_is_valid_assert_false(self, data, message):
        serializer = ClassroomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        # self.assertEqual(message, cm.exception.detail.popitem()[1][0])

    def deserialization(self, data):
        serializer = ClassroomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        classroom = serializer.save()
        self.assertEqual(classroom.name, str(data["name"]))
        self.assertEqual(classroom.capacity, int(data["capacity"]))
        self.assertEqual(classroom.department, str(data.get("department", 'main')))
        self.assertEqual(classroom.area, Decimal(data["area"]))

    def retrieval(self, data):
        classroom = Classroom.objects.get(name=data['name'])
        serializer = ClassroomSerializer(classroom)
        retrieved_data = serializer.data

        self.assertEqual(retrieved_data["name"], str(data['name']))
        self.assertEqual(retrieved_data["capacity"], int(data['capacity']))
        self.assertEqual(retrieved_data["department"], str(data.get("department", 'main')))
        self.assertEqual(retrieved_data["area"], data['area'])

    def test_valid_capacity_and_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_capacity_less_than_five(self):
        data = {'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}

        self.serializer_is_valid_assert_false(data=data, message=CAPACITY_MESSAGE)

    def test_area_less_than_zero(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': -1}

        self.serializer_is_valid_assert_false(data=data, message=AREA_MESSAGE)

    def test_capacity_less_than_five_area_less_than_zero(self):
        data = {'capacity': 4, 'name': 'Classroom 1', 'department': 'main', 'area': -1}

        self.serializer_is_valid_assert_false(data=data, message=AREA_MESSAGE)

    def test_valid_capacity_maximum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '999.99'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_valid_capacity_minimum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.00'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_maximum_capacity_valid_area(self):
        data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_minimum_capacity_valid_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.00'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_maximum_capacity_maximum_area(self):
        data = {'capacity': 2147483647, 'name': 'Classroom 1', 'department': 'main', 'area': '999.99'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_minimum_capacity_minimum_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_invalid_capacity_valid_area(self):
        data = {'capacity': 'capacity', 'name': 'Classroom 1', 'department': 'main', 'area': 0.01}
        self.serializer_is_valid_assert_false(data=data, message=VALID_INTEGER_MESSAGE)

    def test_valid_capacity_invalid_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': 'area'}
        self.serializer_is_valid_assert_false(data=data, message=VALID_NUMBER_MESSAGE)

    def test_string_decimal_area(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}

        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_string_int_capacity(self):
        data = {'capacity': '5', 'name': 'Classroom 1', 'department': 'main', 'area': '0.01'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_none_capacity_valid_area(self):
        data = {'capacity': None, 'name': 'Classroom 1', 'department': 'main', 'area': 5}
        self.serializer_is_valid_assert_false(data=data, message=NULL_MESSAGE)

    def test_without_capacity_valid_area(self):
        data = {'name': 'Classroom 1', 'department': 'main', 'area': 5}
        self.serializer_is_valid_assert_false(data=data, message=REQUIRED_FIELD_MESSAGE)

    def test_valid_capacity_none_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main', 'area': None}
        self.serializer_is_valid_assert_false(data=data, message=NULL_MESSAGE)

    def test_valid_capacity_without_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main'}
        self.serializer_is_valid_assert_false(data=data, message=REQUIRED_FIELD_MESSAGE)

    # def test_exceeding_capacity_valid_area(self):
    #     data = {'capacity': 3147483647, 'name': 'Classroom 1', 'department': 'main', 'area': '10.00'}
    #     self.serializer_is_valid_assert_false(data=data, message=MAXIMUM_CAPACITY_MESSAGE)

    def test_valid_capacity_exceeding_area(self):
        data = {'capacity': 10, 'name': 'Classroom 1', 'department': 'main', 'area': 9999.99}
        self.serializer_is_valid_assert_false(data=data, message=DECIMAL_DIGITS_MESSAGE)

    def test_decimal_capacity_valid_area(self):
        data = {'capacity': 5.5, 'name': 'Classroom 1', 'department': 'main', 'area': 10}
        self.serializer_is_valid_assert_false(data=data, message=VALID_INTEGER_MESSAGE)

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

    def test_valid_name(self):
        data = {'capacity': 5, 'name': 'Classroom 1', 'department': 'main', 'area': '10.00'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_int_name(self):
        data = {'capacity': 5, 'name': 123, 'department': 'main', 'area': '10.00'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_empty_name(self):
        data = {'capacity': 5, 'name': '', 'department': 'main', 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=BLANK_MESSAGE)

    def test_none_name(self):
        data = {'capacity': 5, 'name': None, 'department': 'main', 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=NULL_MESSAGE)

    def test_without_name(self):
        data = {'capacity': 5, 'department': 'main', 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=REQUIRED_FIELD_MESSAGE)

    def test_int_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 123, 'area': '10.00'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_empty_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': '', 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=BLANK_MESSAGE)

    def test_none_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': None, 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=NULL_MESSAGE)

    def test_without_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'area': '10.00'}
        self.serialization_assert_true(data=data)
        self.deserialization(data=data)
        self.retrieval(data=data)

    def test_very_long_name(self):
        data = {'capacity': 5, 'name': 'Class 1' * 100, 'department': 'Department', 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=MAX_LENGTH_MESSAGE)

    def test_very_long_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department' * 100, 'area': '10.00'}
        self.serializer_is_valid_assert_false(data=data, message=MAX_LENGTH_MESSAGE)

    def test_update_capacity_to_less_than_five(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 4, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_capacity_to_five(self):
        data = {'capacity': 6, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(classroom.capacity, 5)

    def test_update_capacity_to_more_than_five(self):
        data = {'capacity': 6, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 10, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(classroom.capacity, 10)

    def test_update_capacity_to_invalid(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 'capacity', 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_area_to_less_than_zero(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '-1'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_area_to_zero(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '0'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(classroom.area, Decimal(0))

    def test_update_area_to_positive(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '55.65'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(classroom.area, Decimal('55.65'))

    def test_update_name_empty(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'name': ''}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_name_none(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'name': None}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_department(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'department': 'Department 2'}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(classroom.department, 'Department 2')

    def test_update_department_empty(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'department': ''}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_update_department_none(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        updated_data = {'department': None}
        classroom = Classroom.objects.create(**data)
        serializer = ClassroomSerializer(classroom, data=updated_data, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_serializer_has_validate_capacity_method(self):
        self.assertTrue(callable(getattr(ClassroomSerializer, 'validate_capacity', False)))

    def test_serializer_has_validate_area_method(self):
        self.assertTrue(callable(getattr(ClassroomSerializer, 'validate_area', False)))

    def test_post_valid(self):
        data = {'capacity': 5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        client = APIClient()
        s = ClassroomSerializer(data=data)
        s.is_valid()
        response: JsonResponse = client.post('/json/', s.data)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertTrue(ClassroomSerializer(data=data).is_valid())
        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        data = {'capacity': 5.5, 'name': 'Class 1', 'department': 'Department', 'area': '10.00'}
        client = APIClient()
        response: JsonResponse = client.post('/json/', data)
        stream = io.BytesIO(response.content)
        self.assertEqual(response.status_code, 400)
