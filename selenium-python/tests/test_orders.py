def test_get_post_resource(client):
    response = client.get("posts/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["userId"] == 1


def test_get_comments_for_post(client):
    response = client.get("posts/1/comments")

    assert response.status_code == 200
    assert response.json()
    assert all(comment["postId"] == 1 for comment in response.json())
