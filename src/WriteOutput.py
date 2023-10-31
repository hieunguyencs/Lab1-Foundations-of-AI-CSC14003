import os

import cv2
import pygame


def writeToFile(file_name="output.txt", path=None, bonus=0, WIN=None, frames=None):
    if path is None:
        return

    # Create the directory structure if it doesn't exist
    directory = os.path.dirname(file_name)
    # print(directory)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file_name, 'w') as out:
        leng = len(path)
        if leng == 0:
            out.write("NO")
        else:
            out.write(str(leng - 1 + bonus))
        # Write path if needed
        # out.write('\n')
        # for point in path:
        #     out.write('({}, {}) '.format(point[0], point[1]))
    if WIN is None:
        return
    image_path = file_name.split('.txt')[0] + '.png'
    pygame.image.save(WIN, image_path)

    video_path = file_name.split('.txt')[0] + '.mp4'
    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video codec
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (height, width))
    rotated_frames = [cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) for frame in frames]
    flipped_frames_horizontal = [cv2.flip(frame, 1) for frame in rotated_frames]
    for frame in flipped_frames_horizontal:
        out.write(frame)
    out.release()

    print("-----Saved cost(.txt) and path(.png) and video(.mp4) -----")


def checkDuplicatePointInPath(path):
    s = set()
    for point in path:
        p_tuple = tuple(point)
        if p_tuple in s:
            return True
        s.add(p_tuple)
    return False

def generate_output_path(maze_path, algorithm):
    # Extract the directory of the input maze path
    base_directory = maze_path[:-4]
    tmp = base_directory.split("/")
    tmp = tmp[2:]
    base_directory = "/".join(tmp)

    # Construct the output directory path
    output_directory = os.path.join('..', 'output', base_directory, algorithm)

    # print(output_directory)

    return output_directory


