#include <iostream>
#include <fstream>
#include "serial.h"

using namespace std;

int main()
{
    int res;
    res = check_serial();

    if (res == TRUE) {
        cout << "Very good!" << endl;
        return SUCCESS;
    }
    
    cout << "Very bad!" << endl;
    return ERROR;    
}