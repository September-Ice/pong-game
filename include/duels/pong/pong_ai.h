#ifndef PONG_AI_H
#define PONG_AI_H

#include <duels/player.h>
#include <duels/pong/msg.h>

namespace duels {
namespace pong {

// built-in AI class, should be heavily adapted to your needs
class PongAI : public duels::Player<Input, Feedback>
{
public:
  PongAI(int difficulty = 1) : difficulty(difficulty) {}

  void updateInput()
  {
    // in this function the `feedback` member variable was updated from the game
    // TODO update the `input` member variable
    // the `difficulty` member variable may be used to tune your AI (0 = most stupidest)
    // do not hesitate to create a .cpp file if this function is long
  }

private:
  int difficulty = 1;
};
}
}
#endif
