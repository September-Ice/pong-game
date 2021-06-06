#ifndef PONG_GAME_H
#define PONG_GAME_H
#include <duels/client.h>
#include <duels/pong/msg.h>
#include <sstream>
namespace duels {
namespace pong {
class Game: public duels::Client<Input, Feedback>
{
public:
  Game(int argc, char** argv, std::string name, int difficulty = 1)
    : Game(argc, argv, name, difficulty, "localhost") {}
  Game(int argc, char** argv, std::string name, std::string ip, int difficulty = 1)
      : Game(argc, argv, name, difficulty, ip) {}
private:
  Game(int argc, char** argv, std::string name, int difficulty, std::string ip)
      : duels::Client<Input, Feedback>(
      argc, argv, 50, 140, name, difficulty, ip, "pong") {}
};
}
}
#endif