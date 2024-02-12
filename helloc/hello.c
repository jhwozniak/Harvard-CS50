#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("Give ma your name please: ");
    printf("hello, %s\n", name);
}