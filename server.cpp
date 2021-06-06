#include <duels/pong/msg.h>
#include <duels/server.h>
#include <duels/pong/pong_ai.h>
#include <duels/pong/mechanics.h>

using namespace duels::pong;
using duels::Result;
using duels::Timeout;
using duels::Refresh;
using GameIO = duels::Server<InitDisplay, Input, Feedback, Display>;


int main(int argc, char** argv)
{
  GameIO game_io("pong", Timeout(50), Refresh(20));
  
  // simulation time
  [[maybe_unused]] const double dt(game_io.samplingTime());
  
  // TODO prepare game state / init message (for display)
  PongMechanics mechanics;
  InitDisplay init = mechanics.initGame();

  // inform displays and get players (multithread by default for simultaneous games)
  const auto [player1, player2] = game_io.initPlayers<PongAI>(argc, argv, init, 0, 1); {}

  

  while(true)
  {
    // extract feedbacks
    const auto result = mechanics.buildPlayerFeedbacks(player1->feedback, player2->feedback);
    // stop if game over
    if(result != Result::NONE)
    {
      game_io.endsWith(result);
      break;
    }
    
    // TODO build display information

    game_io.sendDisplay(mechanics.display());
    

    
    // request player actions, exits if any disconnect / crash
      if(!game_io.syncBothPlayers())
        break;

    // TODO update game state from player1->input and player2->input
    mechanics.update(player1->input, player2->input);    
    
    
  }

  // final results
  game_io.sendResult(mechanics.display());
}
