#include <signal.h>
#include <stdint.h>
#include <math.h>

#include "2048.h"

extern Game g; 

void handler()
{
    myprintf("time out!\n");
    exit(1);
}

void level1()
{
    myprintf("Hey, 2048 is so difficult. Let's begin from 256. I think everyone can reach it...?\n");
    myprintf("Press any key to start...\n");
    getchar();
    if (!play(16)) {
        myprintf("How can you lose? I can't believe it!\n");
        exit(0);
    } else {
        myprintf("Congraz! You pass 256! XD\n");
        clear_map();
    }
}

void init()
{
    signal(SIGALRM, handler);
    alarm(300);
    SIZE = 4;
    CHEAT = 1;
}

int menu()
{
    myprintf("======MENU======\n");
    myprintf("1. play again\n");
    myprintf("2. set map size\n");
    myprintf("3. show ranking\n");
    myprintf("4. set username\n");
    myprintf("5. exit\n");

    char buf[4];
    int c;

    while(1) {
        myprintf("> ");
        fgets(buf, 4, stdin);
        c = atoi(buf);
        if (!c)
            myprintf("Illegal choice!\n");
        else
            return c;
    }
}

void play_again()
{
    init_map();
    play(pow(2, SIZE * SIZE * 2 / 3 + 1));
    
}

void set_mapsize()
{
    myprintf("map size: ");
    char buf[4];
    SIZE = atoi(fgets(buf, 4, stdin));
}

void show_ranking()
{
}

void set_name()
{
    //off-by-one, open cheat mode
    myprintf("username: ");
    scanf("%20s", NAME);
}

int main()
{
    void* func[] = { play_again, set_mapsize, show_ranking, set_name };
    void (*ptr)();

    init();
    level1();
    while (1) {
        int8_t c = menu() - 1;
        if (c >= 4)
            exit(0);
        ptr = func[c]; // out of bound
        (*ptr)();
    }
    
    return 0;
}
