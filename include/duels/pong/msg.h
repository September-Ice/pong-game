// generated from pong.yaml -- editing this file by hand is not recommended
#ifndef PONG_MSG_H
#define PONG_MSG_H
#include <sstream>
#include <duels/game_state.h>
#include <duels/stream_overloads.h>
namespace duels {
namespace pong {

// utility structures
struct Position
{
  int x;int y;
  inline bool operator==(const Position &other) const
  {
    return x == other.x && y == other.y;
  }
};
}}

//detail on how to stream these structures
#include <duels/pong/msg_detail.h>

// core game messages
namespace duels {
namespace pong {

struct InitDisplay
{
  int width; int height; Position p1; Position p2;
  std::string toYAMLString(std::string name1, std::string name2) const 
  {
    std::stringstream ss;
    ss << "name1: " << name1;
    ss << "\nname2: " << name2;
    ss << "\nwidth: " << width;
    ss << "\nheight: " << height;
    ss << "\np1: " << p1;
    ss << "\np2: " << p2;
    return ss.str();
  }
};

struct Input
{
  float vel;
  std::string toString() const 
  {
    std::stringstream ss;
    ss << "vel: " << vel;
    return ss.str();
  }
};

struct Feedback
{
  Position me; Position opponent; Position ball;
  std::string toString() const 
  {
    std::stringstream ss;
    ss << "me: " << me;
    ss << "\nopponent: " << opponent;
    ss << "\nball: " << ball;
    return ss.str();
  }
  State __state;
};

struct Display
{
  Position p1; Position p2; Position ball;
  std::string toYAMLString(Result result) const 
  {
    std::stringstream ss;
    ss << "result: " << result;
    ss << "\np1: " << p1;
    ss << "\np2: " << p2;
    ss << "\nball: " << ball;
    return ss.str();
  }
};

}}
#endif