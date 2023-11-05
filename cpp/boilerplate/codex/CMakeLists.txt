cmake_minimum_required(VERSION 3.21)
project(codex VERSION 0.1.0)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

file(GLOB_RECURSE HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp )
file(GLOB_RECURSE SRCS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp )

add_library(codex STATIC ${HEADERS} ${SRCS})