#include <signal.h>
#include <stdint.h>

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
    init_map();
    if (play(16)) {
        myprintf("Congraz! You pass 256! XD\n");
        clear_map();
    } else {
        myprintf("How can you lose? I can't believe it!\n");
        exit(0);
    }
}

void init()
{
    signal(SIGALRM, handler);
    alarm(300);
    SIZE = 4;
    CHEAT = 1;
    sprintf(NAME, "Player");
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
    int goal = count_goal();
    if (goal == 0) {
        myprintf("It's impossible to win the game.\n");
    } else if (play(goal)) {
        myprintf("Congraz! You pass %d! XD\n", goal);
    } else
        myprintf("You lose. What a pity.");
    
}

void set_mapsize()
{
    myprintf("map size: ");
    char buf[4];
    int size = atoi(fgets(buf, 4, stdin));
    if (size < 4)
        myprintf("Map too small!\n");
    else
        SIZE = size;
}

void show_ranking()
{
}

void set_name()
{
    myprintf("current name: %s\n", NAME);
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
        uint8_t c = menu();
        if (c > 5)
            continue;
        ptr = func[c - 1];
        (*ptr)();
    }
    
    return 0;
}
