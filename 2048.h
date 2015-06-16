#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define SIZE g.size
#define SPACE g.space
#define BOARD g.board
#define SCORE g.score
#define CHEAT g.cheat
#define NAME g.name


struct game {
    uint16_t **board;
    uint8_t size;
    uint32_t space;
    uint32_t score;
    char name[20];
    uint8_t cheat; 
} typedef Game;

Game g;

void init_map();
void clear_map();
uint32_t count_goal();
int play(uint32_t);
