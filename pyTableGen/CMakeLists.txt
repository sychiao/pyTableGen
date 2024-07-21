add_custom_target(copytbl ALL DEPENDS ${CMAKE_BINARY_DIR}/pyTableGen/pyproject.toml)
message(STATUS "copy ${CMAKE_CURRENT_SOURCE_DIR} to ${CMAKE_BINARY_DIR}/pyTableGen")
# copy all files to pyTableGen if any py or toml file changed
# because cmake dependency is static, so you should re-config cmake if you add new file
file(GLOB sources ./**.py ./**.toml)
add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/pyTableGen/pyproject.toml
                   COMMAND ${CMAKE_COMMAND} -E copy_directory
                   ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_BINARY_DIR}/pyTableGen
                   DEPENDS ${sources})

add_dependencies(copytbl tablegen)