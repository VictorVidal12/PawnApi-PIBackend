from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from routers.offer import dbConnect

client = TestClient(app)


def test_update_offer_state_finalizada(monkeypatch):
    # Arrange
    id = 8
    state = "finalizada"
    id_acceptant = 2

    # Act
    response = client.put(f"/update_offer_state?id={id}&state={state}&id_acceptant={id_acceptant}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": id, "state": "finalizada", "id_acceptant": id_acceptant}


def test_update_offer_state_other_states(monkeypatch):
    # Arrange
    id = 1
    state = "en_curso"

    # Simulamos la función update_offer_state
    mock_update_offer_state = AsyncMock(return_value={"id": id, "state": state})
    monkeypatch.setattr("routers.offer.dbConnect.update_offer_state", mock_update_offer_state)

    # Act
    response = client.put(f"/update_offer_state?id={id}&state={state}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": id, "state": state}
    mock_update_offer_state.assert_called_once_with(id, state)
