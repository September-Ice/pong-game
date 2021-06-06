cmake_minimum_required(VERSION 2.8.3)
project(pong_server CXX)

set(DUELS_ROOT "/opt/duels" CACHE STRING "Path to duels dev folder")
set(CMAKE_INSTALL_PREFIX ${DUELS_ROOT})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Debug)
add_compile_options(-pthread)
find_package (Threads)

# find ZeroMQ
find_path ( ZMQ_INCLUDE_DIR zmq.h )
find_library ( ZMQ_LIBRARY NAMES zmq )

include_directories(include ${DUELS_ROOT}/include ${ZMQ_INCLUDE_DIR})
add_definitions(-DDUELS_BIN_PATH="${DUELS_ROOT}/bin")
add_definitions(-DGAME_SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}")
add_definitions(-DDUELS_SERVER)

add_executable(pong_server server.cpp)
target_link_libraries(pong_server ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARY})

# add whatever is needed to build display executable


# install server
install(TARGETS pong_server DESTINATION bin/pong)

# install gui and its deps
install(FILES pong_gui.py DESTINATION bin/pong
        PERMISSIONS OWNER_WRITE OWNER_READ OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
        
# client headers and templates
install(FILES include/duels/pong/game.h include/duels/pong/msg.h include/duels/pong/msg_detail.h DESTINATION include/duels/pong)
install(FILES client_template/CMakeLists.txt DESTINATION games/pong)
install(FILES client_template/pong.cpp DESTINATION games/pong )
