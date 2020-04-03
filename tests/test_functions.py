from lambdafunction.covidlambda import *
import pytest

def test_person():
    assert person_or_people(1) == "person"

def test_people():
    assert person_or_people(10) == "people"

def get_data_all():
    assert get_data() == "noh"