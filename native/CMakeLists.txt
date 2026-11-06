cmake_minimum_required(VERSION 3.22)
project(pes2013_native_core LANGUAGES C CXX)

# O runtime ainda está em fase de auditoria.
# Adicione alvos somente após definir APIs e dependências verificadas.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(pes2013_core INTERFACE)
target_include_directories(pes2013_core INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
