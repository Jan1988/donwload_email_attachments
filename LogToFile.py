import datetime

DateTextFile = "log.txt"


def get_latest_uid():

    f = open(DateTextFile, 'r')
    latest_uid_str = f.readline()
    if not latest_uid_str:
        latest_uid = 0
    else:
        latest_uid = int(latest_uid_str)
    f.close()

    return latest_uid


# converts uid of last fetched email into string and writes into 'log.txt'
def write_latest_uid(new_latest_uid):

    str_new_latest_uid = new_latest_uid.decode("utf-8")

    f = open(DateTextFile, 'w')
    f.write(str_new_latest_uid)
    f.close()
