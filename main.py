import obd


# a callback that prints every new value and its timestamp to the console
def callback(r):
    print(r.time, ",", r.value)


def main():

    # OR
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
    connection.watch(obd.commands.RPM, callback=callback)  # keep track of the RPM
    connection.watch(obd.commands.SPEED, callback=callback)  # keep track of the RPM
    connection.start()  # start the async update loop

    # print(connection.query(obd.commands.RPM))  # non-blocking, returns immediately


if __name__ == '__main__':
    main()