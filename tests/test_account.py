class TestAccount:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_create_account(self, client):
        name = "For test_create_account 01"
        email = "test01@gmail.com"
        password = "top_s1cret_01"

        response = client.post(
            "/accounts/", json={"name": name, "email": email, "password": password}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name
        assert data["email"] == email
        assert "password" not in data
        assert "id" in data

    def test_create_account_with_same_email(self, client, default_account):
        # Arrange: Provide the attr
        name = "First"
        email = default_account.email
        password = "first_secret"

        # Act: Create an account with same email with the default account
        response = client.post(
            "/accounts/", json={"name": name, "email": email, "password": password}
        )

        # Assert: It should fails with 404
        assert response.status_code == 404

    # def test_read_accounts(self, client):
    #     response = client.get("/accounts/")
    #     assert response.status_code == 200
    #     assert isinstance(response.json(), list)

    def test_read_my_account(self, client, default_account, default_token):
        # Act: Read it back
        response = client.get(
            "/accounts/me", headers={"Authorization": f"Bearer {default_token}"}
        )

        # Assert: Check if the value as expected
        assert response.status_code == 200
        assert response.json()["name"] == default_account.name

    def test_update_my_account(self, client, default_token):
        # Arrange: Set new name
        new_name = "This is new name"

        # Act: Update it
        patch = client.patch(
            "/accounts/me",
            json={"name": new_name},
            headers={"Authorization": f"Bearer {default_token}"},
        )
        assert patch.status_code == 200
        assert patch.json()["name"] == new_name

    def test_delete_my_account(self, client, default_account, default_token):
        # Act: Delete it
        delete = client.delete(
            "/accounts/me", headers={"Authorization": f"Bearer {default_token}"}
        )
        assert delete.status_code == 200
        assert delete.json() == {"ok": True}

        # Assert: Deleted account would raise 401 as token expired
        get = client.get(
            "/accounts/me", headers={"Authorization": f"Bearer {default_token}"}
        )
        assert get.status_code == 401
