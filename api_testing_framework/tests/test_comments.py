def test_get_comments_for_post(client):
    response = client.get("posts/1/comments")

    assert response.status_code == 200

    comments = response.json()

    assert isinstance(comments, list)
    assert comments
    assert all(comment["postId"] == 1 for comment in comments)
