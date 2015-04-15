#!/usr/bin/env python
import hashlib
import re

import dicom

from os.path import join
from dicom.errors import InvalidDicomError

FIELD_TAGS = [(0x10, 0x10), (0x08, 0x090), ]
SECRET = "**********"

class Anonymize(object):
    """
        Class responsible to anonymize DICOM files
    """
    def __init__(self, silent=False):
        if not silent:
            self.gui_object = MainGui()
            self.folder_path = self.gui_object.dirname
            self.file_name_list = self.gui_object._list_dir()

    def anonymize(self, dicom_list):
        """
            Replace all desired field (FIELD_TAGS) with ********* (SECRET)
        """
        for dicom_file, dicom_name in zip(dicom_list, self.file_name_list):
            dicom_file = self.__hide(dicom_file)
            self._save_dicom_file(dicom_file, dicom_name)

    def main(self):
        """
            Main method.
        """
        #Read DICOM files from selected folder
        dicom_list = self._open_dicom_files()
        #Check if there are more than one patient
        any_error = self._check_patient(dicom_list)
        self.gui_object._input_gui()
        studyid = self.gui_object.studyid
        if studyid and dicom_list:
            if not any_error:
                try:
                    #Create a SubFolder inside selected Folder
                    #Called Anonymized
                    self._make_subfolder()
                    dicom_list = self._set_studyid(dicom_list, studyid)
                    #Create a text file with DICOM information
                    self._render_template(dicom_list[0], studyid)
                    self.anonymize(dicom_list)
                    self._zip_files(studyid)
                except OSError, e:
                    self.gui_object.show_error_msgs("Create Folder Error", e)
            else:
                    self._patient_error_msg(any_error)

    def __hide(self, dicom_file):
        """
            Replace DICOM fields with **********
        """
        for dicom_tag in FIELD_TAGS:
            try:
                dicom_file[dicom_tag].value = SECRET
            except KeyError:
                continue
        return dicom_file

    def _set_studyid(self, dicom_list, studyid):
        """
            Replace the PatientId field with the generated one
        """
        for dicom_file in dicom_list:
            dicom_file[0x10, 0x20].value = studyid
        return dicom_list

    def _render_template(self, dicom_file, studyid):
        template_loader = jinja2.FileSystemLoader(searchpath='.')
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "template.jinja"
        template = template_env.get_template(template_file)

        context = self._prepare_context(dicom_file)
        output_template = template.render(context)
        self._save_template(output_template, studyid)

    def open_dicom_files(self, file_names):
        """
            Create a list with all DICOM objects in the selected folder
        """
        dicom_list = [dicom.read_file(file_name) for file_name in file_names
                if file_name]
        return dicom_list

    def is_one_patient(self, dicom_list):
        """
            Check if all files in the selected folder belongs to the same
            patient based on the name of the first patient.
            This function returns a list containing the position in the folder
            representing files with differents patient name
        """
        #Get the name in the first Dicom File and use it to compare with the
        #others Dicom files
        if dicom_list:
            pivot_name = dicom_list[0][FIELD_TAGS[0]].value
            #Find the indexes of files that are different from the pivot
            #file name
            patient_error = [file_index for file_index in
                    range(len(dicom_list)) if
                    dicom_list[file_index][FIELD_TAGS[0]].value != pivot_name]
            return len(patient_error) == 0

    def is_anonymized(self, dicom_list):
        for dicom_file in dicom_list:
            for tag in FIELD_TAGS:
                if dicom_file[tag].value != "**********":
                    return False
        return True

    def get_studyid(self, dicom_file):
        birthday = dicom_file[0x10, 0x30].value
        studydate = dicom_file[0x08, 0x20].value
        studyid = hashlib.sha224(birthday + studydate).hexdigest()[0:11]
        return str(studyid)

    def _patient_error_msg(self, patient_error):
        """
            Raises a Error Message if there are more than on patient inside
            selected folder
        """
        error_msg = "There are more than one patient in the selected" +\
        " folder:\n"
        if len(patien_error) < 5:
            patient_names = ' '.join(["\n" + str(self.file_name_list[name])
                for name in patient_error])
        else:
            patient_names = ' '.join(["\n" + str(self.file_name_list[name])
                for name in patient_error[0:6]])
            patient_name += "\n..."

        error_msg += patient_names
        self.gui_object.show_error_msgs("Patient Error", error_msg)


if __name__ == '__main__':
    anonymizer_obj = Anonymize()
    if anonymizer_obj.folder_path:
        anonymizer_obj.main()
#    anonymizer_obj.gui_object.show_error_msgs("Dicom Files not Found",
#            "There are no DICOM files in the selected Folder")

