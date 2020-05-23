# test/functional/test_user_logout.py


def test_user_logs_out(test_client, db_init, insert_user, login_user):
    response = test_client.get("/logout")
    assert response.status_code == 302
    assert response.location.endswith("/")
    with test_client.session_transaction() as updated_session:
        assert "_user_id" not in updated_session
