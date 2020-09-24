#include <iostream>
#include <fstream>
#include "serial.h"

using namespace std;

int main()
{
    int res;
    res = write_serial();

    if (res == SUCCESS) {
        cout << "Activation is succeed!" << endl;
        return SUCCESS;
    }
    
    cout << "Activation is failed!" << endl;
    return ERROR;
}