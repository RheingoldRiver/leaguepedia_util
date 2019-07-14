import pytest
import responses
import requests
from data_dragon_client import DataDragonClient

@pytest.fixture
def new_client():
    '''Returns a new DataDragonClient instance'''
    return DataDragonClient()

# ----- getData() -----
@responses.activate
def test_get_data_success(new_client):
    responses.add(responses.GET, 'http://fake.com',
                    json={'key': '123'}, status=200)
    data = new_client.getData('http://fake.com')
    assert len(responses.calls) == 1
    assert data == {'key': '123'}

@responses.activate
def test_get_data_404_error(new_client):
    responses.add(responses.GET, 'http://fake.com', status=404)
    with pytest.raises(requests.exceptions.RequestException):
        new_client.getData('http://fake.com')
        assert len(responses.calls) == 1

@responses.activate
def test_get_data_500_error(new_client):
    responses.add(responses.GET, 'http://fake.com', status=500)
    with pytest.raises(requests.exceptions.RequestException):
        new_client.getData('http://fake.com')
        assert len(responses.calls) == 1

# ----- getChampionData() -----
@responses.activate
def test_get_champion_data_latest_success(new_client):
    responses.add(responses.GET, 'https://ddragon.leagueoflegends.com/cdn/patch_x/data/en_US/champion.json',
                    json={}, status=200)
    responses.add(responses.GET, 'https://ddragon.leagueoflegends.com/api/versions.json',
                    json=['patch_x', 'wrong_patch'], status=200)
    new_client.getChampionData('latest')
    assert len(responses.calls) == 2

@responses.activate
def test_get_champion_data_patch_success(new_client):
    PATCH='9.1.1'
    responses.add(responses.GET, 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(PATCH),
                    json={}, status=200)
    new_client.getChampionData(PATCH)
    assert len(responses.calls) == 1

# ----- getLatestPatch() ----
@responses.activate
def test_get_latest_patch_success(new_client):
    PATCH = 'right_patch'
    responses.add(responses.GET, 'https://ddragon.leagueoflegends.com/api/versions.json',
                    json=[PATCH, 'wrong_patch'], status=200)
    res = new_client.getLatestPatch()
    assert len(responses.calls) == 1
    assert res == PATCH
                