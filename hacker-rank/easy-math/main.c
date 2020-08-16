#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


int run(int x) {
    // factor out 4
    if ((x % 2) == 0) {
        x = x / 2;
        if ((x % 2) == 0) {
            x = x / 2;
        }
    }

    // factor out 2s and 5s and make them equal (to power of 10)
    int num_twos = 0;
    int num_fives = 0;
    while (x % 2 == 0) {
        num_twos += 1;
        x = x / 2;
    }
    while (x % 5 == 0) {
        num_fives += 1;
        x = x / 5;
    }

    int num_zeros = num_twos;
    if (num_fives > num_twos) {
        num_zeros = num_fives;
    }

    // Take the xprimes left over and find the smallest [1]+ number they can factor into
    int candidate = 1;
    int num_fours = 1;
    while (candidate % x != 0) {
        candidate = candidate * 10 + 1;
        num_fours += 1;
    }

    return num_fours * 2 + num_zeros;
}
int main() {
    int numInput;
    int input;
    scanf("%d",&numInput);
    for (int i = 0; i < numInput; i ++) {
        scanf("%d", &input);
        printf("%d\n", run(input));
    }
    return 0;
}
