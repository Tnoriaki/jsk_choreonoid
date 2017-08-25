set(target PyBodyUtil)
add_cnoid_python_module(${target} PyBodyUtilModule.cpp)
target_link_libraries(${target} boost_python CnoidBody)
