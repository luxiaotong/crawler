import time
import sys, getopt

def have_a_rest(sec):
    while sec > 0:
        msg = "Have a rest, and we will fight again in: %d seconds" %(sec)
        print(msg, '\r', end="")
        time.sleep(1)

        # below two lines is to replace the printed line with white spaces
        # this is required for the case when the number of digits in timer reduces by 1 i.e. from
        # 10 secs to 9 secs, if we dont do this there will be extra prints at the end of the printed line
        # as the number of chars in the newly printed line is less than the previous
        remove_msg = ' ' * len(msg)
        print( remove_msg, '\r', end="")

        # decrement timer by 1 second
        sec -= 1
    print("Let's Fight", '!'*10)
    return

def get_params():
    argv = sys.argv[1:]
    uids = ''
    last_record_time = ''
    try:
        opts, args = getopt.getopt(argv,"hu:l:",["uids=", "last_record_time="])
    except getopt.GetoptError:
        print ('pypost.py -u <user_id_list> -l <last_record_time>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('pypost.py -u <user_id_list> -l <last_record_time>')
            sys.exit()
        elif opt in ("-u", "--uids"):
            uids = arg
        elif opt in ("-l", "--last_record_time"):
            last_record_time = arg


    if last_record_time == '':
        print ('pypost.py -u <user_id_list> -l <last_record_time>')
        sys.exit()

    return uids, last_record_time
