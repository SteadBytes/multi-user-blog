from google.appengine.ext import db
from models.user import User
from models.blogpost import BlogPost
from helpers import *


class Comment(db.Model):
    owner = db.ReferenceProperty(User,
                                 collection_name="comments")
    post = db.ReferenceProperty(BlogPost,
                                collection_name="comments")
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self, post_id="", current_user=""):
        return render_str("comment.html.j2", comment=self, post_id=post_id,
                          current_user=current_user)

    @classmethod
    def by_post_id(cls, post_id):
        """Get stored Comment instance corresponding to a post_id.

        Args:
            post_id: Integer, id of a post.
        Returns:
            Query object of Comment instances associated with the post
        """
        comments = Comment.all().filter('post_id =', int(post_id)).ancestor(comments_key())
        return comments

    @classmethod
    def by_owner_id(cls, owner_id):
        """Get stored Comment instance corresponding to a user_id.

        Args:
            owner_id: Integer, id of a user.
        Returns:
            Query object of Comment instances associated with the user
        """
        comments = Comment.all().filter('owner_id =', int(owner_id)).ancestor(comments_key())
        return comments

    @classmethod
    def by_id(cls, comment_id):
        """Get stored Comment instance corresponding to a comment_id.

        Args:
            post_id: Integer, id of a comment.
        Returns:
            Instance of Comment
        """
        return Comment.get_by_id(int(comment_id), parent=comments_key())

    @classmethod
    def make(cls, owner, post, content):
        """Create new Comment() model instance.

        Args:
            content: String, comment text
            owner_id: Int, primary ID of comment creator
            post_id: Int, primary ID of post comment made on
        Returns:
            Instance of Comment Model
        """

        return Comment(parent=comments_key(),
                       owner=owner,
                       post=post,
                       content=content)
