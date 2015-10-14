# -*- coding: UTF-8 -*-


def recreate_avatars():
    """ TODO: rewrite
    for model in (Person, Institution, Event, Document, PersonGroup):
        for obj in model.objects.all():
            rel_path = obj.get_original_image_rel_path()
            if rel_path:
                abs_path = UPLOADS_ROOT + rel_path
                image = Image.open(abs_path)
                obj.save_image(image)
                print obj
                print "    %s --> %s" % (
                    rel_path.split("/")[-1],
                    obj.get_original_image_rel_path(True).split("/")[-1]
                    )
    """


def recreate_portfolio_images():
    """ TODO: rewrite
    for model in (Person, Institution, Event, Document, PersonGroup):
        for obj in model.objects.all():
            list_of_files = []
            for filename in os.listdir(obj_media_path):
                media_file = {}
                if not fnmatch.fnmatch(filename, 'tn_*'):
                    if fnmatch.fnmatch(filename, '*.jpg'):
                        media_file = {
                            'file_type': 'image',
                            }
                    elif fnmatch.fnmatch(filename, '*.flv'):
                        media_file = {
                            'file_type': 'video',
                            }
                    if media_file:
                        media_file['filename'] = filename
                        media_file['original_path'] = "%soriginal/%s" % (
                            obj_media_path,
                            filename,
                            )
                        try:
                            file_obj = File.objects.get(
                                path="".join((relative_path, filename)),
                                )
                        except Exception:
                            file_obj = None
                        media_file['file_obj'] = file_obj
                        list_of_files.append(media_file)
            if list_of_files:
                print obj
            for media_file in list_of_files:
                new_filename = datetime.now().strftime("%Y%m%d%H%M%S.jpg")
                # add the new resized images
                path_original = os.path.join(obj_media_path, "original", new_filename)
                path_normal = os.path.join(obj_media_path, new_filename)
                path_preview = os.path.join(obj_media_path, "preview", new_filename)
                path_small = os.path.join(obj_media_path, "small", new_filename)
                image = save_jpg_image(
                    media_file['original_path'],
                    path_original=path_original,
                    path_normal=path_normal,
                    dimensions_normal=settings.IMAGE_MAX_SIZE,
                    path_preview=path_preview,
                    dimensions_preview=settings.IMAGE_PREVIEW_MAX_SIZE,
                    path_small=path_small,
                    dimensions_small=settings.IMAGE_SMALL_SIZE,
                    )
                # update the File object
                file_obj = media_file['file_obj']
                if file_obj:
                    file_obj.path = "".join((relative_path, new_filename))
                    file_obj.save()
                # remove the old version of files
                old_filename = media_file['filename']
                paths = [
                    os.path.join(obj_media_path, "original", filename),
                    os.path.join(obj_media_path, "original", "tn_%s" % filename),
                    os.path.join(obj_media_path, filename),
                    os.path.join(obj_media_path, "tn_%s" % filename),
                    os.path.join(obj_media_path, "preview", filename),
                    os.path.join(obj_media_path, "preview", "tn_%s" % filename),
                    os.path.join(obj_media_path, "small", filename),
                    os.path.join(obj_media_path, "small", "tn_%s" % filename),
                    ]
                for f in paths:
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                # report the change
                print "    %s --> %s" % (old_filename, new_filename)
                # wait for one second, because the next image has to have
                # a different file name
                time.sleep(1)
    """
