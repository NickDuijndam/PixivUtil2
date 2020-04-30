# -*- coding: utf-8 -*-

import os
import demjson
import PixivUtil2

_default_batch_filename = "./batch_job.json"


class JobOption(object):
    filenameFormat = ""
    filenameMangaFormat = ""
    filenameInfoFormat = ""
    filenameMangaInfoFormat = ""
    avatarNameFormat = ""
    rootDirectory = ""
    useTagsAsDir = False

    def __init__(self, job, _config):
        if _config is None:
            raise Exception("Cannot get default configuration, aborting...")
        # set default option from config
        self.filenameFormat = _config.filenameFormat
        self.filenameMangaFormat = _config.filenameMangaFormat
        self.filenameInfoFormat = _config.filenameInfoFormat
        self.filenameMangaInfoFormat = _config.filenameMangaInfoFormat
        self.avatarNameFormat = _config.avatarNameFormat
        self.rootDirectory = _config.rootDirectory
        self.useTagsAsDir = _config.useTagsAsDir

        if "option" in job and job["option"] is not None:
            # need to check if the job option exists for each option
            option_data = job["option"]
            if "filenameFormat" in option_data:
                self.filenameFormat = option_data["filenameFormat"]
            if "filenameMangaFormat" in option_data:
                self.filenameMangaFormat = option_data["filenameMangaFormat"]
            if "filenameInfoFormat" in option_data:
                self.filenameInfoFormat = option_data["filenameInfoFormat"]
            if "filenameMangaInfoFormat" in option_data:
                self.filenameMangaInfoFormat = option_data["filenameMangaInfoFormat"]
            if "avatarNameFormat" in option_data:
                self.avatarNameFormat = option_data["avatarNameFormat"]
            if "rootDirectory" in option_data:
                self.rootDirectory = option_data["rootDirectory"]
            if "use_tags_as_dir" in option_data:
                self.useTagsAsDir = option_data["useTagsAsDir"]


def handle_members(caller, job, job_name, job_option):
    member_ids = list()
    if "member_ids" in job:
        print("Multi Member IDs")
        member_ids = job["member_ids"]
    elif "member_id" in job:
        member_id = job["member_id"]
        member_ids.append(member_id)
    else:
        print(f"No member_id or member_ids found in {job_name}!")
        return

    for member_id in member_ids:
        print(f"Member ID: {member_id}")


def handle_images(caller: PixivUtil2, job, job_name, job_option):
    image_ids = list()
    if "image_ids" in job:
        print("Multi Image IDs")
        image_ids = job["image_ids"]
    elif "member_id" in job:
        image_id = job["image_id"]
        image_ids.append(image_id)
    else:
        print(f"No image_id or image_ids found in {job_name}!")
        return

    for image_id in image_ids:
        print(f"Processing {image_id}")
        caller.process_image(image_id=image_id, user_dir=job_option.rootDirectory, title_prefix=job_name)


def handle_tags(caller, job, job_name, job_option):
    if "tags" in job:
        tags = job["tags"]
        print(f"Processing {tags}")
    else:
        print(f"No tags found in {job_name}!")


def process_batch_job(caller: PixivUtil2):
    caller.set_console_title("Batch Menu")
    if os.path.exists(_default_batch_filename):
        jobs_file = open(_default_batch_filename, encoding="utf-8")
        jobs = demjson.decode(jobs_file.read())
        for job_name in jobs["jobs"]:
            print(f"Processing {job_name}")
            curr_job = jobs["jobs"][job_name]

            if "job_type" not in curr_job:
                print(f"Cannot find job_type in {job_name}")
                continue

            job_option = JobOption(curr_job, caller.__config__)
            if curr_job["job_type"] == '1':
                handle_members(caller, curr_job, job_name, job_option)
            elif curr_job["job_type"] == '2':
                handle_images(caller, curr_job, job_name, job_option)
            elif curr_job["job_type"] == '3':
                handle_tags(caller, curr_job, job_name, job_option)
            else:
                print(f"Unsupported job_type {curr_job['job_type']} in {job_name}")


if __name__ == '__main__':
    import PixivUtil2
    process_batch_job(PixivUtil2)
