

def process_folder(input_files):
    picture_groups = []
    for input_image in input_files:
        print(input_image.filename)
        similar = False
        # Present the list in reverse because the most similar group is most likely the last one.
        # It saves about 25% on time overall.
        for group in picture_groups[::-1]:
            similar, same_blocks, different_blocks = compare_images(group[0], input_image)
            # similar, same_blocks, different_blocks = compare_images(group[0], input_image)
            if similar:
                group.append(input_image)
                # If this is not the group's first image, close it for now
                if len(group) > 1:
                    input_image.close()
                break
        if similar:
            continue
        else:
            picture_groups.append([input_image])
    # print(picture_groups)
    groupid = 0

    for group in picture_groups:
        print("Group ID:" + str(groupid))
        for img in group:
            print("Picture: " + img.filename)
            img.close()
        groupid += 1

    return picture_groups


def process_numpys(input_files, options=None):
    """ Group together images given as numpy arrays. """
    picture_groups = []
    for input_image in input_files:
        similar = False
        for group in picture_groups[::-1]:
            similar, same_blocks, different_blocks = image_difference(input_image, group[0])
            if similar:
                group.append(input_image)
                break
        if similar:
            continue
        else:
            picture_groups.append([input_image])
    # Print results
    # gid = 0
    # for group in picture_groups:
    #     print("Group ID:" + str(gid))
    #     for img in group:
    #         print("Picture: " + str(img))
    #     gid += 1
    return picture_groups
