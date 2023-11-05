cmake_minimum_required(VERSION 3.21)

project(boilerplate VERSION 0.1.0)

if(MSVC)
    add_definitions( /std:c++latest )
endif()

enable_testing()

find_package(GTest CONFIG REQUIRED)

add_subdirectory(codex)
add_subdirectory(test)