#include <stdio.h>

int main()
{
    long long   cards    = 119315717514047;
    long long   shuffles = 101741582076661;

    long long   loop_count = 0;
    long        loop_count2 = 0;
    long long   shuffles2;
    long long   temp;
    double frac;

    printf("cards: %lld\n", cards);


     for( ; ; )
     {
        loop_count++;
        loop_count2++;
        for( int i = 0 ; i < 100 ; i++ )
        {
            temp = cards / 2;
            shuffles2 = shuffles - temp;
        }
        if( loop_count2 >= 1000000)
        {
            frac = (float)loop_count / (float)shuffles2;
            printf("Total shuffles: %lld (frac: %f)\n", loop_count, frac);
            loop_count2 = 0;
        }
     }
}
