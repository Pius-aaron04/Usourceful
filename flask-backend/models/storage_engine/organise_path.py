#!/usr/bin/python3

"""
Script to organise users' files on storage server
"""

import os

def create_user_dir(user_id):
    user_dir = os.path.join(BASEDIR, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    image_dir = os.path.join(user_dir, 'images')
    video_dir = os.path.join(user_dir, 'videos')

    os.makedirs(image_dir)
    os.makedirs(video_dir)

    return True


def delete_user_dir(user_id):
    user_dir = os.path.join(BASEDIR, user_id)

    if os.path.exists(user_dir):
        os.remove(user_dir)

    return True
