gcc plug.def plug.a -shared -lwinmm -lWs2_32 -o plug.dll -Wl,--out-implib,plug.dll.a
echo "please use msvc tool run"
echo "lib /def:mian.def  /name:plug.dll  /out:plug.lib /MACHINE:X86"