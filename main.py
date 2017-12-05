import obd
import random
import time


# a callback that prints every new value and its timestamp to the console
def callback(r):
    print(r.time, ",", r.value)


# def write_to_file(r, f):
#     f.write('\n' + r.time + "," + r.value)
#     # print(r.time, ",", r.value)


def closure(fl):
    f = open(fl, 'a', buffering=512)

    def write_to_file(r):
        f.write('\n' + r.time + "," + r.value)
        # print(r.time, ",", r.value)

    return write_to_file


# def rand_closure(fl):
#     f = open(fl, 'a', buffering=512)
#
#     def write_to_file(r):
#         f.write('\n' + str(time.time()) + "," + str(random.random()))
#         # print(r.time, ",", r.value)
#     return write_to_file


def main():

    ports = obd.scan_serial()  # return list of valid USB or RF ports

    # print(ports)  # ['/dev/ttyUSB0', '/dev/ttyUSB1']
    # connection = obd.OBD(ports[0])

    count = 0
    for port in ports:
        count = count + 1
        print("[%s] " % count + port)

    if count == 0:
        print("No ports")
        return

    while True and count > 0:
        selection = input("Select OBD port: ")
        if int(selection) > count:
            print("Wrong selection.")
            continue
        obd_port = ports[int(selection - 1)]

        print("Selected port: %s " % obd_port)
        break

    connection = obd.Async(obd_port)  # same constructor as 'obd.OBD()'

    callback_fun = closure('./output.txt')

    connection.watch(obd.commands.RPM, callback=callback_fun)  # keep track of the RPM
    connection.watch(obd.commands.SPEED, callback=callback_fun)  # keep track of the RPM
    try:
        connection.start()  # start the async update loop
    except KeyboardInterrupt:
            pass
    finally:
        connection.close()


    # print(connection.query(obd.commands.RPM))  # non-blocking, returns immediately


if __name__ == '__main__':
    main()