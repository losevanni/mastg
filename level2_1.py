import sys,frida

PROCESS_NAME="owasp.mstg.uncrackable2"

jscode= """
console.log("[+] start ")
    Java.perform(function(){
        console.log("[+] Hooking")
        var exit_bypass=Java.use("java.lang.System");
        exit_bypass.exit.implementation=function(){
            console.log("[+] System.exit bypass")
        }
        var debug_bypass=Java.use("android.os.Debug");
        debug_bypass.isDebuggerConnected.implementation=function(){
            // console.log("[+] debug bypass")
            return false
        }
        Interceptor.attach(Module.findExportByName("libfoo.so","strncmp"),{
            onEnter: function(args){
                var param0=args[0]; // input
                var param1=args[1]; // pw
                var param2=args[2]; // lenght
                if(args[2].toInt32()==23){
                    var input= Memory.readUtf8String(args[0])
                    if("12345678901234567890123" == input){
                        console.log("[+] pw is "+Memory.readUtf8String(args[1]))
                    }
                }
            }
        });
    })

"""
session=frida.get_usb_device().attach(PROCESS_NAME)
script=session.create_script(jscode)
print('[*] Running Hook')
print(session)
script.load()
sys.stdin.read()
    