// generated from pong.yaml -- editing this file by hand is not recommended
inline std::ostream& operator<<(std::ostream& ss, const duels::pong::Position &position)
{
  ss << "{";
  ss << "x: " << position.x << ',';
  ss << "y: " << position.y << "}";
  return ss;
}
