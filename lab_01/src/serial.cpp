#include <iostream>
#include <fstream>
#include "serial.h"

using namespace std;

int write_serial()
{
    int res;
    system("system_profiler SPHardwareDataType | grep 'Serial Number (system)' | awk '{print $4}' > license.key");
    
    if (res == 0) {
        return SUCCESS;
    } else {
        return ERROR;
    }
}

int check_serial()
{
    FILE *license_pipe, *license_file;
    char serial_buf[SIZE], serial_file[SIZE];
    int res_check = TRUE;

    memset(&serial_buf[0], 0, sizeof(serial_buf));
    memset(&serial_file[0], 0, sizeof(serial_file));

    license_pipe = popen("system_profiler SPHardwareDataType | grep 'Serial Number (system)' | awk '{print $4}'", "r");
    license_file = fopen("license.key", "r");

    if (license_pipe == NULL || license_file == NULL) {
        return FALSE;
    }

    fgets(serial_buf, sizeof(serial_buf), license_pipe);
    fgets(serial_file, sizeof(serial_file), license_file);

    for (int i = 0; i < SIZE; i++) {
        if (serial_file[i] != serial_buf[i]) {
            res_check = FALSE;
            break;
        }
    }

    return res_check;
}