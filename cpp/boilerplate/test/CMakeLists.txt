cmake_minimum_required(VERSION 3.21)

project(boilerplate_test VERSION 0.1.0)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../codex/include)


file(GLOB_RECURSE SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp )

add_executable(boilerplate_test ${SRCS})

target_link_libraries(boilerplate_test  
                        PRIVATE 
                        codex
                        GTest::gtest_main 
                        #GTest::gtest
                        #GTest::gmock 
                        #GTest::gmock_main
                        )

add_test(AllTests boilerplate_test)