cmake_minimum_required(VERSION 3.21)

project(boilerplate VERSION 0.1.0)

if(MSVC)
    add_definitions( /std:c++latest )
elseif(APPLE)
    add_definitions( -Wall -o2 -g -ggdb -DSOCKLEN_T=socklen_t -Wc++17-extensions -stdlib=libc++ )
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++1z")
else()
    add_definitions( -Wall -std=c++17 -o2 -g -ggdb -fconcepts -DSOCKLEN_T=socklen_t )
endif()

enable_testing()

find_package(GTest CONFIG REQUIRED)

add_subdirectory(codex)
add_subdirectory(test)