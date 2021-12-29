add_rules("mode.debug", "mode.release")

if is_mode("debug") then
    target("test")
    set_kind("binary")
    add_links("Dll2")
    add_linkdirs("$(projectdir)/lib")
    --add_linkdirs("$(buildir)/lib")
    add_files("test.cpp")
    set_toolchains("gcc")
else
    target("fuck")
    set_kind("shared")
    add_files("src/*.cpp")
    set_toolchains("gcc")
end




