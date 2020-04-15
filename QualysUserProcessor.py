import xml.etree.ElementTree as ET
import QualysAPI
import csv


def getUsers(api: QualysAPI.QualysAPI):
    fullurl = "%s/msp/user_list.php" % api.server
