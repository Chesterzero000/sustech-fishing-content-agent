"""CLI entrypoint for the social-manager skill using Click."""
import json
from typing import List, Optional

import click

from skills.social-manager.service import (
    create_post as service_create_post,
    get_posts as service_get_posts,
    delete_post as service_delete_post,
    add_comment as service_add_comment,
    get_comments as service_get_comments,
    like_post as service_like_post,
    unlike_post as service_unlike_post,
)


def _images_from_string(images_str: Optional[str]) -> List[str]:
    if not images_str:
        return []
    parts = [p.strip() for p in images_str.split(',') if p.strip()]
    return parts


@click.group(name="social")
def cli():
    """Social manager CLI group."""
    pass


@cli.command(name="create-post")
@click.option('--user-id', required=True, type=int, help='ID of the author')
@click.option('--content', required=True, type=str, help='Post content')
@click.option('--images', required=False, default='', help='Comma-separated image URLs')
@click.option('--spot-id', required=False, type=int, help='Spot identifier')
def cmd_create_post(user_id: int, content: str, images: str, spot_id: Optional[int]):
    images_list = _images_from_string(images)
    res = service_create_post(user_id, content, images_list, spot_id)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="get-posts")
@click.option('--user-id', required=True, type=int, help='Owner user id')
@click.option('--limit', required=False, default=20, type=int)
@click.option('--offset', required=False, default=0, type=int)
def cmd_get_posts(user_id: int, limit: int, offset: int):
    res = service_get_posts(user_id, limit, offset)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="delete-post")
@click.option('--post-id', required=True, type=int, help='Post id to delete')
@click.option('--user-id', required=True, type=int, help='Current user id')
def cmd_delete_post(post_id: int, user_id: int):
    res = service_delete_post(post_id, user_id)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="add-comment")
@click.option('--post-id', required=True, type=int, help='Post id to comment on')
@click.option('--user-id', required=True, type=int, help='Commenting user id')
@click.option('--content', required=True, type=str, help='Comment content')
def cmd_add_comment(post_id: int, user_id: int, content: str):
    res = service_add_comment(post_id, user_id, content)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="get-comments")
@click.option('--post-id', required=True, type=int, help='Post id to fetch comments for')
@click.option('--limit', required=False, default=20, type=int)
@click.option('--offset', required=False, default=0, type=int)
def cmd_get_comments(post_id: int, limit: int, offset: int):
    res = service_get_comments(post_id, limit, offset)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="like-post")
@click.option('--post-id', required=True, type=int, help='Post id to like')
@click.option('--user-id', required=True, type=int, help='User id liking the post')
def cmd_like_post(post_id: int, user_id: int):
    res = service_like_post(post_id, user_id)
    click.echo(json.dumps(res, ensure_ascii=False))


@cli.command(name="unlike-post")
@click.option('--post-id', required=True, type=int, help='Post id to unlike')
@click.option('--user-id', required=True, type=int, help='User id unliking the post')
def cmd_unlike_post(post_id: int, user_id: int):
    res = service_unlike_post(post_id, user_id)
    click.echo(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':  # pragma: no cover
    cli()
