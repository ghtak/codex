cmake_minimum_required(VERSION 3.21)

project(boilerplate VERSION 0.1.0)

if(MSVC)
    add_definitions( /std:c++latest )
elseif(APPLE)
    add_definitions( -Wall -o2 -g -ggdb -std=c++17 -Wc++17-extensions  -stdlib=libc++  -DSOCKLEN_T=socklen_t)
    #include_directories(/Users/codex/works/vcpkg/installed/arm64-osx/include)
    #link_directories(/Users/codex/works/vcpkg/installed/arm64-osx/lib)
    set(GTest_DIR /Users/codex/works/vcpkg/installed/arm64-osx/share/gtest)
else()
    add_definitions( -Wall -std=c++17 -o2 -g -ggdb -fconcepts -DSOCKLEN_T=socklen_t )
endif()

enable_testing()


find_package(GTest CONFIG REQUIRED)

add_subdirectory(codex)
add_subdirectory(test)