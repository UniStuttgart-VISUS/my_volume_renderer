cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

# Create project
project(porous_volume_renderer LANGUAGES CXX)

# Build types
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;RelWithDebInfo;MinSizeRel" CACHE STRING "" FORCE)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the build type." FORCE)
endif()
set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS ${CMAKE_CONFIGURATION_TYPES})

# Collect source files
set(project_sources
  src/main.cpp
  src/mvr.cpp
  src/util/util.cpp
  src/util/texture.cpp
  src/util/geometry.cpp
  src/configraw.cpp
  src/util/transferfunc.cpp)

set(imgui_sources
  libs/imgui/imgui_impl_glfw.cpp
  libs/imgui/imgui_impl_opengl3.cpp
  libs/imgui/imgui.cpp
  libs/imgui/imgui_demo.cpp
  libs/imgui/imgui_draw.cpp
  libs/imgui/imgui_widgets.cpp
  libs/imgui/imgui_stdlib.cpp)

set(gl_sources
  libs/gl3w/GL/gl3w.c)

# Create executable
add_executable(porous_volume_renderer ${project_sources} ${imgui_sources} ${gl_sources})

target_include_directories(porous_volume_renderer PRIVATE
  src
  include
  libs/gl3w
  libs/imgui
  libs/nlohmann)

set_target_properties(porous_volume_renderer PROPERTIES CXX_STANDARD 14)

# Add OpenMP
find_package(OpenMP REQUIRED)
target_link_libraries(porous_volume_renderer PRIVATE OpenMP::OpenMP_CXX)

# Add Boost
set(Boost_USE_STATIC_LIBS ON)
find_package(Boost REQUIRED COMPONENTS system filesystem regex program_options)
target_link_libraries(porous_volume_renderer PRIVATE
  Boost::system
  Boost::filesystem
  Boost::regex
  Boost::program_options)

# Add GLFW
add_subdirectory(libs/glfw)
target_link_libraries(porous_volume_renderer PRIVATE glfw ${GLFW_LIBRARIES})
target_include_directories(porous_volume_renderer PRIVATE libs/glfw/include)

# Add GLM
add_subdirectory(libs/glm)
target_link_libraries(porous_volume_renderer PRIVATE glm::glm)

# Add FreeImage
find_path(FreeImage_INCLUDE_DIR FreeImage.h HINTS ${FreeImage_ROOT})
find_library(FreeImage_LIBRARY NAMES FreeImage HINTS ${FreeImage_ROOT})

if ((NOT FreeImage_INCLUDE_DIR) OR (NOT FreeImage_LIBRARY))
  message(FATAL_ERROR "Unable to find FreeImage library. Provide the path in FreeImage_ROOT!")
endif()

target_link_libraries(porous_volume_renderer PRIVATE ${FreeImage_LIBRARY})
target_include_directories(porous_volume_renderer PRIVATE ${FreeImage_INCLUDE_DIR})

# Output compiler warnings
if (UNIX)
  target_compile_definitions(porous_volume_renderer PRIVATE -Wall -Wextra)
endif()

# Copy shaders and example data
file(COPY src/shader DESTINATION src)
file(COPY exampleData DESTINATION .)

# Install mechanism
# TODO
