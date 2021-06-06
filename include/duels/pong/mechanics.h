#ifndef PONG_MECHANICS_H
#define PONG_MECHANICS_H

#include <duels/pong/msg.h>

using namespace duels::pong;
using duels::Result;

// base mechanics class, should be heavily adapted to reflect the game rules
class PongMechanics
{
public:
    PongMechanics() {}
    InitDisplay initGame() {
       InitDisplay init;

       init.width = 700;
       init.height = 500;
       init.p1.x = 20;
       init.p1.y = 200;
       init.p2.x = 670;
       init.p2.y = 200;
        return init;

    }
    inline const Display& display() const {

        return display_msg;

    }
    
    // game evolution can be put here, or just save the inputs for later when building the feedbacks
    void update(const Input &input1, const Input &input2)
    {
   //    input1.vel;
   //    input2.vel;

    }
    
    // should return who has just won, if any. May also compute display
    Result buildPlayerFeedbacks(Feedback &feedback1, Feedback &feedback2)
    {


        return Result::NONE;    // game goes on
    }

private:
  Display display_msg;
};

#endif 
